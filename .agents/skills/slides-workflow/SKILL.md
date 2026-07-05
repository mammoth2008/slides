---
name: slides-workflow
description: Slides 课程单节开发的标准工作流。当用户提到"开始第X节"、"帮我写"、"写好了"、"生成HTML"、"帮我改一下"、"检查md"、"运行SOP"、"生成"、或"mindmap"、"思维导图"等任何涉及课程节开发的工作时，必须使用此工作流。即使用户没有明确说"工作流"也适用。无论哪个课程（PMI、GAI、ITPM等）均使用此工作流。
---

## 课程目录映射

Markdown 源稿已经从本 repo 的 `draft/` 迁入课程资料库：
`/Users/Freeman/Documents/products/courses/library/texts/`。

本 repo 现在主要保留生成后的 HTML、课程图片资源、生成器、布局工具和发布站点框架。`draft/` 已移出发布根目录；归档副本位于 `archive/draft-20260704/`，只作回退参考，不再作为新工作的长期源目录。

| 课程 | 源包 | 课件 md 子目录 | mindmap md 子目录 | 目标目录 | 生成脚本 |
|---|---|---|---|---|---|
| PMI | `pmi-slide-drafts/` | `slide-drafts/` | `mindmaps/` | `10pmi/` | `generate_html.py` |
| GAI | `gai-slide-drafts/` | `slide-drafts/` | `mindmaps/` | `5gai/` | `generate_html.py` |
| ITPM | `itpm-slide-drafts/` | `slide-drafts/` | 无固定目录 | `3itpm/` | `generate_html.py` |
| ITA | `ita-slide-drafts/` | `slide-drafts/` | `mindmaps/` | `6ita/` | `generate_html.py` |
| IL | `il-slide-drafts/` | `slide-drafts/` | 无固定目录 | `8il/` | `generate_html.py` |
| CCIoT | `cciot-slide-drafts/` | `slide-drafts/` | `mindmaps/` | `2cciot/` | `generate_html.py` |
| DBPA | `dbpa-slide-drafts/` | `slide-drafts/` | `mindmaps/` | `1dbpa/` | `generate_html.py` |
| FIIoT | `fiit-slide-drafts/` | `slide-drafts/` | `mindmaps/` | `9fiit/` | `generate_html.py` |
| 其他 | `{course}-slide-drafts/` | `slide-drafts/` | `mindmaps/` | `{course}/` | `generate_html.py` |

> 新增课程时需同步更新本映射。

## 文本主课件与图片化课件

结果页分为两类：

- **文本主课件**：以课程名前缀命名，如 `pmi-*`、`gai-*`、`dbpa-*`
- **图片化课件**：在对应文本主课件基础上进行图片化改造，文件名前缀为 `g{course}`，如 `gpmi-*`、`ggai-*`、`gdbpa-*`

约束如下：

- `md` 仍只对应文本主课件，图片化课件不另设一套源 `md`
- 图片化课件通常沿用对应文本主课件的 slide 顺序、`mindmap`、`cXXq` 与练习页结构
- 图片化课件的工作重点是视觉改造、图片链路导航修复，以及上一节和总导航页的回补

## 全局设计尺寸

所有课程的新视觉设计、封面背景、图片化课件和投影优先 QA，统一以 **1280×960（4:3）** 为主设计尺寸。

- `1280×960` 是新设计基准；`1024×768` 只作为旧页面兼容尺寸。
- `1280×720` / 16:9 只用于网络复习场景的兼容检查，不作为主设计比例。
- 背景图、封面图、图片化正文图默认按 `1280×960` 生产；更高分辨率也必须保持 4:3。
- 重建课程时，应逐步把 HTML 的 `data-width/data-height`、CSS 安全区和图片资产统一到 1280×960 体系；如果暂时沿用旧 1024×768 坐标，应明确是兼容处理。

## 标准工作流（7步）

### 第1步：确认源文件
- md 源码必须在课程资料库的 `library/texts/{course}-slide-drafts/` 下，不是在目标 HTML 目录
- 文本主课件优先读 `slide-drafts/`，mindmap 读 `mindmaps/`，课程设计/材料/任务按源包内分层读取
- 不再把 `draft/{course}/` 当作长期源；如果旧流程临时需要对照旧稿，只读 `archive/draft-20260704/`，不要恢复为长期源
- 告知用户文件路径和所在课程
- 如需新增图片、SVG、mindmap 等资源，统一放在目标课程目录的 `img/cNN/` 下，`NN` 为章节号

### 第2步：Markdown SOP 检查
- **读取** `references/markdown-sop.md` 的检查清单（共11项）
- 对照清单逐项核对当前 md 文件
- 有问题停下，等用户修正后再继续
- **不得跳过此步**

### 第3步：等待用户审阅（硬性规则）
- 将 md 内容摘要告知用户，明确说明"请审阅"
- **未经用户明确同意，不得进入第4步**
- 典型信号：
  - "好"、"可以"、"审阅通过" → 继续
  - 任何修改意见 → 等修正后重新从第2步开始

### 第4步：生成 HTML
- 参照上方映射表确定目标目录和生成器
- 使用统一生成脚本，传入课程资料库中的 md 路径；脚本会按课程配置直接写入目标课程目录
- 推荐命令：
  `python3 .agents/skills/slides-workflow/scripts/generate_html.py --course gai /Users/Freeman/Documents/products/courses/library/texts/gai-slide-drafts/slide-drafts/gai-3-2.md`
- 课程目录下旧的 `*hg.py` 仅作为兼容 wrapper；新工作不要再新增每课一个 HG 文件
- 如果使用尚未更新的旧生成器，可能需要临时复制 md 到兼容目录；这种副本不得成为长期源

### 第5步：移动到目标目录
- 正常情况下 HTML 应直接生成到对应目标目录
- 如果旧生成器仍把 `.html` 写到旧 `draft/{course}/` 路径或课程资料库源包中，必须立即移动到对应目标目录
- 旧 `draft/{course}/` 路径和课程资料库源包下都不得保留生成后的 `.html` 残留文件
- 如果有新增图片，只同步图片资源，不保留错误位置的副本

### 第6步：应用布局

使用 `auto_layout.py`，流程如下：

1. **阅读 HTML 内容** — LLM 读取生成的 HTML，分析幻灯片结构和内容，确定分组依据
2. **起草分组草案** — LLM 根据内容规划分支分组（每个分支对应一个知识模块），给出初步草案
3. **用户审阅** — 告知用户草案内容（每分支含名称和 step 列表），并确认采用哪套布局规则（默认 `standard`，可选 `wrap-title`）
4. **写成 YAML** — 用户确认后，按 `auto_layout.py` 格式写入 YAML 文件
5. **干跑确认** — `python3 .agents/skills/build-layout/auto_layout.py {name}.yaml --dry-run`，打印坐标预览
6. **正式运行** — 确认无误后运行 `python3 .agents/skills/build-layout/auto_layout.py {name}.yaml`，生成布局
7. **浏览器验证** — `open {html_path}` 预览，用 `check_layout.py --verbose` 确认结构风险

布局规则（供参考）：同分支 y 间距 ≥1000px，分支走廊 x 间距 ≥2000px，±1500px 包围框。
如果只有 1 个内容分支，默认将首个内容页放在 `rel-x=400`，而不是 `0`，以补偿标题居中、正文左对齐造成的视觉偏左。
如果存在右侧分支，默认将右侧分支额外再向右补偿 `600px`，避免标题居中、正文左对齐时左右组在 overview 中看起来不对称。
`wrap-title` 判断内侧/外侧时，使用分支的原始槽位 `x`，不使用右侧视觉补偿后的最终 `x`；否则 4 分支等偶数布局里，右内侧分支会被误判到标题页外侧。
新增或修改布局规则时，至少脑测 `1 / 2 / 3 / 4` 分支四种情况；正式写回后若校验结果异常，必须回看 HTML 中实际写入的坐标，不能只信脚本输出。
普通内容页不得放在同一 `x/y` 后只靠 `z` 远近分开；这种 z-only 深度堆叠会让未激活页面在 3D 视角中穿插出来。只有相邻页面、且 `rel-z` 很浅的图片页/细节页叠加通常可接受。

### 第7步（不可跳过）：修复导航
- 找到生成的 cXXq 页面，修复三项内容：
  1. **思考题**：替换占位符 `-` 为实际思考题
  2. **nav 链接**：中间指向上级 `{course}-exec.html`（PMI → pmi-exec.html，GAI → gai-exec.html，以此类推）；左侧指向前一节；右侧指向后一节
  3. **标题核对**：读取目标文件的原始标题原文，**原样写回，不篡改**
- 如果只是修改 `cXXq` 导航页，**优先按 `div id` 整块替换**：先定位 `id="cXXq"` 的整块 `div`，再整块替换思考题和左右导航；不要靠正文片段猜位置，因为 `-`、链接文案、空行都容易变化。

### 修改后重生成清单
- 只要本次修改涉及 **slide 拆分、合并、改序、删除整页、移动图片页**，就不要试图硬改结果 html，直接重生成。
- 重生成前，先查看当前稳定版 html 中的 `cXXq`，记下：
  1. 思考题三条
  2. 左导航标题与链接
  3. 右导航标题与链接
- 先改课程资料库中的源 `md`；如果结构摘要变了，mindmap `md` 也要同步改。
- 运行生成器后，如果临时 html 落在旧 `draft/{course}/` 路径或源包目录，**立刻移动**到目标课程目录，不留残留文件。
- 然后按顺序执行：
  1. 重跑 layout
  2. 恢复 `cXXq`
  3. 如本节有独立练习页, 同步检查并更新对应 `exec html`
  4. 运行 `check_layout.py --verbose`
- 恢复 `cXXq` 时，优先按 `id="cXXq"` 锚定整块 `div`，不要靠正文片段做零碎替换。
- 对 `PMI` 课程还有一条额外规则：更新分节 `exec html` 时，除从当前小节内容提炼题目外，还要检查 `3itpm/itpm-exec.html` 是否有适合当前小节的题
- `ITPM` 题库只作补充源：只能加入与当前 `PMI` 小节概念同构、不会提前越界到后续章节、且不需要大幅改题干语境的题；不为凑题数硬加
- 边界复杂的小节更要少量补充：像 `5.4` 这种同时覆盖风险、采购、干系人的小节，练习页应以本节内容为主，`ITPM` 只补少量同构题；不要把合同法、政府采购法等细节题整段搬入本节练习页
- 单节练习页题量按内容完整和课堂节奏决定，不固定为 `8` 题；`5-15` 题通常都可接受，不要机械凑题数
- 判断标准：
  - `OVERLAP` 和 `CHAIN BREAK` 不能接受
  - `DEPTH STACK` 通常需要修复；只有相邻浅层图片/detail overlay 可以作为已知例外
  - 图片页同视口导致的 `SPACING` 提示通常是预期行为
  - `BOUNDS` 是否接受，要结合当前课程既有布局风格判断

## 单节扩展经验

### 内容组织

- **桥接节只做桥接**：像 `3.3` 这类承上启下的小节，重点是把下一章需要的概念引出来，不要提前把后续章节讲完。
- **总览章要持续回看总地图**：像 PMI 第五章这种按经典知识领域分节展开的总览章，写后续小节时要反复回看 `5.1` 的整体地图，避免只盯小节标题而漏掉本章应讲完的完整对象集合。
- **标题与内容边界不一致时，要在正文首页点明**：如果章节标题少写了一项、而课程设计或内容栏实际承担更多内容，正文第一页就应直接说明，不要指望学生从上下文自行推断。
- **课件表述要稍正式、体系化**：不要写成口语化、像随口列几个要点；即使保持简洁，也要有课程 slides 应有的结构感、判断框架和术语边界。
- **专业场景优先上提到底层流程**：如果内容很容易写成"某专业学生如何如何"，优先改写成"AI 改变了什么流程和结果"，这样更稳。
- **优先选择桥梁案例**：数据获取、清洗、分析、摘要这类案例，适合连接辅助编程、信息管理、`workflow` 和判断力。

### 图片与插页

- **图片优先补抽象结构**：执行闭环、信息流程、数据流程、能力组成，这些位置比产品截图更值得优先加图。
- **没有合适现成图时，可直接自绘 SVG**：放到对应课程的 `img/cNN/` 下，便于长期复用。
- **md 中资源路径写目标目录相对路径**：例如第四章图片写成 `img/c04/example.svg`，不要写 `draft/` 路径。
- **图片 slide 必须同步写回 md**：即使当前只手改 html，不重生成，也要把 `![图](path) + #### 图片标题` 同步写回源 md。
- **图片页文字不要后贴说明框**：标题、正文要点、标签应长在画面里的牌匾、站牌、票据、地图、任务板、说明纸等实体上；不要做成独立漂浮的后贴面板。
- **图片页先判断“文字是否属于这个场景”**：不只检查字体是否清楚，更要检查文字和视觉语境是否协调。
- **案例图必须显式区分概念层次**：如果案例同时承载两层对象，如 `礼制节点` 和 `管理阶段`，要在图中直接分层，不要只给氛围。
- **图片化课件图片默认按 `1280×960` 设计**：这是所有课程的新主设计尺寸；并把原 slides HTML 里的关键文字做得更大，帮助投影环境下快速识别重点。
- **图片化课件不得用 SVG 重制原有 HTML 文本页**：图片化过程应使用 OpenAI `image 2` 模型生成高质量 `png`，再用这些图片完整替代原有 HTML 中正文 `div` 的文本内容。SVG 只适用于普通课件的结构示意图、流程图等前端资源，不作为图片化课件正文页的重制方案。
- **图片化课件全量生产前先做试片**：优先先做 `2-3` 张，至少覆盖标题页、概念定义页、案例页，确认文字关系和风格方向后再批量生成。
- **批量出图后先按生成时间映射文件**：先根据生成顺序把原图对应到 `a1/a2/...`，再抽查关键页，通常比逐张猜文件名更稳。

### 手改 HTML 的边界

- **只做局部增量时，可直接手改 HTML**：插图、补说明、微调措辞，且不改主结构顺序时，可以不重生成。
- **新增图片页可用卢曼式编号**：插在 `a5` 后的新图页可记为 `a5a`。
- **图片页与前页保持同视口**：通常设 `data-rel-to` 指向前页，`data-rel-x=0`，`data-rel-y=0`，`data-rel-z=10`。
- **普通内容页不要只靠 z 分层**：同一 `x/y` 的深度堆叠容易在 3D 视角中互相穿插；除相邻浅层图片/detail overlay 外，应使用 x/y 间距组织页面。
- **进度条使用 impress.js 原生结构**：底部进度条应保留 `<div class="impress-progressbar"><div></div></div>` 与 `<div class="impress-progress"></div>`，由 impress.js 自动写入宽度和页码；不要改成静态自定义 `.progressbar`。
- **替换图片资源时，同步修改 md 与结果 HTML 的路径**：如果当前只是把结果 html 里的图片从 `svg` 改成 `png`、或切换到新资源文件，而不立即重生成，也必须把源 `md` 的同一图片路径一起改掉；否则下次生成会把结果覆盖回旧资源。
- **图片化课件结果页优先以对应文本主课件为骨架改写**：如 `g{course}-*.html` 优先从 `{course}-*.html` 转换，正文 slide 替换为图片页，保留 `mindmap` 和 `cXXq`，单独修导航。
- **图片化课件新增一节后要回补旧链接**：除了当前页的 `cXXq`，还要检查上一节图片化页面的右导航，以及图片化总导航页是否应切到新的 `g{course}-*`。
- **批量替换若弄脏 `div` 边界，直接重写 block**：不要在坏掉的结构上零碎修补，回到原始文本主课件页按 block 重新替换更稳。

## 关键警告

### ⚠️ 生成器每次重置一切
运行生成器会覆盖：所有布局坐标（`data-rel-x/y/z`）、cXXq 思考题和导航链接。
**每次生成后必须完整执行第5步到第7步，不得跳过。**

### ⚠️ draft 目录不留 html 残留
旧生成器可能先把 `.html` 写到旧 `draft/{course}/` 路径或源 md 所在目录。
**正确做法**：生成后立刻移动到目标课程目录。
**错误做法**：复制一份到目标目录后，让旧 `draft/` 路径或课程资料库源包下残留旧 `.html`。

### ⚠️ layout 输出格式要求
`auto_layout.py` 生成的 div 最后一行必须是：
```
    data-rel-z    = {rz}>
```
注意 `>` 后有**一个空行**，然后才是幻灯片内容。漏掉 `>` 或漏掉空行会导致 impress.js 渲染失败。

### ⚠️ 链式偏移累积
用 `auto_layout.py` 生成的布局不会出现此问题。但如果 YAML 配置有误（如 `data-rel-to` 指向错误），偏移会沿链条叠加。
**正确做法**：分叉跳转时，将 `data-rel-to` 重定向到分叉入口点，并设 `rel-y=0`。

### ⚠️ nav 标题不篡改
读取了文件的原始标题后，写入导航页时必须原样使用。
**错误**：读了"2.2 多模态内容生成"，写入时改成"AIGC 的典型应用"。
**正确**：读到什么，就写什么。

## 辅助工具

### build-layout（独立 skill）
处理 impress.js 布局的校验和自动生成。完整文档见 `.agents/skills/build-layout/SKILL.md`。

用于 slides-workflow 第6步。

### course_map.py
扫描项目结构，返回当前有哪些课程、各课程的 md 文件列表、目标目录是否存在。
用于第1步确认目录。

### chinese-fix.py
按 `references/markdown-sop.md` 的标点/空格规则自动修复 md 文件。

### generate_html.py
统一从 courses vault 的源 md 生成 impress.js HTML，输出到配置的目标课程目录。课程目录下旧 `*hg.py` 只做兼容转发，不再作为长期生成器维护入口。
使用方式：`python3 .agents/skills/slides-workflow/scripts/generate_html.py --course gai <source.md>`
使用方式：`python3 .agents/skills/slides-workflow/chinese_fix.py {filename.md}`

---

## Mindmap 工作流

### 前提：mindmap-md 是独立文件

**课件 md 不能直接生成 mindmap。** 原因：课件 md 的 `###` 是幻灯片级别（一页一页），而 mindmap 需要知识层级（主题→子主题→要点）。两者结构不同，需要人工提炼。

Mindmap md 文件（`{course}-N-N-mindmap.md` 或 `mindmap-N-N.md`）是对课件 md 的**知识结构重组**，放在课程资料库源包的 `mindmaps/` 目录下。

### Mindmap md 格式

```markdown
# 章节标题（根节点）

## 主要知识模块 A

### 子主题 A1
- 具体要点
- 具体要点

### 子主题 A2
- 具体要点

## 主要知识模块 B
- 如果模块 B 无子主题，直接写条目
- 条目二
```

规则：
- `#` — 根节点（整张图的核心，通常就是章节名）
- `##` — 一级分支（主要知识模块，对应一组相关幻灯片）
- `###` — 二级分支（子主题）
- `-` — 叶子节点（具体知识点）
- 层级控制在 4 层以内（`#`/`##`/`###`/`-`）

### 工作流

```
第1步：Codex 读课件 md，起草 mindmap-md 初稿
        → 读课程资料库中对应的课件 md 全文
        → 识别核心主题、知识模块、子主题
        → 按 #/##/###/- 层级重组，写出初稿
        → 告知用户"请审阅 mindmap-md 初稿"，等待确认
  ↓
第2步：用户审阅，Codex 按反馈修改，直到用户同意
  ↓
第3步：运行脚本生成 HTML
  python3 .agents/skills/slides-workflow/scripts/mindmap_gen.py \
    /Users/Freeman/Documents/products/courses/library/texts/{course}-slide-drafts/mindmaps/{name}-mindmap.md
  ↓
输出：{course_dir}/img/cNN/mindmap-N-N.html（路径自动推断）
  ↓
第4步：将 mindmap HTML 嵌入课件 HTML
  → 找到课件 HTML 中已有的 mindmap div（id 形如 mmNN）
  → 只替换 src 中的文件名，其余不动
  → 如果没有 mindmap div，按下方模板新增
```

### 嵌入模板

```html
<div id="mmNN" class="step"
    data-rel-to="cNNt"
    data-rel-x="0"
    data-rel-y="-2000"
    data-rel-z    = "0"
    data-rotate-y = "0"
    data-rotate   = "0"
    data-scale    = "1"
    style         = "width: 92vw; height: 92vh; display: flex; justify-content: center; align-items: center;">

    <iframe
    src           = "img/cNN/mindmap-N-N.html"
    style         = "width: 100%; height: 100%; border: none;"
    allowfullscreen>
    </iframe>

    </div>
```

变量说明（固定不变的不用改）：
- `id="mmNN"` — 本节 mindmap 的唯一 ID，如 `mm32`
- `data-rel-to="cNNt"` — 相对于本节标题页，如 `c32t`
- `data-rel-x` / `data-rel-y` — 布局坐标，按实际位置调整
- `src` — 只改文件名，如 `img/c03/mindmap-3-2.html`

### 课件 md 更新后是否重新生成 mindmap

mindmap-md 是独立文件，与课件 md 各自维护。课件 md 更新后，由**用户判断**是否需要同步更新 mindmap。

参考标准：
- 课件改了**措辞/细节**，mindmap 不需要更新
- 课件**新增或删除了知识模块**，mindmap 可能需要更新
- 课件**章节结构重组**，mindmap 大概率需要重新起草

### LLM 起草 mindmap-md 的原则

**读什么**：课程资料库中的课件 md 全文（通常在 `library/texts/{course}-slide-drafts/slide-drafts/`）

**怎么起草**：
1. 找出全节的核心主题（→ `#` 根节点，通常就是章节名）
2. 把幻灯片按知识模块分组（→ `##`），每组对应一个"能回答一类问题"的主题
3. 模块内有子话题则拆一层（→ `###`），否则直接列条目
4. 每条 `-` 只保留核心要点，不照抄幻灯片原文，精简到 12 字以内

**不要做的事**：
- 不要把每张幻灯片的 `###` 标题原封不动搬过来（幻灯片 `###` 是展示顺序，不是知识层级）
- 不要超过 4 层（`#`/`##`/`###`/`-`）
- 不要在同一层放超过 7 个节点（超过时合并或提升层级）
- 未经用户确认不运行脚本

### 脚本命令

```bash
# 基本用法（输出路径自动推断）
python3 .agents/skills/slides-workflow/scripts/mindmap_gen.py \
  /Users/Freeman/Documents/products/courses/library/texts/gai-slide-drafts/mindmaps/gai-3-2-mindmap.md

# 指定输出路径
python3 .agents/skills/slides-workflow/scripts/mindmap_gen.py \
  /Users/Freeman/Documents/products/courses/library/texts/gai-slide-drafts/mindmaps/gai-3-2-mindmap.md \
  -o 5gai/img/c03/mindmap-3-2.html
```

### 路径自动推断规则

脚本根据 mindmap md 的路径推断输出位置：
- `/Users/Freeman/Documents/products/courses/library/texts/gai-slide-drafts/mindmaps/gai-3-2-mindmap.md` → `5gai/img/c03/mindmap-3-2.html`
- 兼容旧路径：`draft/gai/gai-3-2-mindmap.md` → `5gai/img/c03/mindmap-3-2.html`
- 课程前缀映射：`gai→5gai`, `pmi→10pmi`, `itpm→3itpm` 等（见脚本 `COURSE_PREFIXES`）
