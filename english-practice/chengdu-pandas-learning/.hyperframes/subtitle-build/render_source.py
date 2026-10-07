from pathlib import Path
import subprocess, json
root=Path('/Users/mac/Documents/英语学习/english-practice/chengdu-pandas-learning')
out=root/'.hyperframes/subtitle-build'
ff='/Users/mac/Documents/英语学习/english-practice/.tools/ffmpeg-subtitles'
src='/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/full-video-English.mp4'
srt=str(root/'assets/source.en.srt')
video=f"[0:v:0]trim=start=22.64:end=218.08,setpts=PTS-STARTPTS,subtitles=filename='{srt}':force_style='FontName=Arial,FontSize=18,Outline=1,Shadow=0,MarginV=18,WrapStyle=2',format=yuv420p[v]"
audio='[0:a:0]atrim=start=22.64:end=218.08,asetpts=PTS-STARTPTS[a]'
cmd=[ff,'-y','-hide_banner','-i',src,'-filter_complex',video+';'+audio,'-map','[v]','-map','[a]','-t','195.44','-c:v','libx264','-crf','22','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(root/'assets/source.new.mp4')]
(out/'render-command.json').write_text(json.dumps(cmd,indent=2))
with (out/'render.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=log)
print('Video encoding exit:',r.returncode)
if r.returncode:raise SystemExit(r.returncode)
(root/'assets/source.new.mp4').replace(root/'assets/source.mp4')
print('Atomic replacement complete.')
