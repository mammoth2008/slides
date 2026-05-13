# AI Agent 并行编程可靠性参考手册

## 0. 这份手册解决什么问题？

使用 AI 辅助编程时，很多同学会遇到一种情况：

> AI 看起来写了很多代码，也说“完成了”，但程序跑不起来，测试过不了，或者改坏了原来的功能。

如果只让一个 AI 聊天生成代码，问题还比较容易发现；但如果同时开启多个 AI agent 并行写代码，风险会更大：

- agent A 改了登录模块；
- agent B 改了数据库结构；
- agent C 改了前端页面；
- agent D 补了测试；
- 每个 agent 都说自己完成了；
- 最后合并到一起，项目却运行失败。

所以，并行 AI 编程的核心问题不是：

> 怎样让 AI 写更多代码？

而是：

> 怎样让 AI 写出的代码可以检查、可以测试、可以合并、可以维护？

本手册的核心观点是：

> AI 生成代码的可靠性，不主要来自“模型聪明”，而来自“工程流程约束”。

换句话说，我们不能只依赖 AI 自己说“我完成了”，而要把 AI 放进一个明确的软件工程流程中：隔离任务、限制范围、先计划、写测试、跑检查、审查 diff、再合并。

---

## 1. 基本概念

### 1.1 什么是 agentic coding？

`agentic coding` 可以理解为“让 AI agent 参与真实软件开发流程”。

普通聊天式编程通常是这样：

```text
用户：帮我写一个登录函数。
AI：这是代码……
用户：复制粘贴运行。
```

agentic coding 更接近这样：

```text
用户：修复登录超时后刷新 token 失败的问题。
AI agent：
1. 阅读相关代码；
2. 找到可能出错的位置；
3. 写一个失败测试复现 bug；
4. 修改实现；
5. 运行测试；
6. 修复测试失败；
7. 总结修改内容；
8. 提交 patch 或 PR。
```

也就是说，AI 不只是“回答问题”，而是在完成一段开发任务。

---

### 1.2 什么是并行 agent 编程？

并行 agent 编程是指同时让多个 AI agent 处理不同任务。

例如：

```text
Agent A：修复登录 bug
Agent B：给订单模块补测试
Agent C：重构前端组件
Agent D：更新 README 和 API 文档
```

这种方式的优点是速度快，缺点是风险也更高：

- 多个 agent 可能修改同一个文件；
- 不同 agent 的设计思路可能冲突；
- 局部测试通过，整体合并失败；
- agent 可能为了完成任务而修改无关代码；
- 如果没有审查流程，很难知道是谁引入了 bug。

因此，并行 agent 编程必须有更严格的工作流。

---

## 2. 最重要的原则：隔离、验证、再合并

并行 coding 的基本原则可以概括成三句话：

```text
1. 每个 agent 独立工作。
2. 每个结果必须验证。
3. 验证通过后才能合并。
```

不要让多个 agent 同时直接修改同一个工作目录。更好的方式是：

```text
主分支 main：
  保存稳定代码，不直接让 agent 乱改。

Agent A 分支：
  fix-login-timeout

Agent B 分支：
  add-order-tests

Agent C 分支：
  refactor-user-card
```

每个 agent 都在自己的分支或 worktree 中工作。完成后，先检查，再合并。

---

## 3. 推荐的总体流程

一个比较可靠的 AI 并行编程流程如下：

```text
第 1 步：拆分任务
  把大任务拆成小任务，每个任务有明确目标和验收标准。

第 2 步：分配 agent
  每个 agent 只负责一个小任务。

第 3 步：独立工作区
  每个 agent 使用独立 branch / worktree / sandbox。

第 4 步：先研究和计划
  复杂任务先让 agent 阅读代码、提出计划，不要直接改代码。

第 5 步：实现和自测
  agent 修改代码后，必须运行相关测试、lint、type check 或 build。

第 6 步：审查 diff
  查看 agent 到底改了哪些文件，是否有无关修改。

第 7 步：合并前再验证
  rebase / merge 到最新 main 后，再运行测试。

第 8 步：复盘和更新规则
  如果 agent 重复犯错，把规则写入 AGENTS.md / CLAUDE.md / skill。
```

---

## 4. 任务要小，不要把大而空的任务交给 agent

### 4.1 不推荐的任务写法

下面这些任务都太宽泛：

```text
帮我优化这个项目。
```

```text
帮我重构代码，让它更好。
```

```text
帮我把这个网站做完整。
```

这类任务的问题是：

- “优化”是什么意思不清楚；
- “更好”没有验收标准；
- agent 会自己脑补需求；
- 可能修改大量无关文件；
- 最后很难审查。

---

### 4.2 推荐的任务写法

更好的任务应该包含四个部分：

```text
目标 Goal：
  要完成什么？

上下文 Context：
  相关文件、错误信息、已有代码、参考实现在哪里？

约束 Constraints：
  不能做什么？必须遵守什么？

完成标准 Done when：
  什么情况才算完成？
```

示例：

```text
任务：修复登录超时后 token 刷新失败的问题。

目标：
- 当用户 session 过期后，系统应该尝试使用 refresh token 获取新的 access token。
- 如果 refresh token 无效，才跳转到登录页。

上下文：
- 相关代码在 src/auth/session.py 和 src/auth/token.py。
- 相关测试在 tests/test_auth_session.py。
- 当前错误信息是：ExpiredSessionError: access token expired。

约束：
- 不要修改数据库结构。
- 不要改变公开 API。
- 不要删除已有测试。
- 不要添加新的第三方依赖。

完成标准：
- 新增一个失败测试，能够复现当前 bug。
- 修改代码后，该测试通过。
- 运行 `uv run pytest tests/test_auth_session.py` 通过。
- 运行 `uv run ruff check .` 通过。
- 输出修改文件列表、测试结果和剩余风险。
```

---

## 5. 复杂任务先计划，不要直接写代码

### 5.1 为什么要先计划？

AI agent 很容易犯一种错误：

> 还没有真正理解项目，就开始写代码。

这样可能导致：

- 解决错问题；
- 改错文件；
- 绕过真正的 bug；
- 重写不该重写的模块；
- 引入更复杂的新问题。

因此，复杂任务应该先让 agent 做“只读研究”。

---

### 5.2 推荐流程：Explore → Plan → Implement → Commit

可以把复杂任务拆成四个阶段：

```text
1. Explore：探索
   只读代码，不修改文件。

2. Plan：计划
   输出修改方案、影响范围、测试方案。

3. Implement：实现
   按计划修改代码，边改边测试。

4. Commit：提交
   总结 diff、测试结果、风险点，准备提交或 PR。
```

---

### 5.3 给 agent 的提示词模板

```text
请先不要修改任何文件。

第一阶段：Explore
请阅读以下文件和目录：
- src/auth/
- tests/test_auth_session.py
- README.md 中关于认证的部分

请回答：
1. 当前登录和 session 刷新流程是怎样的？
2. 哪些文件可能需要修改？
3. 现有测试覆盖了哪些情况？
4. 这个任务可能有哪些风险？

完成 Explore 后，请输出一个 Plan。
在我确认之前，不要写代码。
```

确认计划后，再让 agent 实现：

```text
请按照刚才的计划实现。

要求：
1. 先新增失败测试，复现 bug。
2. 确认测试失败后，再修改实现。
3. 修改后运行相关测试。
4. 不要修改无关文件。
5. 完成后输出：
   - 修改文件列表
   - 新增或修改的测试
   - 运行过的命令
   - 测试结果
   - 剩余风险
```

---

## 6. “可用代码”必须有机器可检查的标准

### 6.1 不要相信“我已经完成了”

AI agent 经常会说：

```text
完成了。代码已经修复。
```

但这句话本身没有意义。真正有意义的是：

```text
我运行了以下命令：
- uv run pytest tests/test_auth_session.py
- uv run ruff check .

结果：
- 15 passed
- ruff check passed

修改文件：
- src/auth/session.py
- tests/test_auth_session.py

风险：
- 没有运行全量测试。
- 没有验证前端登录页面行为。
```

---

### 6.2 常见检查项目

| 检查类型 | 检查内容 | Python 示例 | 前端示例 |
|---|---|---|---|
| 格式化 | 代码风格是否统一 | `uv run ruff format .` | `npm run format` |
| 静态检查 | 是否有明显错误 | `uv run ruff check .` | `npm run lint` |
| 类型检查 | 类型是否正确 | `uv run mypy .` | `npm run typecheck` |
| 单元测试 | 局部功能是否正确 | `uv run pytest tests/test_x.py` | `npm test` |
| 构建 | 项目是否能构建 | `uv build` | `npm run build` |
| 集成测试 | 多模块协作是否正常 | `uv run pytest tests/integration` | `npm run test:e2e` |

---

### 6.3 完成报告模板

每个 agent 完成任务后，必须输出类似报告：

```markdown
## 完成报告

### 1. 修改内容

- 修改 `src/auth/session.py`
  - 增加 session 过期后自动刷新 token 的逻辑。
- 修改 `tests/test_auth_session.py`
  - 新增 refresh token 有效时的测试。
  - 新增 refresh token 无效时的测试。

### 2. 运行过的检查

```bash
uv run pytest tests/test_auth_session.py
uv run ruff check .
```

### 3. 检查结果

```text
tests/test_auth_session.py: 8 passed
ruff check: passed
```

### 4. 未完成或风险

- 没有运行全量测试。
- 没有测试真实浏览器登录流程。
- 如果 refresh token 接口返回格式变化，仍可能失败。
```

---

## 7. Bug 修复推荐采用“失败测试先行”

### 7.1 为什么要先写失败测试？

如果不写测试，agent 可能只是“看起来修了 bug”。

例如：

```text
用户登录超时后，页面报错。
```

坏的修法：

```python
try:
    refresh_token()
except Exception:
    pass
```

这可能让报错消失，但真正的问题没有解决。

更可靠的流程是：

```text
1. 写一个测试，复现 bug。
2. 运行测试，确认它失败。
3. 修改代码。
4. 再运行测试，确认它通过。
5. 运行相关回归测试。
```

---

### 7.2 给 agent 的提示词模板

```text
请修复这个 bug，但必须先写失败测试。

规则：
1. 不要先修改实现代码。
2. 先新增一个测试，复现当前 bug。
3. 运行测试，确认它失败。
4. 再修改实现代码。
5. 修改后运行新增测试和相关测试。
6. 不允许删除测试、跳过测试或放宽断言来让测试通过。
7. 完成后说明 bug 的根因，而不仅仅说明改了什么。
```

---

### 7.3 案例：修复购物车数量不能减少的问题

#### 问题描述

一个购物车程序中，点击“减少数量”按钮后，商品数量没有减少。

#### 不好的提示

```text
帮我修复购物车 bug。
```

#### 好的提示

```text
任务：修复购物车减少数量失败的问题。

上下文：
- 购物车逻辑在 src/cart/cart.py。
- 测试在 tests/test_cart.py。
- 当前问题：调用 decrease_quantity(product_id) 后，商品数量没有减少。

要求：
1. 先在 tests/test_cart.py 中新增一个失败测试：
   - 添加商品 A，数量为 2。
   - 调用 decrease_quantity(A)。
   - 期望数量变成 1。
2. 确认测试失败后，再修改 src/cart/cart.py。
3. 不允许删除已有测试。
4. 完成后运行：
   - uv run pytest tests/test_cart.py
   - uv run ruff check .
5. 输出修改文件、测试结果和根因说明。
```

---

## 8. 使用 AGENTS.md / CLAUDE.md 固化项目规则

### 8.1 为什么需要项目规则文件？

如果每次都在提示词里重复说明：

```text
用 uv 运行项目。
用 ruff 检查代码。
不要添加依赖。
不要修改无关文件。
完成后要跑测试。
```

这很麻烦，而且容易忘。

更好的做法是把这些规则写入项目根目录的规则文件：

```text
AGENTS.md    # 常用于 OpenAI Codex 等 coding agents
CLAUDE.md    # Claude Code 会读取的项目规则文件
```

这样每次 agent 开始工作时，就能自动获得项目约定。

---

### 8.2 AGENTS.md 示例

可以在项目根目录创建 `AGENTS.md`：

```markdown
# AGENTS.md

## Project Overview

This is a Python teaching project for learning AI-assisted programming.
The project uses `uv` for dependency management and `pytest` for testing.

## Setup

```bash
uv sync
```

## Run

```bash
uv run python main.py
```

## Test

Run targeted tests first:

```bash
uv run pytest tests/test_some_file.py
```

Run all tests before final submission:

```bash
uv run pytest
```

## Lint and Format

```bash
uv run ruff check .
uv run ruff format .
```

## Coding Rules

- Keep changes minimal.
- Do not modify unrelated files.
- Do not add new dependencies without asking.
- Do not change public APIs unless explicitly required.
- Prefer simple, readable code over clever abstractions.
- Preserve existing behavior unless the task explicitly asks to change it.

## Testing Rules

- Bug fixes should include a regression test when possible.
- Do not delete, skip, or weaken tests just to make the suite pass.
- Report which tests were run and their results.

## Completion Report

Before saying the task is complete, report:

1. Changed files.
2. What changed.
3. Tests added or updated.
4. Commands run.
5. Results.
6. Remaining risks.
```

---

### 8.3 CLAUDE.md 示例

如果使用 Claude Code，可以创建 `CLAUDE.md`：

```markdown
# CLAUDE.md

## Development Commands

- Install dependencies: `uv sync`
- Run tests: `uv run pytest`
- Run a single test file: `uv run pytest path/to/test_file.py`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Workflow Rules

- For complex tasks, use Explore → Plan → Implement → Commit.
- For small tasks, make minimal changes directly.
- Prefer targeted tests before full test suite.
- After a series of code changes, run relevant tests.
- Do not modify unrelated files.

## Bug Fix Rules

- Reproduce the bug first when possible.
- Prefer writing a failing test before changing implementation.
- Do not suppress errors unless the task explicitly requires it.
- Explain the root cause in the final report.

## Code Style

- Use clear names.
- Avoid unnecessary abstractions.
- Keep functions small when practical.
- Match existing project style.

## Final Response Requirements

When finished, include:

- Summary of changes.
- Files changed.
- Tests run.
- Test results.
- Known limitations or risks.
```

---

### 8.4 注意：规则文件不要太长

规则文件不是教材，不要写成几十页。

好的规则文件应该：

- 简短；
- 具体；
- 和项目直接相关；
- 能减少 agent 犯错；
- 能被长期复用。

不好的规则包括：

```text
写出高质量代码。
保持优雅。
注意性能。
不要犯错。
```

这些太空泛，agent 很难执行。

更好的规则是：

```text
不要新增第三方依赖，除非用户明确批准。
修改 Python 文件后，必须运行 `uv run ruff check .`。
修 bug 时，优先新增回归测试。
不要删除已有测试。
```

---

## 9. 使用 hooks / scripts 做强制检查

### 9.1 为什么需要 hooks？

写在 `AGENTS.md` 或 `CLAUDE.md` 里的规则，本质上仍然是“提醒”。

但有些事情必须每次都执行，比如：

- 格式化代码；
- 运行 lint；
- 禁止修改某些目录；
- 禁止提交包含密钥的文件；
- 提交前运行测试。

这类事情更适合用 hook 或脚本强制执行。

---

### 9.2 可以自动化的检查

```text
每次修改后：
- 格式化代码
- 运行 lint

提交前：
- 运行相关测试
- 检查是否有敏感信息
- 检查是否修改了禁止修改的文件

合并前：
- 运行全量测试
- 构建项目
```

---

### 9.3 pre-commit 示例

Python 项目可以使用 `pre-commit`。示例 `.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.0
    hooks:
      - id: ruff-check
      - id: ruff-format
```

安装后：

```bash
uv add --dev pre-commit ruff
uv run pre-commit install
```

这样每次提交前就会自动运行检查。

---

## 10. 并行 agent 的角色分工

并行不等于“大家一起乱写”。

更好的方式是给 agent 分配不同角色。

---

### 10.1 常见角色

```text
Planner agent：
  只读代码，制定计划。

Implementer agent：
  按计划修改代码。

Test agent：
  负责编写测试和补充边界情况。

Reviewer agent：
  审查 diff，寻找 bug、风险和无关修改。

Integrator：
  合并分支，解决冲突，运行全量测试。
```

---

### 10.2 双 agent 模式

最简单的可靠模式是两个 agent：

```text
Agent A：写代码
Agent B：审查代码
```

Agent B 不应该直接相信 Agent A 的总结，而应该只看：

- diff；
- 测试；
- 需求；
- 项目规则。

#### Reviewer agent 提示词模板

```text
你现在是代码审查 agent。

请审查以下 diff，重点检查：

1. 是否完成了任务要求？
2. 是否修改了无关文件？
3. 是否删除、跳过或放宽了测试？
4. 是否引入新的依赖？
5. 是否改变了公开 API？
6. 是否有明显 bug？
7. 是否有安全风险？
8. 是否有过度设计？
9. 是否缺少测试？
10. 是否需要人工进一步确认？

请不要重写代码。
请输出：
- 必须修改的问题
- 建议修改的问题
- 可以接受的部分
- 是否建议合并
```

---

### 10.3 三 agent 模式

更稳的模式是三个 agent：

```text
Agent A：实现功能
Agent B：补测试
Agent C：审查代码
```

适合稍微复杂的任务，例如：

- 新增一个登录功能；
- 重构一个数据处理模块；
- 给旧项目补测试；
- 实现一个课程作业管理小系统。

---

## 11. 合并前必须重新验证

### 11.1 为什么单个分支通过不代表整体通过？

Agent A 的分支测试通过，Agent B 的分支也测试通过，但合并后仍然可能失败。

原因包括：

- 两个分支修改了同一个函数；
- 一个分支改了 API，另一个分支仍按旧 API 调用；
- 一个分支更新了依赖，另一个分支没有同步；
- 两个分支都通过了局部测试，但全量测试失败。

所以合并前必须在最新 main 上重新验证。

---

### 11.2 推荐合并流程

```bash
# 切换到主分支
git checkout main

# 拉取最新代码
git pull

# 切换到 agent 分支
git checkout fix-login-timeout

# 基于最新 main 重新整理
git rebase main

# 运行测试
uv run pytest

# 运行 lint
uv run ruff check .

# 回到 main
git checkout main

# 合并
git merge --no-ff fix-login-timeout

# 合并后再跑一次测试
uv run pytest
```

---

## 12. 常见反模式

### 12.1 反模式一：多个 agent 直接改同一个目录

不推荐：

```text
所有 agent 都在同一个项目目录里直接修改文件。
```

风险：

- 修改互相覆盖；
- 无法追踪责任；
- 很难回滚；
- 难以判断 bug 来自哪个 agent。

推荐：

```text
每个 agent 使用独立 branch / worktree。
```

---

### 12.2 反模式二：任务没有验收标准

不推荐：

```text
帮我优化登录模块。
```

推荐：

```text
重构 src/auth/session.py 中的 token 刷新逻辑。
要求：
- 不改变 public API。
- 新增 3 个测试。
- 运行 tests/test_auth_session.py 通过。
- 不修改无关文件。
```

---

### 12.3 反模式三：让 agent 自己审查自己

不推荐：

```text
Agent A 写代码，然后 Agent A 说自己写得很好。
```

推荐：

```text
Agent A 写代码。
Agent B 审查 diff。
CI 运行测试。
人类审查关键设计。
```

---

### 12.4 反模式四：为了通过测试而删除测试

这是非常危险的行为。

必须明确禁止：

```text
不允许删除失败测试。
不允许把断言改弱。
不允许把测试标记为 skip。
不允许吞掉异常来掩盖 bug。
```

---

### 12.5 反模式五：一次性大规模重写

不推荐：

```text
把整个项目重构一下。
```

推荐：

```text
第一步：只重构 src/cart/cart.py 中的数量计算逻辑。
第二步：补测试。
第三步：确认通过后，再考虑下一个模块。
```

---

## 13. 课堂案例一：命令行待办事项管理器

### 13.1 项目背景

假设已有一个简单的命令行待办事项程序：

```text
todo/
  main.py
  todo.py
  storage.py
tests/
  test_todo.py
```

已有功能：

```text
add      添加任务
list     列出任务
done     标记完成
delete   删除任务
```

现在要并行改进它。

---

### 13.2 并行任务拆分

```text
Agent A：
  给任务增加 due date 截止日期。

Agent B：
  增加 search 搜索功能。

Agent C：
  给 storage.py 补充异常处理和测试。

Agent D：
  审查 Agent A/B/C 的 diff。
```

---

### 13.3 Agent A 任务提示词

```text
任务：给 todo 程序增加 due date 截止日期。

目标：
- add 命令可以接受可选参数 --due YYYY-MM-DD。
- list 命令显示任务时，如果有 due date，要一起显示。
- 已有不带 due date 的任务仍然可以正常使用。

上下文：
- CLI 入口在 main.py。
- 任务数据结构在 todo.py。
- 存储逻辑在 storage.py。
- 测试在 tests/test_todo.py。

约束：
- 不要引入第三方依赖。
- 不要改变已有 add/list/done/delete 的基本行为。
- 不要修改搜索功能，因为那是其他 agent 的任务。

完成标准：
- 新增测试覆盖：
  1. 添加带 due date 的任务；
  2. 添加不带 due date 的任务；
  3. list 能显示 due date。
- 运行 `uv run pytest tests/test_todo.py` 通过。
- 运行 `uv run ruff check .` 通过。
- 输出修改文件、测试结果和风险。
```

---

### 13.4 Agent B 任务提示词

```text
任务：给 todo 程序增加 search 搜索功能。

目标：
- 新增命令：search KEYWORD。
- 搜索任务标题中包含 KEYWORD 的任务。
- 搜索应该大小写不敏感。

上下文：
- CLI 入口在 main.py。
- 任务逻辑在 todo.py。
- 测试在 tests/test_todo.py。

约束：
- 不要修改 due date 相关逻辑。
- 不要引入第三方依赖。
- 不要修改已有命令行为。

完成标准：
- 新增测试覆盖：
  1. 可以搜索到匹配任务；
  2. 大小写不敏感；
  3. 没有结果时返回空列表或友好提示。
- 运行 `uv run pytest tests/test_todo.py` 通过。
- 运行 `uv run ruff check .` 通过。
```

---

### 13.5 Reviewer agent 任务提示词

```text
你是 reviewer agent。

请审查 Agent A 和 Agent B 的修改，重点检查：

1. 两个 agent 是否修改了同一个函数？
2. due date 和 search 是否互相影响？
3. 是否修改了无关文件？
4. 是否新增了必要测试？
5. 是否所有测试都通过？
6. 是否有重复逻辑可以暂时接受，还是必须合并前整理？
7. 是否建议合并？

请输出：
- 必须修复的问题
- 建议改进的问题
- 可以合并的部分
- 不建议合并的部分
```

---

## 14. 课堂案例二：学生成绩分析程序

### 14.1 项目背景

程序读取一个 CSV 文件，计算学生成绩统计信息。

已有文件：

```text
grade_analyzer/
  main.py
  parser.py
  statistics.py
  report.py
tests/
  test_parser.py
  test_statistics.py
```

已有功能：

- 读取 CSV；
- 计算平均分；
- 找出最高分和最低分；
- 输出文本报告。

---

### 14.2 并行任务设计

```text
Agent A：
  增加中位数 median 计算。

Agent B：
  增加不及格学生列表。

Agent C：
  增加 Markdown 报告输出。

Agent D：
  编写综合测试，检查完整流程。
```

---

### 14.3 任务拆分原则

这个案例适合训练同学理解：

```text
功能开发 agent 和测试 agent 可以分开。
统计逻辑和报告逻辑可以分开。
每个 agent 只改少数文件。
最后由 reviewer 检查整体一致性。
```

---

### 14.4 Agent C 示例任务

```text
任务：增加 Markdown 报告输出。

目标：
- 在 report.py 中增加 generate_markdown_report(stats)。
- 输出内容包括：
  - 平均分
  - 最高分
  - 最低分
  - 如果 stats 中包含 median，也显示中位数
  - 如果 stats 中包含 failed_students，也显示不及格学生列表

上下文：
- 现有文本报告函数在 report.py。
- 统计结果由 statistics.py 返回。
- 测试可以新增到 tests/test_report.py。

约束：
- 不要修改 CSV 解析逻辑。
- 不要直接计算统计数据，report.py 只负责展示。
- 不要破坏现有 generate_text_report。

完成标准：
- 新增 tests/test_report.py。
- 覆盖包含 median 和 failed_students 的情况。
- 覆盖没有 median 和 failed_students 的情况。
- 运行 `uv run pytest tests/test_report.py` 通过。
```

---

## 15. 课堂案例三：小型 Web API 项目

### 15.1 项目背景

一个 FastAPI 风格的小项目：

```text
app/
  main.py
  models.py
  database.py
  routers/
    users.py
    tasks.py
tests/
  test_users.py
  test_tasks.py
```

已有功能：

- 创建用户；
- 创建任务；
- 查询任务列表。

现在要增加权限控制。

---

### 15.2 并行任务设计

```text
Agent A：
  增加用户登录和 token 生成。

Agent B：
  给 tasks 接口增加“只能访问自己的任务”的限制。

Agent C：
  补充权限相关测试。

Agent D：
  审查安全风险。
```

---

### 15.3 为什么这个案例更难？

因为权限控制属于高风险代码：

- 不能只看功能是否能跑；
- 要检查是否存在越权访问；
- 要检查未登录用户是否被拒绝；
- 要检查一个用户不能访问另一个用户的数据；
- 测试必须覆盖安全边界。

---

### 15.4 安全审查 agent 提示词

```text
你是安全审查 agent。

请审查当前权限控制相关 diff，重点检查：

1. 未登录用户是否能访问受保护接口？
2. 用户 A 是否能访问用户 B 的任务？
3. token 校验失败时是否正确拒绝？
4. 是否把密钥写死在代码中？
5. 是否把异常信息直接暴露给用户？
6. 是否存在绕过权限检查的路径？
7. 测试是否覆盖了成功和失败场景？
8. 是否修改了无关模块？

请输出：
- 高风险问题
- 中风险问题
- 低风险问题
- 必须补充的测试
- 是否建议合并
```

---

## 16. 作业建议

### 16.1 作业目标

通过一次小型项目练习，理解：

- 如何给 AI agent 写清楚任务；
- 如何拆分并行任务；
- 如何使用测试验证代码；
- 如何审查 AI 生成代码；
- 如何避免“看起来完成但实际不可用”。

---

### 16.2 作业要求

每组选择一个小项目，例如：

```text
1. 命令行待办事项管理器
2. 学生成绩分析程序
3. 简单记账程序
4. 简单图书管理系统
5. 小型 Web API
```

每组至少完成：

```text
1. 一个 AGENTS.md 或 CLAUDE.md。
2. 至少 3 个 agent 任务提示词。
3. 至少 2 个功能性修改。
4. 至少 1 个测试 agent 或 reviewer agent。
5. 最终提交一份完成报告。
```

---

### 16.3 提交内容

```text
project/
  AGENTS.md 或 CLAUDE.md
  prompts/
    agent_a_prompt.md
    agent_b_prompt.md
    reviewer_prompt.md
  src/
  tests/
  REPORT.md
```

`REPORT.md` 应包括：

```markdown
# AI 并行编程实验报告

## 1. 项目简介

## 2. 并行任务拆分

| Agent | 任务 | 修改文件 | 验收标准 |
|---|---|---|---|

## 3. 使用的项目规则

说明 AGENTS.md / CLAUDE.md 中写了哪些规则。

## 4. 测试与验证

列出运行过的命令和结果。

## 5. 代码审查结果

说明 reviewer agent 或人工审查发现了哪些问题。

## 6. 遇到的问题

例如：
- agent 修改了无关文件；
- agent 忘记运行测试；
- agent 删除了测试；
- 合并后出现冲突；
- 提示词不清楚导致理解错误。

## 7. 改进后的规则

说明你们如何根据问题更新 AGENTS.md / CLAUDE.md。

## 8. 总结

说明你们对 AI 辅助编程可靠性的理解。
```

---

## 17. 最小检查清单

每次让 AI agent 写代码前，检查：

```text
[ ] 任务是否足够小？
[ ] 是否写清楚目标？
[ ] 是否提供相关文件或错误信息？
[ ] 是否说明不能修改什么？
[ ] 是否写清楚完成标准？
[ ] 是否要求运行测试？
[ ] 是否要求输出修改文件和测试结果？
```

每次 agent 完成后，检查：

```text
[ ] 是否真的改了正确的文件？
[ ] 是否有无关修改？
[ ] 是否新增或更新了测试？
[ ] 是否运行了测试？
[ ] 测试结果是否明确？
[ ] 是否删除、跳过或放宽了测试？
[ ] 是否新增了未经允许的依赖？
[ ] 是否改变了公开 API？
[ ] 是否说明剩余风险？
[ ] 是否需要另一个 agent 或人类审查？
```

合并前检查：

```text
[ ] 当前分支是否基于最新 main？
[ ] 是否解决了冲突？
[ ] 是否运行了全量测试？
[ ] 是否运行了 lint / format / type check？
[ ] 是否可以回滚？
[ ] 是否有人审查过关键 diff？
```

---

## 18. 一句话总结

AI agent 并行编程的可靠性，不来自“让 AI 一次写对”，而来自一套清楚的工程流程：

```text
小任务
清晰提示
独立分支
先计划
写测试
跑检查
审查 diff
合并前再验证
复盘后更新规则
```

如果没有这些流程，多个 AI agent 只会更快地产生不可控代码。

如果有这些流程，AI agent 才可能从“会写代码的聊天工具”，变成“可以参与软件工程流水线的协作者”。

---

## 19. 参考资料与出处

以下资料用于整理本手册中的实践建议。阅读时建议重点关注：任务提示、AGENTS.md / CLAUDE.md、worktree、Plan Mode、hooks、skills、测试与 review。

1. OpenAI Codex Best Practices
   https://developers.openai.com/codex/learn/best-practices

2. OpenAI Codex App Features
   https://developers.openai.com/codex/app/features

3. OpenAI Codex Worktrees
   https://developers.openai.com/codex/app/worktrees

4. OpenAI Codex AGENTS.md Guide
   https://developers.openai.com/codex/guides/agents-md

5. OpenAI Codex Agent Skills
   https://developers.openai.com/codex/skills

6. OpenAI Codex Exec Plans / PLANS.md
   https://developers.openai.com/cookbook/articles/codex_exec_plans

7. Anthropic Claude Code Best Practices
   https://code.claude.com/docs/en/best-practices

8. Anthropic Claude Code Common Workflows
   https://code.claude.com/docs/en/common-workflows
