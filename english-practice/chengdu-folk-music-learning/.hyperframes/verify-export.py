from pathlib import Path
import json
import subprocess
import numpy as np

ROOT = Path('/Users/mac/Documents/英语学习/english-practice/chengdu-folk-music-learning')
OUTPUT = Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/preview/03-chinese-folk-music-Complex-Sentences.mp4')
SOURCE = ROOT / 'assets/source.mp4'
EXPECTED_DURATION = 158.8
SOURCE_DURATION = 98.8


def run(*args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


probe = json.loads(run('/usr/local/bin/ffprobe', '-v', 'error', '-show_entries',
                       'format=duration:stream=index,codec_name,codec_type,width,height,avg_frame_rate,channels,sample_rate,duration',
                       '-of', 'json', str(OUTPUT)).stdout)
streams = probe['streams']
video = next(s for s in streams if s['codec_type'] == 'video')
audio = next(s for s in streams if s['codec_type'] == 'audio')
duration = float(probe['format']['duration'])
fps = eval(video['avg_frame_rate'], {'__builtins__': {}}, {})
assert video['codec_name'] == 'h264' and video['width'] == 1280 and video['height'] == 720
assert abs(fps - 30) < 0.01
assert audio['codec_name'] == 'aac'
assert abs(duration - EXPECTED_DURATION) < 0.15

run('/usr/local/bin/ffmpeg', '-v', 'error', '-xerror', '-i', str(OUTPUT), '-f', 'null', '-')


def audio_window(path, start, length):
    raw = run('/usr/local/bin/ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(length), '-i', str(path),
              '-map', '0:a:0', '-ar', '48000', '-ac', '2', '-f', 'f32le', 'pipe:1').stdout
    return np.frombuffer(raw, dtype='<f4')


correlations = []
for start, length in ((0.1, 4.5), (25, 5), (60, 5), (90, 5)):
    a = audio_window(OUTPUT, start, length)
    b = audio_window(SOURCE, start, length)
    n = min(len(a), len(b))
    corr = float(np.corrcoef(a[:n], b[:n])[0, 1]) if n else 0.0
    correlations.append({'from_seconds': start, 'to_seconds': start + length, 'correlation': round(corr, 6)})
    assert corr > 0.97, correlations[-1]

outro = audio_window(OUTPUT, SOURCE_DURATION + 1, EXPECTED_DURATION - SOURCE_DURATION - 2)
silent_rms = float(np.sqrt(np.mean(outro * outro))) if len(outro) else 0.0
assert silent_rms < 0.0001, silent_rms

report = {
    'ok': True,
    'width': video['width'],
    'height': video['height'],
    'fps': round(fps, 6),
    'duration_seconds': duration,
    'size_bytes': OUTPUT.stat().st_size,
    'whole_file_decode': 'passed',
    'original_audio_windows': correlations,
    'silent_outro_rms': silent_rms,
    'page_count': 12,
    'seconds_per_page': 5,
}
(ROOT / '.hyperframes/export-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
