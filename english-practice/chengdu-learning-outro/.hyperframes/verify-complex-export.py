import subprocess,json,wave
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parents[1]
out=Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/preview/01-back-in-china-Complex-Sentences.mp4')
probe=json.loads(subprocess.check_output(['/usr/local/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'])==(1280,720)
assert v['codec_name']=='h264' and a['codec_name']=='aac'
assert abs(float(probe['format']['duration'])-58.64)<.15
subprocess.run(['/usr/local/bin/ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
raw=subprocess.check_output(['/usr/local/bin/ffmpeg','-v','error','-i',str(out),'-vn','-ar','48000','-ac','2','-f','f32le','-'])
x=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
with wave.open(str(p/'assets/source-audio.wav'),'rb') as w:original=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2)/32768
c=float(np.corrcoef(original[2400:-2400].ravel(),x[2400:len(original)-2400].ravel())[0,1]);assert c>.97
rms=float(np.sqrt(np.mean(x[round(22.8*48000):]**2)));assert rms<.0001
report={'ok':True,'width':1280,'height':720,'duration_seconds':float(probe['format']['duration']),'size_bytes':int(probe['format']['size']),'whole_file_decode':'passed','source_audio_correlation':round(c,6),'silent_outro_rms':rms,'replay_audio_present':False}
(p/'.hyperframes/complex-export-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
