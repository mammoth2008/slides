# 案例四：SQLite 简单管理信息系统 Skill

## 课堂任务

让学生制作一个 Trae Skill，用于从一个简单业务场景生成基于 SQLite 的管理信息系统原型。

本案例重点是训练学生经历完整的信息系统开发链条：

需求理解 → 数据建模 → 数据库设计 → CRUD 功能 → 测试数据 → 启动说明。

## 建议目录

```text
sqlite-mis-demo/
  .trae/
    skills/
      sqlite-mis-builder/
        SKILL.md
  docs/
    business_brief.md
    feature_requirements.md
  src/
  data/
  output/
```

## 原始材料 1：`docs/business_brief.md`

```markdown
# 业务场景：实验室设备借用管理

学院实验室有一批教学设备，例如笔记本电脑、投影仪、传感器套件、移动硬盘。教师和学生可以申请借用设备。

现在希望做一个很小的管理系统原型，用于记录：

- 设备信息
- 借用人信息
- 借用记录
- 归还状态

系统不需要登录，不需要联网，不需要复杂权限。重点是让学生理解管理信息系统中的数据表、关系和增删改查。
```

## 原始材料 2：`docs/feature_requirements.md`

```markdown
# 功能要求

技术路线：

- Python + Flask + SQLite
- 或 Streamlit + SQLite
- 由 AI 根据简单性选择一种，但必须说明选择理由

必须实现：

1. 初始化数据库。
2. 插入测试数据。
3. 查看设备列表。
4. 新增设备。
5. 查看借用记录。
6. 新增借用记录。
7. 标记归还。
8. README 说明启动方法。

数据表至少包括：

- equipment：设备
- borrower：借用人
- loan：借用记录

安全要求：

- SQL 必须参数化。
- 不允许拼接用户输入执行 SQL。
- 数据库文件保存到 `data/lab_equipment.db`。

输出文件：

- `src/app.py`
- `src/schema.sql`
- `src/seed.py`
- `data/lab_equipment.db`
- `README.md`
- `output/er-design.md`
- `output/test-plan.md`
```

## 完整 Skill 参考：`.trae/skills/sqlite-mis-builder/SKILL.md`

```markdown
---
name: sqlite-mis-builder
description: 当用户需要基于 SQLite 快速生成一个简单管理信息系统原型时使用，适合图书借阅、设备管理、课程签到、社团成员等小型 CRUD 场景。
---

# 目标

从业务场景出发，生成一个可运行的小型管理信息系统原型。重点是数据模型清楚、CRUD 功能闭环、启动方式明确，而不是做复杂界面。

# 适用场景

- 用户说“做一个管理信息系统”“用 SQLite 做 CRUD”“做一个小型 MIS 原型”。
- 项目中有 `docs/business_brief.md` 和 `docs/feature_requirements.md`。
- 任务适合单机 SQLite，不需要真实部署。

# 输入约定

优先读取：

1. `docs/business_brief.md`
2. `docs/feature_requirements.md`

如果业务实体不清楚，先在 `output/er-design.md` 中列出假设，再生成代码。

# 工作流程

1. 读取业务场景和功能要求。
2. 先设计数据模型，输出 `output/er-design.md`：
   - 实体
   - 字段
   - 主键
   - 外键
   - 关系说明
3. 生成 `src/schema.sql`。
4. 生成 `src/seed.py`，用于初始化数据库和测试数据。
5. 生成 `src/app.py`，实现基本 CRUD。
6. 生成或更新 `README.md`，说明依赖安装、初始化和启动方法。
7. 生成 `output/test-plan.md`，列出手工测试步骤。
8. 自查所有 SQL 写入操作是否使用参数化。

# 技术规则

- 默认使用 Python + Flask + SQLite；如果选择 Streamlit，必须说明理由。
- SQLite 数据库文件固定放在 `data/` 下。
- 所有表必须有主键。
- 有关系的表必须使用外键字段。
- 写入、更新、删除操作必须参数化。
- 不做登录、权限、云部署和复杂前端。
- 不把数据库写到临时目录。

# 功能底线

至少实现：

- 查看设备列表
- 新增设备
- 查看借用记录
- 新增借用记录
- 标记归还
- 初始化测试数据

# 输出文件

必须输出：

- `src/app.py`
- `src/schema.sql`
- `src/seed.py`
- `data/lab_equipment.db`
- `README.md`
- `output/er-design.md`
- `output/test-plan.md`

# 验收清单

完成后检查：

- `README.md` 能让同学按步骤启动系统。
- `schema.sql` 中每张表都有主键。
- `loan` 表能关联设备和借用人。
- 能新增一条设备记录。
- 能新增一条借用记录。
- 能把借用记录标记为已归还。
- 数据库文件位于 `data/lab_equipment.db`。
- 代码中没有用字符串拼接执行用户输入 SQL。
```

## 课堂提示词

```text
使用 sqlite-mis-builder 技能，读取 docs/ 下的业务场景和功能要求，先完成 ER 设计，再生成基于 SQLite 的简单管理信息系统。要求能初始化测试数据，并能完成设备新增、借用记录新增和归还标记。
```

## 学生提交物

- `.trae/skills/sqlite-mis-builder/SKILL.md`
- `output/er-design.md`
- `src/schema.sql`
- `src/seed.py`
- `src/app.py`
- `data/lab_equipment.db`
- `README.md`
- `output/test-plan.md`

## 拓展任务

让学生把业务场景改成以下之一：

- 图书借阅管理
- 社团成员管理
- 课程签到管理
- 实验耗材领用管理

比较不同场景下数据表设计和 CRUD 功能的变化。
