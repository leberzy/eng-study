# Design

Concept: 复杂句按意思拆成中英对照的小块，重点词在英文和对应中文中加粗，像一页清晰的语境笔记。

## Palette

Paper #F4F2E6; Ink #163E32; Muted ink #416457; Rule #CFD6C6.

## Typography

English Montserrat 500, bold 800. Chinese LearnCN (Noto Sans SC, chapter-specific glyph subset) 400, bold 800. Header 600. English 39px/1.3, Chinese 28px/1.5, vocabulary 24px/1.35, compact three-pair page English 33px and Chinese 24px.

## Layout

1280 × 720. Header x128 y80. Two bilingual clause pairs x128 y159, width 1024, gap22px. Three-pair pages use a smaller 33/24px hierarchy and tighter gap. Vocabulary from y521, three-word pages from y496. Notes at y628 or y646. Flat, no shadow, cards or gradient.

## Motion

Only a 0.3s opacity entrance on inner content via deterministic GSAP fromTo; each page holds 5 seconds for reading. No progress line, tracking, replay, read-along prompts, typewriter, music or additional animations.
