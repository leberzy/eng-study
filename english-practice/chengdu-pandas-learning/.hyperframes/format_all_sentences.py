from pathlib import Path
import re


PROJECT = Path('/Users/mac/Documents/英语学习/english-practice/chengdu-pandas-learning')
SOURCE_MD = Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/clips/02-pandas-English.md')
SOURCE_SRT = PROJECT / 'assets/source.en.srt'
OUTPUT = PROJECT / 'learning-notes-all.md'


def parse_srt(path: Path):
    cues = []
    for block in path.read_text(encoding='utf-8').split('\n\n'):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        match = re.match(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> '
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3})',
            lines[1],
        )
        if not match:
            continue
        start = (
            int(match.group(1)) * 3600
            + int(match.group(2)) * 60
            + int(match.group(3))
            + int(match.group(4)) / 1000
        )
        cues.append((start, ' '.join(lines[2:])))
    return cues


def clean_markup(text: str) -> str:
    return text.replace('**', '').strip()


def tokens(text: str):
    text = clean_markup(text).lower().replace('…', '...')
    text = text.replace('[unclear name: "chang lang"]', '[name unclear]')
    text = text.replace('[unclear name: "chong low"]', '[name unclear]')
    return re.sub(r'[^a-z0-9%]+', ' ', text).split()


def parse_pairs(path: Path):
    lines = path.read_text(encoding='utf-8').splitlines()
    timestamp_re = re.compile(r'^\*\*(\d{2}):(\d{2})\*\*$')
    pairs = []
    coarse_time = 0
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        timestamp = timestamp_re.match(line)
        if timestamp:
            coarse_time = int(timestamp.group(1)) * 60 + int(timestamp.group(2))
            index += 1
            continue
        if not line or line.startswith('#') or line.startswith('>') or line.startswith('重点：'):
            index += 1
            continue
        english = clean_markup(line)
        next_index = index + 1
        while next_index < len(lines) and not lines[next_index].strip():
            next_index += 1
        if next_index < len(lines) and lines[next_index].startswith('中文：'):
            chinese = clean_markup(lines[next_index][len('中文：'):])
            pairs.append({'english': english, 'chinese': chinese, 'coarse_time': coarse_time})
            index = next_index + 1
            continue
        index += 1
    return pairs


def find_start(pair, cues, cursor):
    wanted = tokens(pair['english'])
    candidates = []
    for cue_index in range(cursor, len(cues)):
        cue_tokens = tokens(cues[cue_index][1])
        best_overlap = 0
        for length in range(min(8, len(wanted)), 0, -1):
            for offset in range(0, len(cue_tokens) - length + 1):
                if wanted[:length] == cue_tokens[offset:offset + length]:
                    best_overlap = length
                    break
            if best_overlap:
                break
        if best_overlap:
            candidates.append((best_overlap, cue_index))
    if candidates:
        best_overlap = max(item[0] for item in candidates)
        cue_index = next(item[1] for item in candidates if item[0] == best_overlap)
        return cues[cue_index][0], cue_index
    # Names and the intentionally unclear fragment do not match the SRT text;
    # retain their existing approximate position in the clip.
    clip_seconds = max(0, pair['coarse_time'] - 22.64)
    return clip_seconds, cursor


def format_time(seconds: float) -> str:
    total = max(0, int(seconds))
    return f'{total // 60:02d}:{total % 60:02d}'


cues = parse_srt(SOURCE_SRT)
pairs = parse_pairs(SOURCE_MD)
cursor = 0
for pair in pairs:
    start, cue_index = find_start(pair, cues, cursor)
    pair['time'] = format_time(start)
    cursor = cue_index

lines = [
    '# 第二段 · 熊猫谷全句中英对照',
    '',
    '本文件覆盖当前熊猫谷视频中的全部英文语句和口语片段。时间以当前视频的 00:00 为起点；英文下面紧跟中文翻译，不标注重点词或难点词汇。',
    '',
]
for pair in pairs:
    lines.extend([
        pair['time'],
        '',
        pair['english'],
        '',
        pair['chinese'],
        '',
    ])

OUTPUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {len(pairs)} sentence pairs to {OUTPUT}')
