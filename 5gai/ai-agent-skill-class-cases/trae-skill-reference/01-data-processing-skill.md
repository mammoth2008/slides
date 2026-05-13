# 案例一：数据处理 Skill

## 课堂任务

让学生制作一个 Trae Skill，用于清洗一份 CSV 数据，并生成可复核的小报告。

本案例重点不是“让 AI 算一个平均数”，而是训练学生把数据处理中的专业规范写进 Skill：

- 原始数据不能被覆盖。
- 缺失值、重复值、异常值不能静默删除。
- 每一个处理规则都要可追溯。
- 统计结论必须基于真实计算。

## 建议目录

```text
data-processing-demo/
  .trae/
    skills/
      data-cleaning-report/
        SKILL.md
  data/
    student_ai_tool_usage.csv
  docs/
    data_dictionary.md
    report_requirements.md
  output/
```

## 原始材料 1：`data/student_ai_tool_usage.csv`

```csv
student_id,major,grade,weekly_ai_minutes,ai_tasks,assignment_score,self_report_learning_gain,notes
S001,信息管理,2023,120,资料检索;代码解释,86,4,按要求记录使用过程
S002,信息管理,2023,45,资料检索,78,3,
S003,工商管理,2022,300,论文润色;资料检索,91,5,可能存在过度依赖
S004,信息管理,2023,,代码解释;SQL练习,82,4,缺少使用时长
S005,会计学,2022,20,资料检索,73,2,低频使用
S006,信息管理,2023,180,SQL练习;报表生成,88,4,结果经过人工核对
S007,信息管理,2023,180,SQL练习;报表生成,88,4,重复记录
S007,信息管理,2023,180,SQL练习;报表生成,88,4,重复记录
S008,市场营销,2022,15,论文润色,69,2,
S009,信息管理,2023,999,代码解释;作业生成,95,5,异常高时长待核对
S010,信息管理,2023,60,资料检索;概念解释,80,3,
S011,工商管理,2022,0,未使用,72,1,
S012,信息管理,2023,90,SQL练习;概念解释,84,4,
S013,信息管理,2023,-30,资料检索,77,3,负数时长错误
S014,会计学,2022,75,报表生成,83,4,
S015,信息管理,2023,140,SQL练习;报表生成;代码解释,90,5,
```

## 原始材料 2：`docs/data_dictionary.md`

```markdown
# 数据字典

| 字段 | 含义 | 说明 |
| --- | --- | --- |
| student_id | 学生编号 | 应唯一 |
| major | 专业 | 中文专业名称 |
| grade | 年级 | 入学年份 |
| weekly_ai_minutes | 每周使用 AI 的分钟数 | 允许为空，但不允许为负数 |
| ai_tasks | AI 使用任务 | 多个任务用分号分隔 |
| assignment_score | 最近一次课程作业成绩 | 0-100 |
| self_report_learning_gain | 自评学习收获 | 1-5 |
| notes | 备注 | 可能包含异常说明 |
```

## 原始材料 3：`docs/report_requirements.md`

```markdown
# 报告要求

请生成一个 Markdown 小报告，至少包括：

1. 数据概况：行数、字段数、主要字段。
2. 数据质量：缺失、重复、异常值清单。
3. 清洗规则：每条规则说明原因。
4. 描述统计：AI 使用时长、作业成绩、自评学习收获。
5. 分组比较：信息管理专业与其他专业的差异。
6. 风险提示：不能从这份数据中得出哪些结论。

要求：

- 原始 CSV 不得覆盖。
- 清洗后文件保存为 `output/student_ai_tool_usage_cleaned.csv`。
- 问题清单保存为 `output/issues.md`。
- 报告保存为 `output/summary.md`。
```

## 完整 Skill 参考：`.trae/skills/data-cleaning-report/SKILL.md`

```markdown
---
name: data-cleaning-report
description: 当用户需要清洗 CSV/Excel 数据、生成统计摘要和数据质量报告时使用。适用于课堂数据、问卷数据、成绩数据和简单业务数据。
---

# 目标

把原始数据整理成可分析、可复核、可提交的小报告。重点是保留处理依据，而不是只给一个看似完整的结论。

# 适用场景

- 用户说“清洗数据”“生成报表”“统计汇总”“检查数据质量”。
- 项目中出现 `data/*.csv`、`data/*.xlsx` 或数据字典。
- 用户需要 Markdown 报告、清洗后数据和问题清单。

# 输入约定

优先读取：

1. `docs/data_dictionary.md`
2. `docs/report_requirements.md`
3. `data/` 下的原始数据文件

如果缺少数据字典，先根据字段名和样例推断含义，并在报告中标注“字段含义为推断”。

# 工作流程

1. 读取数据字段、行数、样例和数据字典。
2. 检查缺失值、重复记录、非法值和明显异常值。
3. 不覆盖原始文件；把清洗结果写入 `output/`。
4. 对每一条清洗规则写明理由，例如“删除完全重复行”“保留异常但列入问题清单”。
5. 生成描述统计。统计必须基于实际计算，不得凭直觉概括。
6. 生成分组比较，但只做描述，不做因果判断。
7. 输出 `issues.md`，记录无法自动判断的问题。
8. 最后按验收清单自查。

# 处理规则

- 完全重复行可以删除，但要在 `issues.md` 中记录。
- 缺失值不要擅自填补，除非用户明确要求。
- 负数时长、超过合理范围的时长、超出量表范围的值，先列入问题清单。
- 不得删除备注字段。
- 不得把相关性写成因果关系。
- 不得说“AI 使用越多成绩越高”这类因果结论。

# 输出文件

必须输出：

- `output/student_ai_tool_usage_cleaned.csv`
- `output/issues.md`
- `output/summary.md`

`summary.md` 至少包含：

- 数据概况
- 数据质量问题
- 清洗规则
- 描述统计
- 分组比较
- 风险与限制

# 验收清单

完成后检查：

- 原始数据文件仍在 `data/` 中，未被覆盖。
- `output/` 中有清洗后数据、问题清单和报告。
- 报告中的数字能在清洗后数据中复核。
- 异常值没有被静默删除。
- 报告没有做超出数据支持的因果判断。
```

## 课堂提示词

```text
使用 data-cleaning-report 技能，读取本项目中的 data/ 和 docs/，完成数据清洗与小报告生成。不要覆盖原始数据。完成后说明你发现了哪些数据质量问题，以及哪些结论不能从这份数据中得出。
```

## 学生提交物

- `.trae/skills/data-cleaning-report/SKILL.md`
- `output/student_ai_tool_usage_cleaned.csv`
- `output/issues.md`
- `output/summary.md`

