# ElevenLabs job runner for the Minecraft voice pipeline.
# Runs on this PC, reads the API key ONLY from the user environment variable ELEVENLABS_API_KEY,
# never prints, logs or writes it. Watches C:\MinecraftServer\voices\jobs for *.json jobs, writes results\<job>.json
# and audio into raw\. Stop with Ctrl+C or by closing the window.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$jobs = Join-Path $root 'jobs'; $results = Join-Path $root 'results'; $raw = Join-Path $root 'raw'
$src = 'none'; $key = $null
foreach ($scope in 'Process', 'User', 'Machine') {
  $v = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY', $scope)
  if ($v -and $v.Trim().Trim('"').Trim("'").Length -gt 0) { $key = $v.Trim().Trim('"').Trim("'").Trim(); $src = $scope; break }
}
$diag = @{ runner = 'v3'; key_source = $src; key_length = $(if ($key) { $key.Length } else { 0 }); key_starts_sk = $(if ($key) { $key.StartsWith('sk_') } else { $false }); time = (Get-Date).ToString('s') }
$diag.runner = 'v4'
$tmp = Join-Path $results '_runner.json'
[System.IO.File]::WriteAllText($tmp, ($diag | ConvertTo-Json), (New-Object System.Text.UTF8Encoding($false)))
if (-not $key) { Write-Host 'ELEVENLABS_API_KEY is not set (or empty) - stopping.' -ForegroundColor Red; exit 1 }
Write-Host ('Voice job runner v4 ready - watching ' + $jobs) -ForegroundColor Green
while ($true) {
  Get-ChildItem $jobs -Filter *.json | Sort-Object Name | ForEach-Object {
    $f = $_; $name = $f.BaseName
    try { $job = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8) | ConvertFrom-Json } catch { return }
    try { Move-Item $f.FullName ($f.FullName + '.taken') -ErrorAction Stop } catch { return }
    Write-Host ((Get-Date).ToString('HH:mm:ss') + ' job ' + $name + ' (' + $job.action + ')')
    try { . (Join-Path $root 'el-actions.ps1') } catch { [System.IO.File]::WriteAllText((Join-Path $results ($name + '.json')), ('{"error":' + (ConvertTo-Json $_.Exception.Message) + '}')) }
    Move-Item ($f.FullName + '.taken') ($f.FullName + '.done') -Force
  }
  Start-Sleep -Seconds 2
}
