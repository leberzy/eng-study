from pathlib import Path
import html
import json

ROOT = Path('/Users/mac/Documents/英语学习/english-practice/chengdu-folk-music-learning')
pages = json.loads((ROOT / 'learning-pages.json').read_text(encoding='utf-8'))
source_duration = 98.8
page_duration = 5
total_duration = source_duration + len(pages) * page_duration

style = '''
@font-face{font-family:LearnCN;src:url("assets/fonts/NotoSansSC-folk.woff2") format("woff2");font-weight:100 900;font-style:normal;font-display:block}
@font-face{font-family:Montserrat;src:url("assets/fonts/Montserrat.ttf") format("truetype");font-weight:100 900;font-style:normal;font-display:block}
*{box-sizing:border-box}.content{position:absolute;inset:0}.header{position:absolute;left:128px;right:128px;top:80px;display:flex;justify-content:space-between;align-items:center;font-size:25px;font-weight:600}.count{font-family:Montserrat,sans-serif;font-size:24px;color:#416457;font-weight:600}.pairs{position:absolute;left:128px;top:159px;width:1024px;display:flex;flex-direction:column;gap:22px}.pairs.three{top:146px;gap:12px}.pair p{margin:0}.english{font-family:Montserrat,sans-serif;font-weight:500;font-size:39px;line-height:1.3;letter-spacing:-.5px}.chinese{font-size:28px;line-height:1.5;margin-top:5px!important;font-weight:400;color:#416457}.pairs.three .english{font-size:33px;line-height:1.24}.pairs.three .chinese{font-size:24px;line-height:1.38}.pairs.three .pair p{margin:0}.pairs.three .chinese{margin-top:3px!important}b{font-weight:800;color:#163E32}.lexicon{position:absolute;left:128px;right:128px;top:521px;border-top:2px solid #CFD6C6;padding-top:22px;display:flex;flex-direction:column;gap:10px;font-size:24px;line-height:1.35;color:#416457}.lexicon.compact{top:496px;gap:7px}.wordrow{display:flex;align-items:baseline;gap:18px}.wordrow b{font-family:Montserrat,sans-serif;font-weight:800}.note{position:absolute;left:128px;right:128px;top:628px;font-size:20px;line-height:1.4;color:#416457;margin:0}.note.compact{top:646px}
''' 

for index, page in enumerate(pages, 1):
    page_id = page['id']
    pairs = page['pairs']
    words = page['words']
    pair_class = 'pairs three' if len(pairs) >= 3 else 'pairs'
    lex_class = 'lexicon compact' if len(words) >= 3 else 'lexicon'
    note_class = 'note compact' if len(words) >= 3 else 'note'
    pair_html = []
    for pair_index, (english, chinese) in enumerate(pairs, 1):
        pair_html.append(
            f'<div class="pair" id="{page_id}-pair-{pair_index}">'
            f'<p class="english">{english}</p><p class="chinese">{chinese}</p></div>'
        )
    words_html = ''.join(
        f'<div class="wordrow"><b>{html.escape(word)}</b><span>{html.escape(meaning)}</span></div>'
        for word, meaning in words
    )
    note = html.escape(page['note'])
    source = html.escape(page['source_sentence'])
    document = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"></head><body><template><style>
{style}
#{page_id}-root{{position:absolute;inset:0;width:1280px;height:720px;background:#F4F2E6;color:#163E32;font-family:LearnCN,sans-serif}}
</style><div id="{page_id}-root" data-composition-id="{page_id}" data-width="1280" data-height="720" data-duration="5">
<div class="content" id="{page_id}-content"><div class="header"><span>复杂句解析 · {html.escape(page['title'])}</span><span class="count">{index:02} / {len(pages):02}</span></div>
<div class="{pair_class}" data-source="{source}">{''.join(pair_html)}</div>
<div class="{lex_class}">{words_html}</div><p class="{note_class}">{note}</p></div></div>
<script>{{const tl=gsap.timeline({{paused:true}});tl.fromTo("#{page_id}-content",{{opacity:0}},{{opacity:1,duration:.3,ease:"power1.out"}},0);window.__timelines=window.__timelines||{{}};window.__timelines["{page_id}"]=tl;}}</script>
</template></body></html>'''
    (ROOT / 'compositions' / f'{page_id}.html').write_text(document, encoding='utf-8')

hosts = []
for index, page in enumerate(pages):
    page_id = page['id']
    start = source_duration + index * page_duration
    hosts.append(
        f'<div id="mount-{page_id}" class="clip" data-composition-id="{page_id}" '
        f'data-composition-src="compositions/{page_id}.html" data-start="{start:.2f}" '
        f'data-duration="5" data-track-index="1" data-track-kind="graphics" data-width="1280" data-height="720"></div>'
    )
index_html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1280,height=720"><script src="lib/gsap.min.js"></script><style>
*{{box-sizing:border-box}}html,body{{margin:0;padding:0;width:1280px;height:720px;overflow:hidden;background:#F4F2E6}}#root{{position:relative;width:1280px;height:720px}}#source-video{{position:absolute;inset:0;width:1280px;height:720px;object-fit:contain}}[data-composition-src]{{position:absolute;inset:0;width:1280px;height:720px}}
</style></head><body><div id="root" data-composition-id="main" data-width="1280" data-height="720" data-duration="{total_duration:.2f}">
<video id="source-video" class="clip" src="assets/source.mp4" data-has-audio="true" playsinline data-start="0" data-duration="{source_duration:.2f}" data-track-index="0" data-volume="1"></video>
{''.join(hosts)}
</div><script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script></body></html>'''
(ROOT / 'index.html').write_text(index_html, encoding='utf-8')
print(f'Wrote {len(pages)} pages; composition duration {total_duration:.2f}s.')
