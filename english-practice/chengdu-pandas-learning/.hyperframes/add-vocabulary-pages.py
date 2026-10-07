import hashlib
import json
import re
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

PROJECT = Path(__file__).resolve().parents[1]
ORIGINAL = PROJECT / 'assets/fonts/NotoSansSC.ttf'
FONT_OUT = PROJECT / 'assets/fonts/NotoSansSC-pandas.woff2'
GROUPS = [
    {
        'title': '熊猫谷生词 · 地点与语气',
        'words': [
            ('Valley', '山谷；Panda Valley 是“熊猫谷”。'),
            ('Corner', '拐角；around this corner = 前面拐角处。'),
            ('Literally', '口语中加强语气：真的、简直。'),
        ],
    },
    {
        'title': '熊猫谷生词 · 熊猫印象',
        'words': [
            ('Bamboo', '竹子；熊猫会吃竹子。'),
            ('Brilliant', '很棒、太有趣了；这里形容熊猫。'),
            ('Cuddly', '软乎乎、让人很想抱的。'),
        ],
    },
    {
        'title': '熊猫谷生词 · 野外与圈养',
        'words': [
            ('Runt', '一窝中最小或最弱的幼崽。'),
            ('Wild', '野外；in the wild = 在野外。'),
            ('Captivity', '圈养状态；in captivity = 在圈养环境中。'),
        ],
    },
    {
        'title': '熊猫谷生词 · 训练与保护',
        'words': [
            ('Train', '训练；train them up = 训练它们。'),
            ('Giant', 'giant panda = 大熊猫；giant 意为“巨大的”。'),
            ('Extinct', '灭绝；go extinct = 灭绝。'),
        ],
    },
    {
        'title': '熊猫谷生词 · 放归与生存',
        'words': [
            ('Reintroduction', '重新放归野外；这里指把熊猫放回自然环境。'),
            ('Starve', '挨饿、饿死；starve to death = 饿死。'),
            ('Fluffy', '毛茸茸的、蓬松的。'),
        ],
    },
    {
        'title': '熊猫谷生词 · 外形与关注',
        'words': [
            ('Cute', '可爱的。'),
            ('Fuss', '这里指关注、追捧；get as much fuss = 得到那么多关注。'),
            ('Himalayas', '喜马拉雅山脉。'),
        ],
    },
    {
        'title': '熊猫谷生词 · 物种与食物',
        'words': [
            ('Species', '物种；单数和复数写法相同。'),
            ('Diet', '日常饮食、食物构成；这里指熊猫的食谱。'),
            ('Treat', '特别的小零食或加餐；这里指熊猫吃的苹果。'),
        ],
    },
]
PAGE_START = 10
BASE_TIME = 245.44
PAGE_DURATION = 5
PAGE_COUNT = PAGE_START + len(GROUPS)
TOTAL_DURATION = BASE_TIME + len(GROUPS) * PAGE_DURATION

# Allocate compact, stable HyperFrames IDs that do not collide with current project IDs.
existing = set(re.findall(r'data-hf-id="(hf-[a-z0-9]+)"', (PROJECT / 'index.html').read_text()))
for f in (PROJECT / 'compositions').glob('*.html'):
    existing.update(re.findall(r'data-hf-id="(hf-[a-z0-9]+)"', f.read_text()))
def hf_id(label):
    n = 0
    while True:
        candidate = 'hf-' + hashlib.sha256(f'{label}:{n}'.encode()).hexdigest()[:4]
        if candidate not in existing:
            existing.add(candidate)
            return candidate
        n += 1

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

all_added_text = ''
for offset, group in enumerate(GROUPS, 1):
    num = PAGE_START + offset
    slug = f'pandas-vocab-{offset:02d}'
    root_id = f'{slug}-root'
    content_id = f'{slug}-content'
    entries = []
    for word, meaning in group['words']:
        entries.append(
            f'<div class="entry"><p class="english"><b>{esc(word)}</b></p>'
            f'<p class="chinese">{esc(meaning)}</p></div>'
        )
    all_added_text += group['title'] + ''.join(w + m for w, m in group['words'])
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"></head><body><template><style>
@font-face{{font-family:LearnCN;src:url("assets/fonts/NotoSansSC-pandas.woff2") format("woff2");font-weight:100 900;font-style:normal;font-display:block}}
@font-face{{font-family:Montserrat;src:url("assets/fonts/Montserrat.ttf") format("truetype");font-weight:100 900;font-style:normal;font-display:block}}
*{{box-sizing:border-box}}
#{root_id}{{position:absolute;inset:0;width:1280px;height:720px;background:#F4F2E6;color:#163E32;font-family:LearnCN,sans-serif}}
.content{{position:absolute;inset:0}}
.header{{position:absolute;left:128px;right:128px;top:80px;display:flex;justify-content:space-between;align-items:center;font-size:25px;font-weight:600}}
.count{{font-family:Montserrat,sans-serif;font-size:24px;color:#416457;font-weight:600}}
.entries{{position:absolute;left:128px;top:168px;width:1024px;display:flex;flex-direction:column;gap:29px}}
.english{{font-family:Montserrat,sans-serif;font-weight:500;font-size:32px;line-height:1.25;margin:0;letter-spacing:-.3px}}
.chinese{{font-size:25px;line-height:1.4;margin:5px 0 0!important;font-weight:400;color:#416457}}
b{{font-weight:800;color:#163E32}}
</style><div data-hf-id="{hf_id(slug+'-root')}" id="{root_id}" data-composition-id="{slug}" data-width="1280" data-height="720" data-duration="5">
<div data-hf-id="{hf_id(slug+'-content')}" id="{content_id}" class="content">
<div class="header"><span>{esc(group['title'])}</span><span class="count">{num:02d} / {PAGE_COUNT:02d}</span></div>
<div class="entries">{''.join(entries)}</div></div></div>
<script>{{const tl=gsap.timeline({{paused:true}});tl.fromTo("#{content_id}",{{opacity:0}},{{opacity:1,duration:.3,ease:"power1.out"}},0);window.__timelines=window.__timelines||{{}};window.__timelines["{slug}"]=tl;}}</script>
</template></body></html>'''
    (PROJECT / 'compositions' / f'{slug}.html').write_text(html)

# Extend main composition with seven final 5-second vocabulary pages.
main_path = PROJECT / 'index.html'
main = main_path.read_text()
main = main.replace('data-duration="245.44"', f'data-duration="{TOTAL_DURATION:.2f}"', 1)
mounts = []
for i in range(1, len(GROUPS) + 1):
    page = PAGE_START + i
    slug = f'pandas-vocab-{i:02d}'
    start = BASE_TIME + (i - 1) * PAGE_DURATION
    mounts.append(
        f'<div data-hf-id="{hf_id(slug+"-mount")}" id="mount-{slug}" class="clip" '
        f'data-composition-id="{slug}" data-composition-src="compositions/{slug}.html" '
        f'data-start="{start:.2f}" data-duration="5" data-track-index="1" data-track-kind="graphics" '
        f'data-width="1280" data-height="720"></div>'
    )
insert_at = main.rfind('</div>', 0, main.index('<script>window.__timelines'))
main = main[:insert_at] + ''.join(mounts) + main[insert_at:]
main_path.write_text(main)

# Add printable/downloadable page data for the vocabulary cards.
pages_path = PROJECT / 'learning-pages.json'
pages = json.loads(pages_path.read_text())
for i, group in enumerate(GROUPS, 1):
    pages.append({'id': f'pandas-vocab-{i:02d}', 'kind': 'vocabulary', 'title': group['title'], 'words': [list(x) for x in group['words']]})
pages_path.write_text(json.dumps(pages, ensure_ascii=False, indent=2) + '\n')

# Regenerate the Chinese glyph subset from the original source so new cards cannot show missing glyphs.
chars_path = PROJECT / 'assets/fonts/NotoSansSC-pandas-characters.txt'
chars = set(chars_path.read_text()) | set(all_added_text)
char_text = ''.join(sorted(chars))
chars_path.write_text(char_text)
font = TTFont(ORIGINAL)
opts = subset.Options()
opts.flavor = 'woff2'
opts.name_IDs = [0, 1, 2, 3, 4, 5, 6]
opts.name_legacy = True
opts.notdef_glyph = True
opts.notdef_outline = True
opts.recommended_glyphs = True
subsetter = subset.Subsetter(options=opts)
subsetter.populate(text=char_text)
subsetter.subset(font)
font.flavor = 'woff2'
font.save(FONT_OUT)
font_check = TTFont(FONT_OUT)
coverage = set(font_check.getBestCmap())
missing = sorted(ord(ch) for ch in char_text if ord(ch) not in coverage)
if missing:
    raise RuntimeError(f'missing glyphs: {missing}')

# Describe the full 17-page storyboard and the longer exported runtime.
story_path = PROJECT / 'STORYBOARD.md'
story = story_path.read_text()
story = story.replace('duration: 245.44s', f'duration: {TOTAL_DURATION:.2f}s', 1)
story += '\n\n## 生词片尾页\n'
for i, group in enumerate(GROUPS, 1):
    page = PAGE_START + i
    start = BASE_TIME + (i - 1) * PAGE_DURATION
    words = '、'.join(word for word, _ in group['words'])
    story += f'\n### 第{page:02d}页 · {group["title"]}\n- src: compositions/pandas-vocab-{i:02d}.html\n- 时间：{start:.2f}–{start+PAGE_DURATION:.2f}秒，5秒\n- 生词：{words}\n'
story_path.write_text(story)

brief_path = PROJECT / 'BRIEF.md'
brief = brief_path.read_text()
brief += '\n\n## 生词补充\n用户指出21个生词需加入视频片尾。新增7页，每页3词、5秒，接在10页复杂句卡片之后；无配音，沿用已确认样式。\n'
brief_path.write_text(brief)

print(json.dumps({'page_count': PAGE_COUNT, 'new_pages': len(GROUPS), 'duration': TOTAL_DURATION, 'font_bytes': FONT_OUT.stat().st_size, 'font_characters': len(char_text), 'missing_glyphs': len(missing)}, ensure_ascii=False))
