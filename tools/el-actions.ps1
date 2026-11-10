# job handlers, dot-sourced by el-watch.ps1 for every job (edit freely, no restart needed).
# Uses $key, $job, $name, $jobs, $results, $raw from the runner. Never print or write $key.
$base = 'https://api.elevenlabs.io'
function Get-ElHeaders { @{ 'xi-api-key' = $key; 'Accept' = '*/*' } }
function Get-Json($path) { Invoke-RestMethod -Method Get -Uri ($base + $path) -Headers (Get-ElHeaders) -TimeoutSec 120 }
function Post-Json($path, $obj) {
  $bytes = [System.Text.Encoding]::UTF8.GetBytes(($obj | ConvertTo-Json -Depth 10 -Compress))
  Invoke-RestMethod -Method Post -Uri ($base + $path) -Headers (Get-ElHeaders) -Body $bytes -ContentType 'application/json; charset=utf-8' -TimeoutSec 180
}
function Write-Result($name, $obj) {
  $txt = $obj | ConvertTo-Json -Depth 12
  [System.IO.File]::WriteAllText((Join-Path $results ($name + '.json')), $txt, (New-Object System.Text.UTF8Encoding($false)))
}

    try {
      switch ($job.action) {
        'subscription' { Write-Result $name (Get-Json '/v1/user/subscription') }
        'voices'       { Write-Result $name (Get-Json '/v1/voices') }
        'get'          { Write-Result $name (Get-Json $job.path) }
        'shared_voices' {
          $out = @()
          foreach ($q in $job.queries) { try { $r = Get-Json ('/v1/shared-voices?' + $q.query); $out += @{ label = $q.label; result = $r } } catch { $m = $_.Exception.Message; if ($_.ErrorDetails) { $m = $m + ' ' + $_.ErrorDetails.Message }; $out += @{ label = $q.label; error = $m } } }
          Write-Result $name $out
        }
        'add_voice' {
          $out = @()
          foreach ($v in $job.voices) {
            try { $r = Post-Json ('/v1/voices/add/' + $v.public_owner_id + '/' + $v.voice_id) @{ new_name = $v.new_name }; $out += @{ ok = $true; voice = $v; result = $r } }
            catch { $out += @{ ok = $false; voice = $v; error = $_.Exception.Message } }
          }
          Write-Result $name $out
        }
        'tts' {
          $out = @(); $fmt = if ($job.output_format) { $job.output_format } else { 'mp3_44100_128' }
          foreach ($c in $job.clips) {
            $dest = Join-Path $raw $c.out
            if ((Test-Path $dest) -and -not $job.overwrite) { $out += @{ out = $c.out; ok = $true; skipped = $true }; continue }
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
            $body = @{ text = $c.text; model_id = $(if ($c.model_id) { $c.model_id } else { 'eleven_v4' }) }
            if ($c.voice_settings) { $body.voice_settings = $c.voice_settings }
            $bytes = [System.Text.Encoding]::UTF8.GetBytes(($body | ConvertTo-Json -Depth 6 -Compress))
            try {
              $resp = Invoke-WebRequest -Method Post -Uri ($base + '/v1/text-to-speech/' + $c.voice_id + '?output_format=' + $fmt) -Headers (Get-ElHeaders) -Body $bytes -ContentType 'application/json; charset=utf-8' -TimeoutSec 300 -UseBasicParsing
              [System.IO.File]::WriteAllBytes($dest, $resp.Content)
              $cc = $resp.Headers['character-cost']; $rid = $resp.Headers['request-id']
              $out += @{ out = $c.out; ok = $true; bytes = $resp.Content.Length; character_cost = "$cc"; request_id = "$rid" }
            } catch {
              $msg = $_.Exception.Message
              if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $msg = $msg + ' ' + $_.ErrorDetails.Message } else { try { $sr = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream()); $msg = $msg + ' ' + $sr.ReadToEnd() } catch {} }
              $out += @{ out = $c.out; ok = $false; error = $msg }
            }
            Write-Host ('  ' + $c.out)
          }
          Write-Result $name $out
        }
        default { Write-Result $name @{ error = ('unknown action ' + $job.action) } }
      }
    } catch {
      $msg = $_.Exception.Message
      if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $msg = $msg + ' ' + $_.ErrorDetails.Message } else { try { $sr = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream()); $msg = $msg + ' ' + $sr.ReadToEnd() } catch {} }
      Write-Result $name @{ error = $msg }
    }
