from pathlib import Path
import difflib
import json
import re

ROOT = Path('/Users/mac/Documents/英语学习/english-practice/chengdu-folk-music-learning')
DATA = Path('/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/source/word-timing.en.json3')
START = 218.08
END = 316.88


def tokens(text):
    return re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", text.lower())


# Keep the original spoken wording, including the omitted subject in “so quite
# excited” and the speaker's “a slight different movement”. Punctuation and
# line breaks are editorial aids for learners; they do not rewrite the audio.
cues = [
    ("We have just entered our next spot in the middle of Chengdu,",
     ["We have just entered our next spot", "in the middle of Chengdu,"]),
    ("and it's this beautiful scenic area.",
     ["and it's this beautiful scenic area."]),
    ("And I think, in a few minutes' time,",
     ["And I think, in a few minutes' time,"]),
    ("we're going to be able to see some Chinese folk music.",
     ["we're going to be able to see some Chinese folk", "music."]),
    ("Now, I never saw Chinese folk music on my first trip,",
     ["Now, I never saw Chinese folk music on my first", "trip,"]),
    ("so quite excited to see it here.",
     ["so quite excited to see it here."]),
    ("[Music]", ["[Music]"]),
    ("The instruments make such a beautiful sound,",
     ["The instruments make such a beautiful sound,"]),
    ("and being surrounded by all these trees and this beautiful Chinese architecture, um,",
     ["and being surrounded by all these trees", "and this beautiful Chinese architecture, um,"]),
    ("in this area just, like, adds to that atmosphere.",
     ["in this area just, like, adds to that", "atmosphere."]),
    ("Chinese folk music takes a...", ["Chinese folk music takes a..."]),
    ("[Music]", ["[Music]"]),
    ("turn. 1, 2, 3, 4!", ["turn. 1, 2, 3, 4!"]),
    ("[Music]", ["[Music]"]),
    ("Okay, that was so awesome.", ["Okay, that was so awesome."]),
    ("So, after the music, we were able to try and, like, play",
     ["So, after the music, we were able to try and,", "like, play"]),
    ("the instruments, and that, like, violin",
     ["the instruments, and that, like, violin"]),
    ("kind of thing was incredible.", ["kind of thing was incredible."]),
    ("You have to be so delicate on all the strings",
     ["You have to be so delicate on all the strings"]),
    ("because a slight different movement,", ["because a slight different movement,"]),
    ("and it makes a completely different sound.",
     ["and it makes a completely different sound."]),
    ("Very confusing, but yeah, good", ["Very confusing, but yeah, good"]),
    ("[Music]", ["[Music]"]),
    ("fun. This beautiful scenic area is",
     ["fun. This beautiful scenic area is"]),
    ("actually a thousand years old,", ["actually a thousand years old,"]),
    ("and it used to be a private land, a private park.",
     ["and it used to be a private land,", "a private park."]),
    ("It wasn't open to the public, but it was",
     ["It wasn't open to the public, but it was"]),
    ("owned by the government,", ["owned by the government,"]),
    ("and the government were able to come around",
     ["and the government were able to come around"]),
    ("and just relax in this beautiful",
     ["and just relax in this beautiful"]),
    ("[Music]", ["[Music]"]),
    ("area.", ["area."]),
]


def stamp(seconds):
    ms = round(seconds * 1000)
    hours, ms = divmod(ms, 3_600_000)
    minutes, ms = divmod(ms, 60_000)
    seconds, millis = divmod(ms, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{millis:03}'


events = json.loads(DATA.read_text(encoding='utf-8'))['events']
raw = []
for event in events:
    event_start = event.get('tStartMs', 0) / 1000
    event_end = (event.get('tStartMs', 0) + event.get('dDurationMs', 0)) / 1000
    for seg in event.get('segs', []):
        text = seg.get('utf8', '').strip()
        if not text:
            continue
        t = (event.get('tStartMs', 0) + seg.get('tOffsetMs', 0)) / 1000
        if START <= t < END:
            clean = {'text': text, 'start': t, 'event_end': event_end}
            if text.lower() == 'changu':
                clean['text'] = 'Chengdu'
            elif text.lower() == 'scenic':
                clean['text'] = 'scenic'
            elif text.lower() == 'era':
                clean['text'] = 'area'
            raw.append(clean)
raw.sort(key=lambda item: item['start'])

actual = [token for word in raw for token in tokens(word['text'])]
expected = [token for text, _ in cues for token in tokens(text)]
if actual != expected:
    diff = '\n'.join(difflib.unified_diff(actual, expected, fromfile='source', tofile='cues', lineterm=''))
    raise SystemExit(f'Token sequence mismatch:\n{diff}')

rows = []
cursor = 0
for text, lines in cues:
    count = len(tokens(text))
    group = raw[cursor:cursor + count]
    cursor += count
    start = group[0]['start'] - START
    rows.append({'text': text, 'lines': lines, 'start': start, 'source_start': group[0]['start']})

for index, row in enumerate(rows):
    if index + 1 < len(rows):
        end = rows[index + 1]['start'] - 0.04
    else:
        end = END - START - 0.04
    row['end'] = max(row['start'] + 0.12, min(END - START, end))

srt = []
for index, row in enumerate(rows, 1):
    srt.append(f"{index}\n{stamp(row['start'])} --> {stamp(row['end'])}\n" + '\n'.join(row['lines']))
(ROOT / 'assets/source.en.srt').write_text('\n\n'.join(srt) + '\n', encoding='utf-8')
(ROOT / '.hyperframes/subtitle-build/alignment.json').write_text(
    json.dumps({'start': START, 'end': END, 'duration': END - START, 'cues': rows}, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)
print(f'Built {len(rows)} cues, {len(raw)} timed words, duration {END - START:.2f}s.')
print(f'Max line length: {max(len(line) for _, lines in cues for line in lines)}')
