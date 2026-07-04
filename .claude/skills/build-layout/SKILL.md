---
name: build-layout
description: 校验并自动生成 impress.js 幻灯片布局的工具。
---

## 概述

`build-layout` skill 目前包含：

| 工具 | 状态 |
|------|------|
| `check_layout.py` | 可用：校验 OVERLAP/SPACING/BOUNDS/CHAIN BREAK/DEPTH STACK |
| `auto_layout.py` | 可用：读取 YAML 配置生成布局坐标 |

---

## check_layout.py — 布局校验

读取 HTML，解析所有 `.step` div，计算绝对坐标，报告重叠、间距和越界问题。

### 绝对坐标算法

按 DOM 顺序单次扫描，`data-rel-to` 只能指向前面的步骤：

```
prev_abs = (0, 0, 0)
for step in DOM order:
    if has data-x AND data-y:
        abs = (data-x, data-y, data-z)
    elif has data-rel-to="P":
        abs = id_map[P] + (rel-x, rel-y, rel-z)
    else:
        abs = prev_abs
```

### 校验规则

| 规则 | 触发条件 |
|------|---------|
| OVERLAP | 两个步骤同一 (x, y, z) |
| SPACING | \|Δy\| < 1000 且 \|Δx\| < 2000 |
| BOUNDS | x 或 y 超出 ±1500px |
| CHAIN BREAK | `data-rel-to` 引用的 ID 不存在 |
| DEPTH STACK | 两个步骤共享同一 (x, y)，但只靠 z 分开 |

`DEPTH STACK` 是针对 impress.js 3D 视角的额外校验：两个页面即使 `(x, y, z)` 不完全相同，也可能因为同一视线方向上的 z-only 分层而在视觉上互相穿插。只有相邻页面、且 z 差很浅的图片页/细节页叠加通常可以接受；普通内容页应优先用 x/y 间距分开。

### 使用

```bash
python3 .claude/skills/build-layout/check_layout.py 5gai/gai-3-2.html --verbose
```

---

## auto_layout.py — YAML 配置驱动布局生成

读取 YAML 配置文件，计算 impress.js 布局坐标，直接写回 HTML。

### 工作流

1. 生成 HTML（第4步）
2. LLM 读 HTML 内容，起草分支分组
3. 用户审阅分组，确认后写成 YAML 文件
4. 运行脚本：`python3 .claude/skills/build-layout/auto_layout.py {name}.yaml`
5. 浏览器预览验证

### YAML 格式

```yaml
html: 5gai/gai-3-2.html       # 必填，目标 HTML 相对路径
layout_mode: standard         # 可选，布局模式：standard / wrap-title
spacing_y: 1100               # 可选，纵向间距，默认 1100
corridor_x: 2200             # 可选，横向走廊宽度，默认 2200
single_branch_x: 400         # 可选，仅 1 个分支时的视觉补偿 x 偏移
right_branch_extra_x: 600    # 可选，右侧分支额外向右的视觉补偿
mindmap_y: -2000              # 可选，mindmap 相对标题的 y 偏移
mindmap_x: 0                  # 可选，mindmap 相对标题的 x 偏移
wrap_title_inner_y: 1200      # 可选，仅 wrap-title 生效
wrap_title_outer_y: -2000     # 可选，仅 wrap-title 生效
title: c32t                   # 可选，默认用 c\d+t 正则匹配
mindmap: mm32                 # 可选，默认用 mm\d+ 正则匹配
branches:                     # 必填，分支列表
  - name: 工作模式
    steps: [a1, a2, a3, a4]
  - name: 课堂练习
    steps: [a5, a6, a7]
```

### 坐标计算逻辑

- 分支数 n → x 走廊均分：`x_offset[i] = (i - (n-1)/2) × corridor_x`
- 仅 1 个分支时：首个内容页默认不用 `x=0`，而是用 `single_branch_x=400`
- 原因：标题页居中、正文左对齐时，唯一内容组放在 `x=0` 会看起来偏左
- 多分支时：所有右侧分支默认额外应用 `right_branch_extra_x=600`
- 原因：标题页居中、正文左对齐时，几何对称的左右分支在视觉上并不对称，右侧需要略向外推
- `layout_mode: standard`：每分支第一步从 title 出发（`rel-y=spacing_y`，x 为走廊偏移），后续沿链条纵向排列
- `layout_mode: wrap-title`：分支第一步仍从 title 出发，但按标题保护区分两类：
  - **inner**：`|x_offset| <= corridor_x / 2`，第一步 `rel-y = wrap_title_inner_y`（默认 `1200`）
  - **outer**：`|x_offset| > corridor_x / 2`，第一步 `rel-y = wrap_title_outer_y`（默认 `-2000`）
- `wrap-title` 的 inner / outer 判断，使用**原始槽位 x_offset**，不使用右侧视觉补偿后的最终 x
- 原因：`right_branch_extra_x=600` 只负责视觉对称，不应把右内侧分支误判成外侧分支
- 偶数分支（尤其 4 分支）要先按原始槽位区分 `左外 / 左内 / 右内 / 右外`，再应用右侧视觉补偿
- `wrap-title` 的效果是让内容围绕标题页展开，而不是全部压在标题下方
- **图片页**（HTML 含 `<img>` 且无标题）：`rel-z=10`、`rel-y=0`，叠加在前一内容页上
- 普通内容页不得复用同一 `x/y` 后只靠 `z` 分层；这种结构在 overview 或切换过程中容易露出未激活页面，应改用 x/y 走廊或纵向推进
- **mindmap 页**：从 title 出发，固定 `rel-x/rel-y` 偏移
- **导航页**（`cXXq`）：**不修改坐标**，保留手工设置的旋转/缩放

### 两套规则的选择

- `standard`：默认规则，适合大多数现有课件
- `wrap-title`：标题居中，内容环绕，适合希望在 overview 里突出标题中心的页面
- 如果只有 1 个分支且正文左对齐，默认启用 `single_branch_x=400` 做视觉补偿
- 如果有右侧分支且正文左对齐，默认启用 `right_branch_extra_x=600` 做视觉补偿
- 新增或修改布局规则时，至少脑测 `1 / 2 / 3 / 4` 分支四种情况，避免偶数分支误判
- 起草布局草案时，除了确认 `branches`，还应确认 `layout_mode`
- 如果用户未明确说明，默认使用 `standard`

### 校验经验

- `--dry-run` 用来看规则推导出来的坐标是否符合预期
- 正式写回后，若 `check_layout.py` 输出明显反常，必须直接回看 HTML 中实际写入的 `data-rel-to / x / y / z`
- 不要只信校验脚本；脚本异常时，以写回后的 HTML 事实为准继续定位
- `DEPTH STACK` 通常应视为需要修复；只有相邻浅层叠加、且确实用于图片/detail overlay 时，才可作为已知例外保留

### 用法

```bash
# 干跑（只打印坐标，不写入）
python3 .claude/skills/build-layout/auto_layout.py gai-3-2-layout.yaml --dry-run

# 正式运行
python3 .claude/skills/build-layout/auto_layout.py gai-3-2-layout.yaml
```

---

## 与 slides-workflow 的集成

第6步使用 auto_layout.py：生成 YAML → 干跑确认 → 正式运行 → 浏览器验证。
