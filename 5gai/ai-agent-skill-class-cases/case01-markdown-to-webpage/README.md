# 案例 1：Markdown 课程笔记转网页

本案例的目标是把 `source/` 文件夹中的课程笔记转换成一个适合学生阅读的静态网页。

要求最终生成：

- `output/index.html`
- `output/style.css`
- `output/app.js`
- `output/README.md`

本案例需要分别尝试三种方式：

1. 直接和 AI 聊天，让 AI 生成网页代码；
2. 使用 Agent，让它读取文件夹、分析需求并生成文件；
3. 先撰写一个 Markdown-to-Webpage Skill，再让 Agent 根据 Skill 生成网页。
