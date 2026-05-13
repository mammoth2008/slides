# 案例三：HTML 小游戏 Skill

## 课堂任务

让学生制作一个 Trae Skill，用于从一个游戏想法生成可运行的 HTML/CSS/JS 小游戏。

本案例重点是训练学生理解：

- 编程任务不能一上来就写代码。
- 游戏必须先有规则、状态和交互。
- “看起来像游戏页面”和“真的能玩”是两回事。

## 建议目录

```text
browser-game-demo/
  .trae/
    skills/
      browser-game-builder/
        SKILL.md
  docs/
    game_idea.md
    game_requirements.md
  src/
  output/
```

## 原始材料 1：`docs/game_idea.md`

```markdown
# 游戏想法：SQL 查询闯关

做一个适合数据库课程入门的网页小游戏。

玩家需要根据题目选择正确的 SQL 查询语句。每答对一题获得 10 分，答错扣 1 次生命。生命为 0 时失败。完成全部题目后显示胜利。

游戏应该简单、清晰，适合在课堂上投影演示。不要做复杂登录，不要联网，不要依赖后端。
```

## 原始材料 2：`docs/game_requirements.md`

```markdown
# 游戏要求

必须实现：

1. 开始界面。
2. 至少 5 道 SQL 选择题。
3. 分数和生命值显示。
4. 答对、答错反馈。
5. 胜利界面。
6. 失败界面。
7. 重新开始按钮。

技术要求：

- 只使用 HTML、CSS、JavaScript。
- 文件放在 `src/` 下。
- 页面离线可打开。
- 不使用外部 CDN。

输出文件：

- `src/index.html`
- `src/style.css`
- `src/game.js`
- `output/game-spec.md`
- `output/test-checklist.md`
```

## 完整 Skill 参考：`.trae/skills/browser-game-builder/SKILL.md`

```markdown
---
name: browser-game-builder
description: 当用户需要根据一个教学游戏想法生成可运行的 HTML/CSS/JavaScript 小游戏时使用。
---

# 目标

把模糊的游戏想法变成一个可运行、可演示、可检查的浏览器小游戏。必须先明确玩法和验收标准，再写代码。

# 适用场景

- 用户说“写一个小游戏”“做一个网页游戏”“做课堂互动游戏”。
- 项目中有 `docs/game_idea.md` 或 `docs/game_requirements.md`。
- 输出要求是 HTML/CSS/JavaScript，而不是大型游戏引擎。

# 输入约定

优先读取：

1. `docs/game_idea.md`
2. `docs/game_requirements.md`

如果游戏目标、胜负条件或操作方式不清楚，先在 `output/game-spec.md` 中提出合理假设，再执行。

# 工作流程

1. 读取游戏想法和要求。
2. 先生成 `output/game-spec.md`，写清：
   - 游戏主题
   - 玩家目标
   - 操作方式
   - 核心循环
   - 得分规则
   - 胜利条件
   - 失败条件
3. 再生成 `src/index.html`、`src/style.css`、`src/game.js`。
4. 确保游戏有开始、运行、胜利、失败、重新开始状态。
5. 确保所有资源本地可用，不依赖外网。
6. 生成 `output/test-checklist.md`，列出手工测试步骤。
7. 自查页面是否可能空白、按钮是否能点击、状态是否能变化。

# 代码规则

- HTML 只负责结构。
- CSS 负责布局和视觉样式。
- JavaScript 负责题目、状态、计分和交互。
- 不把所有代码塞进一个文件，除非用户明确要求。
- 不使用外部 CDN。
- 不引入复杂构建工具。
- 不做登录、数据库或网络请求。

# 输出文件

必须输出：

- `src/index.html`
- `src/style.css`
- `src/game.js`
- `output/game-spec.md`
- `output/test-checklist.md`

# 验收清单

完成后检查：

- 打开 `src/index.html` 后不是空白页。
- 点击开始后进入题目。
- 答对会加分。
- 答错会减少生命值。
- 生命值为 0 时出现失败界面。
- 答完全部题目后出现胜利界面。
- 重新开始按钮能重置游戏。
- 离线状态下仍可运行。
```

## 课堂提示词

```text
使用 browser-game-builder 技能，读取 docs/ 下的游戏想法和要求，先写 game-spec.md，再生成一个可离线运行的 HTML/CSS/JS 小游戏。完成后给出手工测试清单。
```

## 学生提交物

- `.trae/skills/browser-game-builder/SKILL.md`
- `output/game-spec.md`
- `src/index.html`
- `src/style.css`
- `src/game.js`
- `output/test-checklist.md`

## 拓展任务

让学生改写原始材料，把游戏换成以下主题之一：

- 数据库索引消消乐
- E-R 图配对游戏
- SQL 注入防御闯关
- 信息系统角色分类游戏

