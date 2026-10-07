from pathlib import Path
import json,subprocess, concurrent.futures
root=Path('/Users/mac/Documents/英语学习/english-practice/chengdu-pandas-learning');out=root/'.hyperframes/subtitle-build'
ff='/Users/mac/Documents/英语学习/english-practice/.tools/ffmpeg-subtitles';probe='/usr/local/bin/ffprobe'
source=root/'assets/source.mp4';wave=root/'assets/source-audio.wav'
def metadata(p):return json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(p)]))
m=metadata(source);w=metadata(wave)
print([(s['codec_type'],s['codec_name'],s.get('width'),s.get('height'),s.get('duration'),s.get('avg_frame_rate')) for s in m['streams']]);print('WAV',w['format']['duration'])
with (out/'decode.log').open('w') as log:r=subprocess.run([ff,'-hide_banner','-v','error','-i',str(source),'-map','0:v:0','-map','0:a:0','-f','null','-'],stdout=log,stderr=log)
print('Full decode exit:',r.returncode)
def snap(pair):
 n,t=pair;p=out/f'source-sample-{n:02}.png'
 subprocess.run([ff,'-y','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(source),'-frames:v','1',str(p)],check=True)
 return {'path':str(p),'time':t}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:shots=list(pool.map(snap,enumerate([2.0,26.3,49.1,107.0,148.0,194.8],1)))
from PIL import Image,ImageDraw
sheet=Image.new('RGB',(1920,760),'#efefef');draw=ImageDraw.Draw(sheet)
for i,shot in enumerate(shots):
 x=(i%3)*640;y=(i//3)*380
 img=Image.open(shot['path']);img.thumbnail((640,360));sheet.paste(img,(x,y));draw.text((x+12,y+363),f"Source clip {shot['time']:.2f}s",fill='black')
sheet.save(out/'source-contact-sheet.jpg',quality=93)
record={'planned_start_s':22.64,'planned_end_s':218.08,'planned_duration_s':195.44,'mp4_duration_s':float(m['format']['duration']),'streams':m['streams'],'wav_duration_s':float(w['format']['duration']),'wav_sample_rate_hz':w['streams'][0]['sample_rate'],'wav_channels':w['streams'][0]['channels'],'full_decode_exit_code':r.returncode,'full_decode_log_bytes':(out/'decode.log').stat().st_size,'subtitles_cues':85,'max_subtitle_lines':2,'max_line_characters':47,'subtitle_last_word':'them.','last_word_relative_start_s':194.44,'last_word_relative_end_s':195.14,'next_chapter_absolute_start_s':218.08,'screenshots':shots,'contact_sheet':str(out/'source-contact-sheet.jpg'),'source_no_old_subtitles': 'Only video/audio streams mapped; source mov_text stream excluded.'}
(root/'assets/source-verified.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
assert r.returncode==0
assert abs(float(m['format']['duration'])-195.44)<.07
assert w['streams'][0]['sample_rate']=='48000' and w['streams'][0]['channels']==2
assert len(m['streams'])==2
