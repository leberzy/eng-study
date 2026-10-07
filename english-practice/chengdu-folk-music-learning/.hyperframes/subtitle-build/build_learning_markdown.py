from pathlib import Path
import json
import re

ROOT = Path('/Users/mac/Documents/英语学习/english-practice/chengdu-folk-music-learning')
pages = json.loads((ROOT / 'learning-pages.json').read_text(encoding='utf-8'))


def markdown_bold(text: str) -> str:
    return re.sub(r'<b>(.*?)</b>', r'**\1**', text)


lines = [
    '# 第三段 · 中国民乐复杂句中英对照',
    '',
    '原片约1分39秒，片尾12页，每页5秒，共60秒。下列时间为本段片段内时间，用于找到对应语境。',
    '',
]

for index, page in enumerate(pages, 1):
    lines.extend([
        f"## {index}. {page['title']}",
        '',
        f"片段内时间：{page['source_time_hint']}",
        '',
    ])
    for english, chinese in page['pairs']:
        lines.extend([markdown_bold(english), '', markdown_bold(chinese), ''])
    words = '；'.join(
        f"**{word}**：{meaning}" for word, meaning in page['words']
    )
    lines.extend([
        f'重点词：{words}。',
        '',
        f"句子说明：{page['note']}",
        '',
    ])

lines.extend([
    '## 本段听辨说明',
    '',
    '- 原话中的 `so quite excited` 保留了口语省略；规范表达可以说 `so I\'m quite excited`。',
    '- 原话中的 `a slight different movement` 按视频保留；更自然的表达是 `a slightly different movement`。',
    '- `Chinese folk music takes a... [Music] turn` 中间被演奏声打断，字幕用省略号和 `[Music]` 保留这一听感。',
    '- 英文字幕已经补充句首大写、标点和语义断句，仍保留说话者的口语填充词。',
    '',
    '原视频：Joel and Emilia，[3 DAYS in CHENGDU - This CITY SURPRISED ME 🇨🇳](https://www.youtube.com/watch?v=UqmPUsnWg14)',
    '',
])

output = ROOT / '03-chinese-folk-music-Complex-Sentences.md'
output.write_text('\n'.join(lines), encoding='utf-8')
print(output)
