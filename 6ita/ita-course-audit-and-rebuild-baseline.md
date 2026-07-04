# ITA Course Audit and Rebuild Baseline

检查日期: 2026-07-04
课程: ITA
源目录: `draft/ita/`
目标目录: `6ita/`
审查范围: `6ita/*.html`, `draft/ita/*.md`, mindmap, navigation, layout, resources
审查状态: draft

## 一句话结论

ITA 当前不是“缺少零散文件”, 而是处在“完整 13 章课程框架 + 少量已落地成品页 + 多个未生成源稿/特殊页”的混合状态。`ita-0.html` 列出 13 章共 55 个 `ita-*.html` 本地入口, 实际只存在 9 个入口目标, 其中正文分节 HTML 只有 8 个。已有正文 HTML 都有对应 md, 但 `draft/ita` 中仍有 `ita-1-2.md`、`ita-3-1.md`、`ita-5-1.md`、`ita-23tasks.md` 没有生成到 `6ita/`。所有正文分节的 `cXXq` 都指向不存在的 `ita-exec.html`, 第 2 章和第 13.1 只有 mindmap 图片或无 mindmap 引用, 没有对应 mindmap md。后续应先裁决下学期 ITA 是否继续沿用 13 章框架, 再决定从哪几章恢复成可讲授版本。

## 关键风险清单

- `ita-0.html` 有 55 个 `ita-*.html` 本地链接, 其中 46 个目标文件不存在。
- `ita-1-2.md`、`ita-3-1.md`、`ita-5-1.md` 有源稿但没有目标 HTML, 导致总目录和分节导航断链。
- 所有正文分节 `cXXq` 都链接到不存在的 `ita-exec.html`。
- `ita-0.html` 使用 `data-rel-z="-0.5w"`, 当前 `check_layout.py` 无法解析, 与 DBPA 总目录存在同类旧布局债务。
- 第 2 章和第 13.1 缺少 mindmap md; 目标目录中只有 `img/c02/mindmap-2-*.png`、`img/c13/mindmap-13-1.png`。
- `class.md`、总目录、现有 md/HTML 的部分标题不完全一致, 后续不能凭记忆统一标题。

## 审查过程复盘

- 读取 `course-audit`、`slides-workflow` 和项目规则, 确认 ITA 映射为 `draft/ita/` -> `6ita/`, 生成器为 `pmihg.py`。
- 扫描 `6ita/`、`draft/ita/`、`6ita/img/` 文件状态。
- 读取 `6ita/ita-0.html` 和 `draft/ita/class.md`, 对照总目录框架、实际 HTML 和源 md。
- 扫描所有 `6ita/*.html` 的标题、`cXXq`、资源引用、重复 id、`data-rel-to`、iframe/mindmap。
- 扫描 `draft/ita/*.md` 的标题、图片路径、SOP 风险、未生成源稿和长列表风险。
- 对 `6ita/*.html` 运行 `check_layout.py --verbose`, 记录布局解析错误、overlap、spacing、bounds、chain break。未进行浏览器视觉审查, 也未联网核验 AI 工具、课程资源和外部链接的时效性。

## 高阶课程设计问题

- 课程定位需要重新确认: `ita-0.html` 的描述是“智能技术及应用”, 面向全日制硕士研究生; 当前内容覆盖人工智能、深度学习、Python、NLP、机器视觉、机器人、IoT、人机交互、商业应用、伦理法律, 范围很大。
- 下学期教学目标需要取舍: 总目录写有“构建个人专用的智能技术工具组”, 但很多章节仍是传统 AI 技术综述, 需要决定是以工具能力、概念框架、研究阅读、还是项目交付为主线。
- 13 章框架可能过宽: 对研究生课程而言, 深度学习数学、Python 基础、框架技术、NLP、视觉、机器人、IoT、人机交互、商业应用和伦理法律全部展开, 很容易变成目录型课程。
- 课程内容时效性风险高: ChatGPT、Claude、Midjourney、Stable Diffusion、New Bing、Sora、AIGC 工具列表、MOOC 与外部 PDF 链接都需要重新核验。
- 评价体系尚未闭合: 有任务页和 presentation/报告要求, 但没有统一 `ita-exec.html`, 也没有看到从每章学习目标到作业、展示、考试的映射。
- 资源来源和版本需要重新审查: 课程有大量图片、视频、工具链接、教材 PDF 和云端资源, 但本轮未看到来源、授权、版本、替代方案记录。
- 生成契约不完整: 部分特殊页没有 md 源, 第 2 章/13.1 缺 mindmap md, 旧总目录布局无法被当前 checker 解析, 后续如果重生成会很难稳定复现。

## 重建前必须先做的决策

1. 确定下学期 ITA 是否继续使用 13 章全框架, 还是压缩为若干教学模块。
2. 确定课程主线: “智能技术工具组”, “人工智能基础与应用”, “生成式 AI 工作流”, “研究生文献/案例研讨”, 或混合方案。
3. 确定第 1-2 章的恢复优先级: 是先补 `ita-1-2.html`, 还是直接进入第 2 章/生成式 AI/工具实践。
4. 确定练习与评价入口: 补建统一 `ita-exec.html`, 还是改为任务页/章节作业页。
5. 确定特殊页地位: `ita-case.html`、`ai-tools.html`、`ita-24tasks.html`、`ita-24-fall-tasks.html` 是保留、归档、还是重写为下学期任务页。
6. 确定 mindmap 策略: 第 2 章和第 13.1 是恢复 mindmap md, 还是退役现有 PNG mindmap。
7. 确定外部资源刷新策略: 教材、MOOC、AI 工具、云端模板和 PDF 是否仍可访问、是否仍适合课程。

## 当前目录状态

- 目标目录 `6ita/` 中正文分节 HTML: `ita-1-1.html`, `ita-1-3.html`, `ita-1-4.html`, `ita-2-1.html`, `ita-2-2.html`, `ita-2-3.html`, `ita-2-4.html`, `ita-13-1.html`。
- 目标目录特殊 HTML: `ita-0.html`, `ita-case.html`, `ita-src.html`, `ai-tools.html`, `ita-24tasks.html`, `ita-24-fall-tasks.html`。
- 源目录正文/任务 md: `ita-1-1.md`, `ita-1-2.md`, `ita-1-3.md`, `ita-1-4.md`, `ita-2-1.md`, `ita-2-2.md`, `ita-2-2-lecture.md`, `ita-2-3.md`, `ita-2-4.md`, `ita-3-1.md`, `ita-5-1.md`, `ita-13-1.md`, `ita-23tasks.md`, `ita-case.md`。
- 其他源材料: `aiqa.md`, `class.md`, `ideas.md`, `lecture.md`, `slides-prompt.md`。
- 已有 mindmap md: `mindmap-1-1.md`, `mindmap-1-2.md`, `mindmap-1-3.md`, `mindmap-1-4.md`。
- 已有目标 mindmap 资源: `img/c01/mindmap-1-1.html` 至 `mindmap-1-4.html`, `img/c02/mindmap-2-1.png` 至 `mindmap-2-4.png`, `img/c13/mindmap-13-1.png`。
- `draft/ita` 下未发现生成残留 HTML。

## 总目录与入口问题

- `ita-0.html` 是完整 13 章入口, 但 55 个 `ita-*.html` 本地链接中只有 9 个存在, 46 个缺失。
- 第 1 章缺 `ita-1-2.html`; 这会同时断开总目录入口、`ita-1-1.html` 下一节、`ita-1-3.html` 上一节。
- 第 3-12 章基本只有总目录框架, 没有对应目标 HTML; 其中 `draft/ita/ita-3-1.md` 与 `draft/ita/ita-5-1.md` 已有源稿但未生成。
- 第 13 章只有 `ita-13-1.html`, 缺少 `ita-13-2.html` 至 `ita-13-4.html`; `ita-13-1.html` 的左右导航也指向缺失页面。
- `ita-0.html` 课程框架与 `draft/ita/class.md` 大体一致, 但存在标题差异, 例如 `class.md` 的 `2.2 神经网络的诞生与发展` 与现有 md/HTML 的 `2.2 多层神经网络的诞生与发展` 不完全一致。
- `ita-0.html` 使用 `data-rel-z="-0.5w"`, 导致 `check_layout.py` 无法完成解析。

## 最大结构问题

最大结构问题是课程架构和已落地课件之间严重不对称: 总目录表达的是一门 13 章、覆盖面极宽的完整研究生课程, 但实际可讲授的成品页主要集中在第 1 章、第 2 章和第 13.1。与 DBPA 不同, ITA 不是大量 HTML 无源; 与 CCIOT 不同, ITA 也不是正文基本齐全但入口漏章。它的问题是“目标课程框架远大于已完成课件资产”, 并且练习、mindmap、特殊任务页和资源页没有形成统一教学闭环。

## 逐文件问题记录

### `ita-0.html`

- 实际标题: `智能技术及应用`
- 对应 md: 不适用
- 对应 mindmap md: 不适用
- 是否在总目录: 不适用
- 缺失链接/资源: 46 个 `ita-*.html` 入口目标缺失, 包括 `ita-1-2.html`, `ita-3-1.html` 至 `ita-12-3.html`, `ita-13-2.html` 至 `ita-13-4.html`
- `cXXq` 状态: 未发现 `cXXq`
- 布局状态: `check_layout.py` 无法解析 `data-rel-z="-0.5w"`
- 源与结果是否分叉: 待确认; 与 `class.md` 存在若干标题差异
- 建议处理: 重写
- 优先级: P0

补充记录:

- 当前总目录仍可作为课程范围参考, 但不能作为下学期可用入口。
- 重建前应先决定是否保留 13 章框架。

### `ita-1-1.html`

- 实际标题: `1. 人工智能技术概述 / 1.1 人工智能的概念与基础`
- 对应 md: `draft/ita/ita-1-1.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-1-1.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `ita-1-2.html`, `ita-exec.html`
- `cXXq` 状态: `c11q` 存在, 有 4 个问题; 下一节与练习链接断开
- 布局状态: `check_layout.py` 报 92 个问题: 15 overlap, 44 spacing, 33 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:

- 本节内容与资源基础完整, 但依赖缺失的 `ita-1-2.html`。
- 后续应先补齐 1.2 或调整导航。

### `ita-1-3.html`

- 实际标题: `1. 人工智能技术概述 / 1.3 人工智能的技术流派`
- 对应 md: `draft/ita/ita-1-3.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-1-3.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `ita-1-2.html`, `ita-exec.html`
- `cXXq` 状态: `c13q` 存在, 有 5 个问题; 上一节与练习链接断开
- 布局状态: `check_layout.py` 报 121 个问题: 1 overlap, 48 spacing, 72 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:

- 本页规模很大, step 数量较多, 需要后续结合课堂节奏判断是否拆分或压缩。

### `ita-1-4.html`

- 实际标题: `1. 人工智能技术概述 / 1.4 人工智能的发展现状与应用`
- 对应 md: `draft/ita/ita-1-4.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-1-4.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `ita-exec.html`
- `cXXq` 状态: `c14q` 存在, 有 4 个问题; 练习链接断开, 下一节到 `ita-2-1.html` 正常
- 布局状态: `check_layout.py` 报 29 个问题: 14 spacing, 15 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:

- 内容主题容易受技术发展影响, 后续需核验 AI 应用分类和案例时效性。

### `ita-2-1.html`

- 实际标题: `2. 机器学习与深度学习 / 2.1 机器学习的概念与原理`
- 对应 md: `draft/ita/ita-2-1.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-2-1.md` 缺失
- 是否在总目录: 是
- 缺失链接/资源: `ita-exec.html`
- `cXXq` 状态: `c21q` 存在, 有 4 个问题; 练习链接断开
- 布局状态: `check_layout.py` 报 53 个问题: 5 overlap, 26 spacing, 22 bounds
- 源与结果是否分叉: mindmap 源链不完整
- 建议处理: 修复
- 优先级: P0

补充记录:

- 目标目录存在 `img/c02/mindmap-2-1.png`, 但没有 mindmap md。
- 源 md 中 `### 重点事件` 粗略计数有 9 条列表, 后续应拆分或压缩。

### `ita-2-2.html`

- 实际标题: `2. 机器学习与深度学习 / 2.2 多层神经网络的诞生与发展`
- 对应 md: `draft/ita/ita-2-2.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-2-2.md` 缺失
- 是否在总目录: 是
- 缺失链接/资源: `ita-exec.html`
- `cXXq` 状态: `c22q` 存在, 有 6 个问题; 练习链接断开
- 布局状态: `check_layout.py` 报 58 个问题: 3 overlap, 22 spacing, 33 bounds
- 源与结果是否分叉: mindmap 源链不完整; `class.md` 标题为 `2.2 神经网络的诞生与发展`
- 建议处理: 修复
- 优先级: P0

补充记录:

- 存在 `draft/ita/ita-2-2-lecture.md`, 但该文件使用 `##` 结构, 更像讲稿素材, 不应直接作为 slide md。

### `ita-2-3.html`

- 实际标题: `2. 机器学习与深度学习 / 2.3 深度学习的原理与应用`
- 对应 md: `draft/ita/ita-2-3.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-2-3.md` 缺失
- 是否在总目录: 是
- 缺失链接/资源: `ita-exec.html`
- `cXXq` 状态: `c23q` 存在, 有 6 个问题; 练习链接断开
- 布局状态: `check_layout.py` 报 55 个问题: 1 overlap, 19 spacing, 35 bounds
- 源与结果是否分叉: mindmap 源链不完整
- 建议处理: 修复
- 优先级: P0

补充记录:

- 本节围绕 Transformer/self-attention, 技术时效性和数学表达需要后续复核。

### `ita-2-4.html`

- 实际标题: `2. 机器学习与深度学习 / 2.4 深度学习的现状与不足`
- 对应 md: `draft/ita/ita-2-4.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-2-4.md` 缺失
- 是否在总目录: 是
- 缺失链接/资源: `ita-3-1.html`, `ita-exec.html`
- `cXXq` 状态: `c24q` 存在, 有 5 个问题; 下一节与练习链接断开
- 布局状态: `check_layout.py` 报 41 个问题: 18 spacing, 23 bounds
- 源与结果是否分叉: mindmap 源链不完整
- 建议处理: 修复
- 优先级: P0

补充记录:

- `draft/ita/ita-3-1.md` 已存在, 因此下一步可优先生成或重建 3.1, 但必须先审阅 md。

### `ita-13-1.html`

- 实际标题: `13. 智能技术的伦理与法律问题 / 13.1 法律责任的变化: 自动驾驶`
- 对应 md: `draft/ita/ita-13-1.md` 存在
- 对应 mindmap md: `draft/ita/mindmap-13-1.md` 缺失
- 是否在总目录: 是
- 缺失链接/资源: `ita-12-3.html`, `ita-13-2.html`, `ita-exec.html`
- `cXXq` 状态: `c131q` 存在, 有 5 个问题; 上一节、下一节、练习链接均断开
- 布局状态: `check_layout.py` 报 67 个问题: 31 spacing, 36 bounds
- 源与结果是否分叉: mindmap 源链不完整; `class.md` 标题为 `13.1 法律责任的变化——以自动驾驶为例`
- 建议处理: 修复
- 优先级: P0

补充记录:

- 这是从第 13 章跳出的独立成品页, 课程顺序上与现有第 2 章之后的内容断裂。

### `ita-case.html`

- 实际标题: `AIGC / Artificial Intelligence Generated Content`
- 对应 md: `draft/ita/ita-case.md` 存在
- 对应 mindmap md: 不适用
- 是否在总目录: 否
- 缺失链接/资源: HTML 中未发现缺失; 但源 md 中有 13 项图片路径在目标目录缺失, 包括 `img/c00/newbing.jpg`, `img/c00/newbing1.jpg`, `img/c00/ai-mj.jpg`
- `cXXq` 状态: `c00q` 存在, 有 5 个问题; 只回总目录, 没有练习链接
- 布局状态: `check_layout.py` 报 102 个问题: 9 overlap, 43 spacing, 44 bounds
- 源与结果是否分叉: 是, 源 md 与当前 HTML 资源引用不一致
- 建议处理: 后续复查
- 优先级: P1

补充记录:

- AIGC 工具和案例页可能仍有课程价值, 但需要作为专题页重新定位, 并修复 md 与 HTML 分叉。

### `ita-src.html`

- 实际标题: `其它课本`
- 对应 md: 不适用
- 对应 mindmap md: 不适用
- 是否在总目录: 是
- 缺失链接/资源: 本地缺失无; 外部资源未联网核验
- `cXXq` 状态: 未发现 `cXXq`
- 布局状态: `check_layout.py` 报 5 个问题, 其中 1 个 chain break; `textbook` 的 `data-rel-to=""` 是问题源
- 源与结果是否分叉: 手写资源页, 无 md 源
- 建议处理: 修复
- 优先级: P1

补充记录:

- 教材、MOOC、工具链接含外部资源, 后续需要核验可访问性和课程适配性。

### `ai-tools.html`

- 实际标题: `AI 工具列表`
- 对应 md: 待确认
- 对应 mindmap md: 不适用
- 是否在总目录: 否
- 缺失链接/资源: 本地缺失无; 外部工具链接未联网核验
- `cXXq` 状态: 未发现 `cXXq`
- 布局状态: `check_layout.py` 报 1 个 spacing 问题
- 源与结果是否分叉: 无对应 md, 需决定是否恢复源
- 建议处理: 后续复查
- 优先级: P2

补充记录:

- 工具列表明显过时风险较高, 但可作为下学期工具清单重建的旧资产。

### `ita-24tasks.html`

- 实际标题: `第六周周四 / 第八周周四 提交个人报告`
- 对应 md: `draft/ita/ita-24tasks.md` 缺失
- 对应 mindmap md: 不适用
- 是否在总目录: 否
- 缺失链接/资源: 本地缺失无
- `cXXq` 状态: 未发现 `cXXq`
- 布局状态: `check_layout.py` 报 6 个问题, 其中 2 个 chain break; `a1a` 指向不存在的 `a3`, `a1b` 指向不存在的 `a3a`
- 源与结果是否分叉: 无对应 md, 属于 HTML-only 任务页
- 建议处理: 后续复查
- 优先级: P1

补充记录:

- 这是 2024 fall 任务页, 是否继续使用取决于下学期作业设计。

### `ita-24-fall-tasks.html`

- 实际标题: `第四周周四 / 第六周周四 提交个人报告`
- 对应 md: `draft/ita/ita-24-fall-tasks.md` 缺失
- 对应 mindmap md: 不适用
- 是否在总目录: 否
- 缺失链接/资源: 本地缺失无
- `cXXq` 状态: 未发现 `cXXq`
- 布局状态: `check_layout.py` 报 6 个问题, 其中 2 个 chain break; `a1a` 指向不存在的 `a3`, `a1b` 指向不存在的 `a3a`
- 源与结果是否分叉: 无对应 md, 属于 HTML-only 任务页
- 建议处理: 后续复查
- 优先级: P1

补充记录:

- 与 `ita-24tasks.html` 内容相近但时间与模板链接不同, 后续应合并或归档其中一个。

## Mindmap 状态

- 第 1 章 mindmap 源链相对完整: `mindmap-1-1.md` 至 `mindmap-1-4.md` 存在, 目标 HTML 也存在。
- `mindmap-1-2.md` 与 `img/c01/mindmap-1-2.html` 存在, 但 `ita-1-2.html` 缺失。
- 第 2 章没有 `mindmap-2-1.md` 至 `mindmap-2-4.md`, 目标目录只有 `img/c02/mindmap-2-*.png`。
- `ita-2-1.html` 至 `ita-2-4.html` 当前未发现 iframe mindmap, 即使图片存在也没有按第 1 章方式接入。
- 第 13.1 没有 `mindmap-13-1.md`, 目标目录只有 `img/c13/mindmap-13-1.png`。
- 第 3 章以后大部分没有 mindmap 源或目标资源。

## 练习与评价状态

- `ita-exec.html` 不存在, 但所有正文分节 `cXXq` 的中间链接都指向它。
- 目标目录存在 `ita-24tasks.html` 和 `ita-24-fall-tasks.html`, 但它们是任务说明页, 不是按章节组织的练习页。
- `ita-0.html` 写有“课堂讨论 + 分组辩论”“分组调研 + Presentation”“平时成绩 + 期末闭卷考试”, 但 baseline 中还没有看到这些评价方式与每章内容之间的映射。
- `draft/ita/ita-23tasks.md` 存在, 但没有对应目标 HTML; 任务页版本之间需要统一。

## 资源与图片状态

- `6ita/img/c00`, `c01`, `c02`, `c13` 资源很丰富, 但来源、版权、版本、是否仍适合下学期教学均未审查。
- `draft/ita/ita-case.md` 中有多项图片路径在目标目录不存在, 而 `ita-case.html` 中没有本地缺失, 说明该专题页存在源/结果分叉。
- `ita-src.html` 中教材 PDF、MOOC、工具链接全部是外部链接, 本轮未联网核验。
- `ai-tools.html` 中工具清单内容明显依赖当前工具生态, 后续必须更新。
- `draft/ita/ita-5-1.md` 包含一个指向 `https://chat.openai.com/chat?model=gpt-4` 的图片链接, 不适合作为长期图片资源。

## 工作建议

1. 先裁决课程结构: 保留 13 章框架、压缩为 6-8 个模块, 或改成“智能工具/生成式 AI 工作流 + 关键技术解释 + 伦理法律”的新结构。
2. 先补入口闭环: 如果保留第 1-2 章, 优先处理 `ita-1-2.md` -> `ita-1-2.html`, 并修复第 1 章导航链。
3. 先决定是否补建 `ita-exec.html`: 如果继续使用统一练习入口, 这是 P0; 如果改为任务页评价, 则需要批量替换 `cXXq` 中间链接。
4. 恢复 mindmap 源链: 至少为第 2 章和 `ita-13-1` 恢复 mindmap md, 或明确退役现有 PNG mindmap。
5. 整理特殊页: 合并或归档 `ita-24tasks.html` 与 `ita-24-fall-tasks.html`, 判断 `ita-case.html` 和 `ai-tools.html` 是否进入新课程。
6. 校对权威目录: 以 `class.md`、`ita-0.html`、现有 md/HTML 三者之一作为下学期标题源, 不要混用。
7. 技术内容更新应单章推进: AI 工具、深度学习应用、Transformer、AIGC、自动驾驶法律等内容都需要在具体改写时重新核验。

## 后续执行原则

- `draft/ita/*.md` 是正文课件长期源, 不把现有 HTML 当作唯一源。
- 未经用户审阅同意不生成 HTML。
- 任何从 `draft/ita/*.md` 生成的 HTML, 若先落到 `draft/ita`, 必须立即移动到 `6ita`, 不留残留。
- 每次重生成后必须重做 layout 和 `cXXq`: 思考题、左右导航、中间练习或任务链接。
- 对已有 HTML-only 特殊页, 先决定保留/归档/重写, 再考虑是否恢复 md 源。
- 对总目录和导航标题, 必须读取权威文件原文后写回, 不凭记忆修正。
- 外部链接、AI 工具、软件版本、课程资源在正式改课前必须重新核验。

## 更新记录

- 2026-07-04: 建立 ITA 课程审查与重建基线, 使用统一 course-audit baseline 结构。
