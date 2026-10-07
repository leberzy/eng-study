# 英语学习独立目录与 Git 管理 Implementation Plan

> **For agentic workers:** Steps use checkbox (`- [ ]`) syntax for tracking. This is a reversible directory migration, not a feature implementation; execute inline and verify file preservation. A read-only subagent reviews the Git ignore boundaries.

**Goal:** 将生词本、英语学习项目和视频资料集中到独立目录，建立本地 Git 仓库，并在用户提供 Gitee 地址后推送。

**Architecture:** `/Users/mac/Documents/英语学习` 作为唯一资料根目录。既有视频项目放入 `english-practice/`，已下载资料放入 `media/Chengdu-English-Practice/`。旧路径保留符号链接，原有文件不删除。

**Tech Stack:** Markdown、Python、Git；现有 HyperFrames 项目保持可编辑。

## Global Constraints

- 用户请求 Git 管理并推送 Gitee，必须先取得准确的仓库地址。
- 不覆盖已有远程历史，不强制推送，不提交凭据。
- 视频、音频、字体二进制、渲染缓存和工具可执行文件留在本地；学习资料、字幕和项目源码纳入 Git。
- 保留按日分组的生词记录；迁移不改变视频、字幕或学习内容。

## Task 1: 本地迁移

- [x] 记录旧目录文件清单和 SHA-256，保存到被 Git 忽略的 `.local/`。
- [x] 将混合目录中的 `english-practice/` 移入新根目录，旧路径创建符号链接。
- [x] 将下载目录中的 `Chengdu-English-Practice/` 移入新根目录的 `media/`，旧路径创建符号链接。
- [x] 更新本项目文本中的绝对路径，核验文件数量、非文本文件哈希及旧链接。

## Task 2: Git 管理

- [x] 创建根目录 `README.md`、`AGENTS.md` 和 `.gitignore`。
- [x] 执行 `git init -b main`；确认待提交文件仅包括英语学习资料，不含媒体大文件、缓存、凭据。
- [x] 创建首次本地提交，确认工作区干净。

## Task 3: Gitee 推送

- [x] 用户提供准确仓库地址后，检查远程状态及当前机器访问权限。`git@gitee.com:leberzy/english-study.git` 可通过 SSH 访问，首次检查为空仓库。
- [x] 空仓库直接配置 origin 并推送；非空仓库先检查并保留既有历史。已建立 `main` 并设置 upstream，未使用强制推送。
- [x] 首次推送返回成功，远程建立 `main`。最终补充本迁移说明后再次推送，并以远程 ref 与本地 HEAD 的一致性作为交付检查。
