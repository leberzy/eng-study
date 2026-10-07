from pathlib import Path
import json
import subprocess

ROOT = Path('/Users/mac/Documents/英语学习/english-practice/chengdu-folk-music-learning')
source = ROOT / 'assets/fonts/NotoSansSC.ttf'
pages = json.loads((ROOT / 'learning-pages.json').read_text(encoding='utf-8'))
notes = (ROOT / 'learning-notes.md').read_text(encoding='utf-8')
text = json.dumps(pages, ensure_ascii=False) + notes
text += '复杂句解析中国民乐片尾页地点期待回忆环境体验细节评价历史开放第章重点词语含义'
text += '0123456789/·，。、“”‘’：；（）！…—-'
chars = ''.join(sorted(set(ch for ch in text if ord(ch) < 0x10000)))
(ROOT / 'assets/fonts/NotoSansSC-folk-characters.txt').write_text(chars, encoding='utf-8')
output = ROOT / 'assets/fonts/NotoSansSC-folk.woff2'
command = [
    'pyftsubset', str(source), f'--text-file={ROOT / "assets/fonts/NotoSansSC-folk-characters.txt"}',
    f'--output-file={output}', '--flavor=woff2', '--layout-features=*', '--glyph-names',
]
subprocess.run(command, check=True)
print(f'Created {output} with {len(chars)} characters ({output.stat().st_size} bytes).')
