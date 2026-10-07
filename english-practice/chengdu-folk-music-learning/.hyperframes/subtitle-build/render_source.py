from pathlib import Path
import json
import subprocess

ROOT = Path('/Users/mac/Documents/英语学习/english-practice/chengdu-folk-music-learning')
FFMPEG = Path('/Users/mac/Documents/英语学习/english-practice/.tools/ffmpeg-subtitles')
SOURCE = Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/full-video-English.mp4')
SRT = ROOT / 'assets/source.en.srt'
OUTPUT = ROOT / 'assets/source.new.mp4'
START = 218.08
END = 316.88
DURATION = END - START

video = (
    f"[0:v:0]trim=start={START}:end={END},setpts=PTS-STARTPTS,"
    f"subtitles=filename='{SRT}':force_style='FontName=Arial,FontSize=18,Outline=1,Shadow=0,MarginV=18,WrapStyle=2',"
    "format=yuv420p[v]"
)
audio = f"[0:a:0]atrim=start={START}:end={END},asetpts=PTS-STARTPTS[a]"
command = [
    str(FFMPEG), '-y', '-hide_banner', '-i', str(SOURCE),
    '-filter_complex', video + ';' + audio,
    '-map', '[v]', '-map', '[a]', '-t', f'{DURATION:.2f}',
    '-c:v', 'libx264', '-crf', '22', '-preset', 'fast', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(OUTPUT),
]
(ROOT / '.hyperframes/subtitle-build/render-command.json').write_text(json.dumps(command, indent=2) + '\n')
with (ROOT / '.hyperframes/subtitle-build/render.log').open('w') as log:
    result = subprocess.run(command, stdout=log, stderr=log)
if result.returncode:
    raise SystemExit(result.returncode)
OUTPUT.replace(ROOT / 'assets/source.mp4')
print(f'Created source cut {START:.2f}–{END:.2f}s ({DURATION:.2f}s).')
