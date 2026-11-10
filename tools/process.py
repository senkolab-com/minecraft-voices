# mp3 (raw/<key>.mp3) -> mono 44.1 kHz Vorbis ogg, loudness-normalised (EBU R128 -16 LUFS, peak -1.5 dB), trimmed
# silence at both ends; writes ogg/<key>.ogg and ogg/durations.json (seconds).  usage: python3 process.py [keys...]
import json, os, subprocess, sys
V = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(V, 'raw'); OUT = os.path.join(V, 'ogg')
os.makedirs(OUT, exist_ok=True)
dp = os.path.join(OUT, 'durations.json'); durs = json.load(open(dp)) if os.path.exists(dp) else {}
keys = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(RAW) if f.endswith('.mp3'))
af = ('silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,'
      'silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.15,areverse,'
      'loudnorm=I=-16:TP=-1.5:LRA=11')
for k in keys:
    src = os.path.join(RAW, k + '.mp3'); dst = os.path.join(OUT, k + '.ogg')
    if not os.path.exists(src): print('missing', k); continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', af, '-ac', '1', '-ar', '44100', '-c:a', 'libvorbis', '-q:a', '4', dst], check=True)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', dst], capture_output=True, text=True).stdout.strip())
    durs[k] = round(d, 2); print(k, durs[k])
json.dump(durs, open(dp, 'w'), indent=1, sort_keys=True)
