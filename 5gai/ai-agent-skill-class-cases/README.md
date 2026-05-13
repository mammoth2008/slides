# AI Agent Skill 课堂案例集

本目录用于《生成式人工智能与应用》课程中“人工智能辅助编程”部分的课堂练习。

核心主线是：

**聊天生成代码 → Agent 完成任务 → Skill 固化流程**

三个案例使用同一套比较框架：

1. 聊天生成：把需求直接发给 AI，一次性生成代码或方案；
2. Agent 生成：把材料放进项目目录，让 Agent 阅读、规划、生成、修改；
3. Skill + Agent：先写 `SKILL.md`，再让 Agent 按流程执行。

## 目录结构

```text
ai-agent-skill-class-cases/
  README.md
  case01-markdown-to-webpage/
  case02-data-report/
  case03-project-planning/
```

## 三个案例

### 案例 1：Markdown 转网页

目录：[case01-markdown-to-webpage](/Users/Freeman/Works/slides/5gai/ai-agent-skill-class-cases/case01-markdown-to-webpage)

主要教学点：

- 读取材料而不是只接收一段 prompt；
- 理解 Markdown 结构并整理层级；
- 生成多个前端文件；
- 检查目录、练习区、TODO 区是否完整。

最适合展示：

- Agent 的执行能力；
- 多文件输出能力；
- 从“生成一段 HTML”到“完成一个小任务”的升级。

### 案例 2：CSV 数据清洗与小报告

目录：[case02-data-report](/Users/Freeman/Works/slides/5gai/ai-agent-skill-class-cases/case02-data-report)

主要教学点：

- 数据质量检查；
- 标准化与异常保留；
- 问题清单记录；
- 基于真实计算生成报告。

最适合展示：

- Skill 的价值；
- 为什么流程约束比“看起来做完了”更重要；
- Agent 在“读数据、写脚本、运行、修复、输出报告”中的完整闭环。

### 案例 3：从模糊需求到项目计划

目录：[case03-project-planning](/Users/Freeman/Works/slides/5gai/ai-agent-skill-class-cases/case03-project-planning)

主要教学点：

- 需求如何先被澄清；
- 模糊目标如何拆成任务清单；
- 规划文档如何先于代码；
- MVP 如何按约束落地。

最适合展示：

- Agent 的规划能力；
- “先整理需求，再写代码”的工作方式；
- 人和 Agent 如何一起做取舍。

## 建议课堂顺序

### 第一：案例 3，讲规划

先让学生看到：

**不要一上来写代码，先把需求变成任务。**

课堂上至少完成：

- 需求摘要
- 任务拆解
- 文件结构
- 验收标准

### 第二：案例 1，讲多文件生成

然后展示：

**读取材料 → 理解结构 → 生成 HTML/CSS/JS → 检查输出**

这个案例最适合说明 Agent 为什么比普通聊天更适合做多文件任务。

### 第三：案例 2，讲 Skill 的必要性

最后讲数据清洗，因为这里最容易体现：

**没有 Skill：AI 可能随意处理异常值；有 Skill：AI 会按规则记录、清洗、报告、验收。**

如果课堂时间不够，案例 2 也可以作为课下练习。

## Trae Skill 参考材料

`trae-skill-reference/` 下提供四份可直接发给学生的 Markdown 文档。每份都包含建议目录、原始材料、完整 `SKILL.md` 参考、课堂提示词和提交物清单。

- `trae-skill-reference/01-data-processing-skill.md`：数据清洗与小报告 Skill。
- `trae-skill-reference/02-course-note-audio-skill.md`：课程笔记/录音转写整理 Skill。
- `trae-skill-reference/03-browser-game-skill.md`：HTML 小游戏生成 Skill。
- `trae-skill-reference/04-sqlite-mis-skill.md`：SQLite 简单管理信息系统 Skill。

## 统一对比表

学生完成三个案例后，可以填写这张比较表：

| 比较项 | 聊天生成 | Agent 生成 | Skill + Agent |
| --- | --- | --- | --- |
| 是否理解了全部材料 | 低 / 中 / 高 | 低 / 中 / 高 | 低 / 中 / 高 |
| 是否能处理多个文件 | 低 / 中 / 高 | 低 / 中 / 高 | 低 / 中 / 高 |
| 是否有规划过程 | 低 / 中 / 高 | 低 / 中 / 高 | 低 / 中 / 高 |
| 输出是否稳定 | 低 / 中 / 高 | 低 / 中 / 高 | 低 / 中 / 高 |
| 是否容易复用 | 低 / 中 / 高 | 低 / 中 / 高 | 低 / 中 / 高 |
| 人类需要做什么 |  |  |  |
| AI 容易犯什么错 |  |  |  |
| 适合什么任务 |  |  |  |

## 使用建议

每个案例都建议按以下顺序进行：

1. 先只给聊天窗口一个简短需求，看会发生什么；
2. 再把同样任务交给 Agent，让它读取目录完成任务；
3. 最后先写 Skill，再让 Agent 重做一次；
4. 比较三次结果在完整性、稳定性、可复用性上的差异。

## 备注

- 三个案例目录都预留了 `output/`，用于放 Agent 生成结果。
- 原始材料与输出结果分开，便于课堂反复实验。
- 如需扩展成网页原型、示例解答或课堂展示页，可在现有目录基础上继续补充。
