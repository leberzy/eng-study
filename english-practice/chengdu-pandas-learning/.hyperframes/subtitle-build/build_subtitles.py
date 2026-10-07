from pathlib import Path
import json, re, textwrap, difflib
ROOT=Path('/Users/mac/Documents/英语学习/english-practice/chengdu-pandas-learning')
OUT=ROOT/'.hyperframes/subtitle-build'
START,END=22.64,218.08
j=json.loads(Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/source/word-timing.en.json3').read_text())
raw=[]
for event in j['events']:
 if event.get('aAppend'):continue
 for seg in event.get('segs',[]):
  t=(event['tStartMs']+seg.get('tOffsetMs',0))/1000
  text=seg['utf8'].strip()
  if text and START<=t<END:raw.append({'text':text,'original':text,'start':t,'event_end':(event['tStartMs']+event.get('dDurationMs',0))/1000})
raw.sort(key=lambda x:x['start'])
fixes={'chenu':'Chengdu','thead':'there','G':'grams','run':'runt','wi':'wild'}
corrections=[]
for i,w in enumerate(raw):
 text=w['text']
 if text in fixes:
  w['text']=fixes[text];corrections.append({'time':w['start'],'from':text,'to':w['text']})
 if text=='very' and 45<w['start']<47:
  w['text']='[unclear]';corrections.append({'time':w['start'],'from':text,'to':'[unclear]'})
 if text in ['Chang','Chong']:
  w['text']='[name';raw[i+1]['text']='unclear]';corrections.append({'time':w['start'],'from':text+' '+raw[i+1]['original'],'to':'[name unclear]'})
def toks(text):return re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?",text.lower())
words=[]
for w in raw:
 for token in toks(w['text']):words.append({**w,'token':token})
cues=[line.strip() for line in (OUT/'cues.txt').read_text().splitlines() if line.strip()]
expected=[x for cue in cues for x in toks(cue)]
actual=[w['token'] for w in words]
if actual!=expected:
 print('\n'.join(difflib.unified_diff(actual,expected,fromfile='source',tofile='cues')))
 raise SystemExit('Token sequence mismatch')

manual_wraps={
"This is one of the famous places here in Chengdu.": ["This is one of the famous places", "here in Chengdu."],
"He is literally just sitting on his back, eating bamboo.": ["He is literally just sitting on his back,", "eating bamboo."],
"Can't get over how funny the pandas actually are.": ["Can't get over how funny", "the pandas actually are."],
"They literally look like the toys you buy in, like, the gift store, like, down there.": ["They literally look like the toys you buy", "in, like, the gift store, like, down there."],
"They're just brilliant. They're just like big, cuddly animals.": ["They're just brilliant.", "They're just like big, cuddly animals."],
"So, the panda behind me is called [name unclear].": ["So, the panda behind me is called", "[name unclear]."],
"And this was the smallest panda to ever be born.": ["And this was the smallest panda", "to ever be born."],
"Like, pick your phone up and think of a third of that weight,": ["Like, pick your phone up", "and think of a third of that weight,"],
"and that's how much this panda was when it was born.": ["and that's how much this panda was", "when it was born."],
"[name unclear] was actually the runt of the litter when she was born.": ["[name unclear] was actually", "the runt of the litter when she was born."],
"Here in Panda Valley, they're not just keeping them in captivity.": ["Here in Panda Valley,", "they're not just keeping them in captivity."],
"But it is very hard to reintroduce them to the wild": ["But it is very hard", "to reintroduce them to the wild"],
"because, obviously, they're very used to being fed here in captivity.": ["because, obviously, they're very used to", "being fed here in captivity."],
"but I think they look equally as fluffy and cute.": ["but I think they look", "equally as fluffy and cute."],
"which is pretty cool. I don't know where we're going to see them,": ["which is pretty cool. I don't know", "where we're going to see them,"],
"and it might actually be one of my new favorite animals.": ["and it might actually be", "one of my new favorite animals."],
"They look super fluffy, just like the giant pandas,": ["They look super fluffy,", "just like the giant pandas,"],
}

rows=[];idx=0
for cue in cues:
 n=len(toks(cue));group=words[idx:idx+n]
 start=group[0]['start']
 nxt=words[idx+n]['start'] if idx+n<len(words) else END
 last=group[-1]
 if cue=='[Music]':end=min(last['event_end'],nxt-.04)
 else:end=min(nxt-.04,max(last['start']+.2,min(last['event_end'],last['start']+.7)))
 end=max(start+.12,end)
 lines=manual_wraps.get(cue) or textwrap.wrap(cue,width=47,break_long_words=False,break_on_hyphens=False)
 assert " ".join(lines)==cue
 assert all(len(line)<=47 for line in lines)
 assert len(lines)<=2,(cue,lines)
 rows.append({'start':round(start-START,3),'end':round(min(END,end)-START,3),'absolute_start':start,'absolute_end':end,'text':cue,'lines':lines,'words':[{'word':w['text'],'start':w['start']-START} for w in group]})
 idx+=n
for i,row in enumerate(rows):
 if i+1<len(rows):row['end']=min(row['end'],rows[i+1]['start'])
 row['cps']=round(len(row['text'])/(row['end']-row['start']),1)
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
(ROOT/'assets/source.en.srt').write_text('\n\n'.join(f'{i}\n{stamp(r["start"])} --> {stamp(r["end"])}\n'+ '\n'.join(r['lines']) for i,r in enumerate(rows,1))+'\n',encoding='utf-8')
(OUT/'alignment.json').write_text(json.dumps({'start':START,'end':END,'duration':END-START,'corrections':corrections,'cues':rows},ensure_ascii=False,indent=2))
print('Aligned',len(rows),'cues and',len(words),'tokens; max line length',max(len(line) for r in rows for line in r['lines']))
print('Fast cues (>25 CPS):',[(r['start'],r['text'],r['cps']) for r in rows if r['cps']>25])
print('Final cue',rows[-1])
