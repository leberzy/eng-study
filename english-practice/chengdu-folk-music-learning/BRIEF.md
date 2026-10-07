---
workflow: general-video
flow: automation
storyboard: no
message: "通过中国民乐原片及复杂句中英对照，帮助初学者理解本章英语。"
aspect: 1280x720
language: en-zh
audience: 中文母语英语初学者及观看视频的粉丝
length: source-duration-plus-pages-times-5s
voice: source-audio
---

## Intent

第三章中国民乐，严格使用上级英语学习视频制作规范 v1.2。沿用已确认的复杂句解析版式；页数按内容决定，每页 5 秒。

## Assets

- 本地全视频：/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/full-video-English.mp4。
- 本地词级时间：/Users/mac/Documents/英语学习/media/Chengdu-English-Practice/source/word-timing.en.json3，用于本章字幕标点、断句和完整句切点。
- 本地字体和 GSAP：assets/fonts、lib/gsap.min.js。

## Customizations

- 原片保留原声并烧录带标点英文字幕，每次最多两行。
- 片尾每个英文分句紧接中文；重点词及对应中文加粗，配语境词义。
- 仅 0.3 秒内容淡入，静音阅读页；无跟读、重播、配音、练习、计时或音乐。

## Chapter boundaries

使用词级时间核实的本章范围 218.08–316.88 秒，原片 98.80 秒。结尾保留完整的 “area”，下一章从 “we have just arrived…” 开始。

## Pages

本章选取 10 个原句，按语义拆成 12 页，片尾 60 秒，完整预览预计 158.80 秒。
