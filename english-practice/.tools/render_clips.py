from pathlib import Path
import json, subprocess
root = Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice')
segments = json.loads(Path('/Users/mac/Documents/英语学习/english-practice/video-segments.json').read_text())
times = ','.join(str(s['start']) for s in segments[1:])
ffmpeg = '/Users/mac/Documents/英语学习/english-practice/.tools/ffmpeg-subtitles'
command = [ffmpeg, '-y', '-hide_banner', '-loglevel', 'warning', '-nostats',
 '-progress', '/tmp/chengdu-render-progress.txt',
 '-i', str(root/'full-video-English.mp4'), '-map', '0:v:0', '-map', '0:a:0',
 '-vf', "subtitles=/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/source/original.en.srt:force_style='FontName=Arial,FontSize=18,Outline=1,Shadow=0,MarginV=18'",
 '-c:v', 'libx264', '-crf', '22', '-preset', 'fast', '-threads', '4', '-pix_fmt', 'yuv420p',
 '-c:a', 'aac', '-b:a', '128k', '-force_key_frames', times,
 '-f', 'segment', '-segment_times', times, '-segment_time_delta', '0.017',
 '-reset_timestamps', '1', '-segment_start_number', '1', '-segment_format', 'mp4',
 '-segment_format_options', 'movflags=+faststart', str(root/'clips/.segment-%02d.mp4')]
subprocess.run(command, check=True)
for segment in segments:
 source=root/'clips'/('.segment-%02d.mp4' % segment['index'])
 target=root/'clips'/('%02d-%s-English.mp4' % (segment['index'],segment['slug']))
 source.rename(target)
print('Finished: 10 captioned clips.')
