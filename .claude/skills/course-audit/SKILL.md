---
name: course-audit
description: Audit an existing course slide directory and write a rebuild baseline. Use when the user asks to inspect, review, audit, summarize, establish a working starting point, or prepare a course for reconstruction from existing impress.js HTML, courses-vault markdown, mindmaps, exercises, and resources in this slides repo.
---

# Course Audit

## Purpose

Use this skill to turn an existing course folder into a factual rebuild baseline: what exists, what is missing, what is broken, what is pedagogically questionable, and what decisions must be made before generating new slides.

This is an audit workflow, not a repair workflow. Do not rewrite course slides, regenerate HTML, or move resources unless the user explicitly asks for implementation after the audit.

## Required Context

Before auditing:

1. Read project rules in `AGENTS.md`.
2. If the task concerns slide generation, editing, source md, navigation, layout, or mindmap, also use `slides-workflow`.
3. Confirm the course mapping:
   - source: `/Users/Freeman/Documents/products/courses/library/texts/{course}-slide-drafts/`
   - target: `{course-dir}/`
   - generated HTML must not remain in `draft/` or in the courses-vault source package
4. Treat the courses-vault source package as the intended long-term source, even if the current course has drifted into HTML-only edits. `draft/{course}/` is legacy compatibility/cache material, not the new source of truth.

## Audit Scope

Inspect at least these layers:

- **Source layer**: Which courses-vault source files exist under `slide-drafts/`, `mindmaps/`, `layout-data/`, `course-planning/`, and related package folders; which generated HTML pages lack source md; and whether mindmap md exists.
- **Target layer**: Which `{course-dir}/*.html` files exist, including course index, chapter pages, exercise pages, resource pages, and special pages.
- **Index layer**: Whether the course landing page links to existing pages and whether labels match actual page titles.
- **Navigation layer**: Whether `cXXq` pages have real questions, correct left/right navigation, and correct middle exercise links.
- **Layout layer**: Check duplicate step ids, broken `data-rel-to`, obvious non-image overlaps, legacy coordinates, and `check_layout.py` incompatibilities.
- **Resource layer**: Check referenced images, iframe mindmaps, videos, SVGs, and generated mindmap HTML.
- **Pedagogy layer**: Ask whether the current structure still matches course goals, student profile, weekly hours, assignments, and assessment.
- **Rebuild layer**: Identify decisions required before restoring md or regenerating HTML.

## Recommended Commands

Use `rg` and `find` first. Avoid broad manual browsing when structured scans can reveal drift faster.

Useful scans:

```bash
find {course-dir} -maxdepth 1 -type f -name '{prefix}-*.html' -print | sort
find /Users/Freeman/Documents/products/courses/library/texts/{course}-slide-drafts -maxdepth 2 -type f -name '*.md' -print | sort
rg -n 'href="{prefix}-|src="|!\[[^\]]*\]\(|id="c[0-9]+q"|id="mm[0-9]+|### ' {course-dir}/{prefix}-*.html
python3 .claude/skills/build-layout/check_layout.py {course-dir}/{file}.html --verbose
```

When using `check_layout.py`, interpret results with course context:

- Duplicate ids and `CHAIN BREAK` are hard errors.
- Non-image text pages sharing the same coordinate are serious layout problems.
- Image pages intentionally sharing a viewport may be acceptable.
- Old coordinates such as `data-rel-z="-0.5w"` may break the checker and should be recorded as tool incompatibility or legacy layout debt.

## Review Questions

Do not stop at file health. Include the questions a strong architect or course designer would ask:

- What are the actual learning outcomes for the next teaching cycle?
- Does the directory structure match those outcomes, or only an old textbook table of contents?
- What is the student profile: major, prior programming, SQL, math, and domain knowledge?
- What are the contact hours, lab hours, homework cadence, and assessment artifacts?
- Is there a reusable through-case that can connect concepts, SQL, design, transactions, and evaluation?
- Are screenshots, tools, versions, and technical claims still current?
- Are practice pages aligned with outcomes, or only concept recall?
- Is the generation contract clear enough that future work can be reproduced from md?
- Which HTML pages are useful old assets, and which should be retired rather than repaired?

## Output File

If the user asks for a written baseline, create a markdown file in the requested course target directory unless they specify another location.

Use an English filename that states both audit and future-work purpose:

```text
{prefix}-course-audit-and-rebuild-baseline.md
```

Examples:

- `1dbpa/dbpa-course-audit-and-rebuild-baseline.md`
- `2cciot/cciot-course-audit-and-rebuild-baseline.md`
- `6ita/ita-course-audit-and-rebuild-baseline.md`

## Output Structure

Use this structure unless the user asks otherwise. Keep the H2 headings stable across courses so baseline files can be compared and searched consistently.

```markdown
# {COURSE} Course Audit and Rebuild Baseline

检查日期: YYYY-MM-DD
课程:
源目录:
目标目录:
审查范围:
审查状态: draft

## 一句话结论
## 关键风险清单
## 审查过程复盘
## 高阶课程设计问题
## 重建前必须先做的决策
## 当前目录状态
## 总目录与入口问题
## 最大结构问题
## 逐文件问题记录
### `{file}.html`
- 实际标题:
- 对应 md:
- 对应 mindmap md:
- 是否在总目录:
- 缺失链接/资源:
- `cXXq` 状态:
- 布局状态:
- 源与结果是否分叉:
- 建议处理:
- 优先级:
## Mindmap 状态
## 练习与评价状态
## 资源与图片状态
## 工作建议
## 后续执行原则
## 更新记录
```

Use these stable values where practical:

- `审查状态`: `draft`, `reviewed`, or `active`.
- `建议处理`: `保留`, `修复`, `合并`, `重写`, `退役`, or `后续复查`.
- `优先级`: `P0` for blockers, `P1` for rebuild prerequisites, `P2` for quality improvements.

For each HTML file, record the fixed fields above in the same order. If a field is not applicable, write `无` or `待确认` rather than omitting it.

## Writing Rules

- Be factual first. Separate observed facts from recommendations.
- Say when the audit is incomplete, such as not visually checking browser rendering or not verifying current external technical facts.
- Preserve exact titles read from files. Do not normalize chapter names from memory.
- Do not silently fix problems while auditing.
- Treat the output as a working baseline: include decisions and next steps, not only defects.
- Keep H2 headings consistent across course baselines. Put course-specific detail inside the section body instead of changing the heading text.

## Sync Rule

This slides repo uses both an `a` system and a `c` system. If this skill is updated under `.agents/skills/course-audit/`, mirror the same substantive instructions under `.claude/skills/course-audit/`. The path prefixes may differ, but rules and workflow content should stay equivalent.
