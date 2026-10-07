import subprocess,json,wave
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]
out=Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/preview/02-pandas-Complex-Sentences-With-Vocabulary.mp4')
probe=json.loads(subprocess.check_output(['/usr/local/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1280,720)
assert v['codec_name']=='h264' and a['codec_name']=='aac'
assert abs(float(probe['format']['duration'])-280.44)<.15
assert abs(float(v['avg_frame_rate'].split('/')[0])/float(v['avg_frame_rate'].split('/')[1])-30)<.01
subprocess.run(['/usr/local/bin/ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
raw=subprocess.check_output(['/usr/local/bin/ffmpeg','-v','error','-i',str(out),'-vn','-ar','48000','-ac','2','-f','f32le','-'])
x=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
with wave.open(str(p/'assets/source-audio.wav'),'rb') as w:original=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
checks=[]
for start,end in [(0.1,5),(60,65),(120,125),(189,194)]:
 i,j=round(start*48000),round(end*48000)
 c=float(np.corrcoef(original[i:j].ravel(),x[i:j].ravel())[0,1]);assert c>.97,(start,c)
 checks.append({'from_seconds':start,'to_seconds':end,'correlation':round(c,6)})
rms=float(np.sqrt(np.mean(x[round(196*48000):]**2)));assert rms<.0001
report={'ok':True,'width':1280,'height':720,'fps':30,'duration_seconds':float(probe['format']['duration']),'size_bytes':int(probe['format']['size']),'whole_file_decode':'passed','original_audio_windows':checks,'silent_outro_rms':rms,'page_count':17,'seconds_per_page':5}
(p/'.hyperframes/export-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
