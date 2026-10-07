import subprocess,json,wave
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]
out=Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/preview/01-back-in-china-Learning.mp4')
probe=json.loads(subprocess.check_output(['/usr/local/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1280,720)
assert v['codec_name']=='h264' and a['codec_name']=='aac'
assert abs(float(probe['format']['duration'])-58.64)<.15
subprocess.run(['/usr/local/bin/ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
raw=subprocess.check_output(['/usr/local/bin/ffmpeg','-v','error','-i',str(out),'-vn','-ar','48000','-ac','2','-f','f32le','-'])
x=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
checks=[]
for f,start in [('source-audio.wav',0),('voice-1.wav',24.64),('voice-2.wav',33.64),('voice-3.wav',42.64)]:
 with wave.open(str(p/'assets'/f),'rb') as w:
  orig=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2)/32768
 if start==0: orig=orig[:48000*5]
 n=len(orig);offset=round(start*48000);r=x[offset:offset+n]
 # Exclude 50ms clip edges, where AAC can smear transients into silence.
 c=float(np.corrcoef(orig[2400:-2400].ravel(),r[2400:-2400].ravel())[0,1])
 assert c>.97,(f,c)
 checks.append({'source':f,'placed_at_seconds':start,'waveform_correlation':round(c,6)})
silence=[]
for start,end in [(26,30),(36,39),(45,48),(51,58)]:
 rms=float(np.sqrt(np.mean(x[round(start*48000):round(end*48000)]**2)))
 assert rms<.0001,(start,rms)
 silence.append({'start':start,'end':end,'rms':rms})
report={'ok':True,'width':1280,'height':720,'duration_seconds':float(probe['format']['duration']),'size_bytes':int(probe['format']['size']),'codecs':[v['codec_name'],a['codec_name']],'whole_file_decode':'passed','original_audio_checks':checks,'followalong_silence_checks':silence}
(p/'.hyperframes/export-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
