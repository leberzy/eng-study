# 我的英语学习资料

统一保存个人生词本、旅行视频的中英对照稿、英文字幕和可编辑视频项目。

## 日常学习

- [全局生词本](全局生词本.md)：按学习日期整理，保存中文意思、语境、出处和复习记录。
- [生词本使用说明](使用说明.md)：收录、去重与复习规则。
- [成都旅行学习目录](media/Chengdu-English-Practice/学习目录.md)：各章节视频与学习文案。
- [英语学习视频制作规范](english-practice/英语学习视频制作规范.md)：字幕、复杂句学习片尾及验收要求。
- [熊猫谷全句对照稿](english-practice/chengdu-pandas-learning/learning-notes-all.md)：按当前视频时间排列的全句中英对照。

## 目录

```text
英语学习/
├── 全局生词本.md
├── 使用说明.md
├── english-practice/          # 文案、字幕、HyperFrames 项目与本地素材
├── media/
│   └── Chengdu-English-Practice/
│       ├── source/            # 原始字幕、逐词时间等资料
│       ├── clips/             # 章节视频与对应文案
│       └── preview/           # 已导出成片、学习文案和英文字幕
└── docs/                     # 管理与迁移记录
```

## Git 保存范围

Git 保存生词本、复习记录、中英文案、字幕、章节时间、制作规范、项目 HTML/JSON/脚本以及字体授权说明。

视频、音频、字体文件、渲染截图与缓存、工具可执行文件保存在本地，由 `.gitignore` 排除。Gitee 中的代码仓库不包含这些素材；换电脑时需要单独复制素材或按来源重新获取。

本目录是独立 Git 仓库，远程为 [Gitee · english-study](https://gitee.com/leberzy/english-study)，SSH 地址为 `git@gitee.com:leberzy/english-study.git`，主分支为 `main`。

日常可以用 `git status` 查看变化，`git add` 和 `git commit` 保存修改；用户明确要求推送时再执行 `git push`。

## 迁移兼容

此前 `/Users/mac/Documents/misc/english-practice` 和 `/Users/mac/Downloads/Chengdu-English-Practice` 保留为指向本目录的符号链接，旧对话中的文件链接仍可使用。后续新资料统一写入本目录。
