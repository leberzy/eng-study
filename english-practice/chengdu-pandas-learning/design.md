# Design
Concept: 复杂句按意思拆成中英对照的小块，重点词在英文和对应中文中加粗，像一页清晰的语境笔记。

## Palette
Paper #F4F2E6; Ink #163E32; Muted ink #416457; Rule #CFD6C6.

## Typography
English Montserrat 500, bold800. Chinese LearnCN (Noto Sans SC, new chapter-specific glyph subset)400, bold800. Header600. English39px/1.3, Chinese28px/1.5, vocabulary24px/1.35, structure note22px (third card20px).

## Layout
1280x720. Header x128 y80. Three or two bilingual clause pairs x128 y159, width1024, gap22px. Vocabulary from y521, spacing10px. Note y628 (third card650). Flat, no shadow or cards, square rules. Key text in10% safe box, note in5% safe box.

## Motion
Only 0.3s opacity entrance on inner content via deterministic GSAP fromTo; each page holds5 seconds for reading. No progress line, no tracking of speech or reading, no additional animations.

## Avoid
No voice replays, read/listen/repeat prompts, exercises, timers, replacement sentences, typewriter, music, gradient, unrelated decoration.

New chapter preserves the approved hierarchy; sentence count and page count follow the content, not a fixed limit. Long English clauses use natural wrapping or block line wrappers at meaning boundaries, without br markup.
