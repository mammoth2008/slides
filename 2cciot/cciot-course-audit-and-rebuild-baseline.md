# CCIOT Course Audit and Rebuild Baseline

检查日期: 2026-07-04
课程: CCIOT
源目录: `draft/cciot/`
目标目录: `2cciot/`
审查范围: 2cciot/cciot-*.html, draft/cciot/*.md, mindmap, navigation, layout, resources
审查状态: draft

## 一句话结论

CCIOT 当前比 DBPA 更接近可重建状态: `draft/cciot` 中 14 个正文 md 与 `2cciot` 中 14 个正文 HTML 基本一一对应, mindmap HTML 也基本存在。但课程入口、练习页、资源页和生成契约没有闭合: `cciot-0.html` 只列到第 6 章, 第 7-12 章无法从总目录进入; 所有分节的 `cXXq` 都指向不存在的 `cciot-exec.html`; 总目录的 `课程资源` 指向不存在的 `cciot-src.html`; 第 7 章部分 md 仍引用错误的 `img/c10/` 路径, 与现有 HTML 中的 `img/c07/` 已经分叉。

## 关键风险清单

- `cciot-0.html` 只列到第 6 章, 第 7-12 章缺少总目录入口。
- 所有分节 `cXXq` 都指向不存在的 `cciot-exec.html`。
- `课程资源` 指向不存在的 `cciot-src.html`。
- 第 7 章部分 md 图片路径仍写 `img/c10/`, 与现有 HTML 的 `img/c07/` 分叉。

## 审查过程复盘

- 读取项目规则与 `course-audit` Skill, 本次按审查流程执行, 不修复、不重生成、不移动资源。
- 扫描 `draft/cciot`、`2cciot`、`2cciot/img` 的文件状态。
- 读取 `2cciot/cciot-0.html`, 对照总目录链接、实际 HTML、实际 md。
- 扫描每个 `cciot-*.html` 的标题、`cXXq`、mindmap iframe、资源引用、重复 id、`data-rel-to`。
- 扫描每个 `draft/cciot/cciot-*.md` 的标题、图片路径、是否存在 `思考题`、是否存在明显不符合当前 md SOP 的结构。
- 对 `cciot-0.html` 和所有正文 HTML 运行 `check_layout.py --verbose`, 记录布局债务。未进行浏览器视觉审查, 也未联网核验云计算/物联网技术材料的时效性。

## 高阶课程设计问题

- 课程目标还没有被重新确认: 当前材料看起来像“云计算 1-6 章 + 物联网 7-12 章”的拼接, 但下学期到底要培养学生能做什么, 还没有在目录层明确表达。
- 学生画像没有进入结构设计: 信息管理与信息系统本科生的编程、网络、Linux、数据库、云服务账号、硬件实践基础不同, 会直接影响项目难度。
- 课程主线不够闭合: 云计算部分强调体验公有云/私有云/容器/存储, 物联网部分强调背景/模型/感知/标识/定位/网络, 但二者之间缺少一个贯穿案例或平台任务。
- 技术时效性需要重审: 云厂商产品、Kubernetes 生态、边缘计算、IoT 平台、5G/6G、低功耗网络、定位授时、隐私安全等内容都可能过时。
- 练习页缺失意味着评价体系不可见: 现在每节都有思考题, 但没有可执行的统一练习页、作业节奏或考核映射。
- 图片来源和可复用性未审查: 现有图片资源很多, 但没有看到来源、授权、更新日期、是否可长期复用的说明。
- 生成器与项目规范之间有差距: `2cciot/cciothg.py` 是旧式交互生成器, 生成后会把 `cXXq` 重置为占位内容, 且按输入 md 路径输出 HTML; 如果直接处理 `draft/cciot/*.md`, HTML 会先落在 `draft/cciot` 下, 需要手动迁移并重修布局/导航。

## 重建前必须先做的决策

- 总目录是否扩展为 12 章完整课程, 还是重组为更少的教学单元。
- 第 1-6 章云计算与第 7-12 章物联网之间是否增加贯穿项目, 例如“采集设备数据 -> 边缘/网络传输 -> 云端存储与容器化服务 -> 可视化/告警/决策”。
- 是否保留现有 7.1/7.2/7.3 三个小节, 还是把第 7 章压缩为物联网导论。
- 是否补建 `cciot-exec.html`, 以及练习页是全课程统一题库还是每章单独练习。
- 是否补建 `cciot-src.html`, 作为课程资源、软件账号、实验说明、参考阅读入口。
- 是否把 `cciot-6-1.md` 重写为当前生成器可接受的 slide md 格式。
- 是否先修复源 md 与 HTML 的路径分叉, 再开始改内容。

## 当前目录状态

- 目标目录: `2cciot/`
- 源目录: `draft/cciot/`
- 正文 HTML: `cciot-1-1.html` 到 `cciot-12-1.html` 共 14 个正文页, 外加 `cciot-0.html`。
- 正文 md: `cciot-1-1.md` 到 `cciot-12-1.md` 共 14 个, 与正文 HTML 基本对应。
- mindmap md: 缺少 `mindmap-6-1.md`; 其他正文页对应 mindmap md 基本存在。
- mindmap HTML: `2cciot/img/c01` 到 `c12` 下均有对应 mindmap HTML, 包括 `img/c06/mindmap-6-1.html`。
- textbook md: 仅有 `textbook-9-1.md`、`textbook-10-1.md`、`textbook-11-1.md`、`textbook-12-1.md`。
- 缺失文件: `2cciot/cciot-exec.html`、`2cciot/cciot-src.html`。
- 异常文件: `draft/cciot/temp.md` 混有多个主题材料, 不应直接作为生成源。

## 总目录与入口问题

- `cciot-0.html` 的目录只列出第 1-6 章:
  - `cciot-1-1.html`
  - `cciot-2-1.html`
  - `cciot-3-1.html`
  - `cciot-4-1.html`
  - `cciot-5-1.html`
  - `cciot-6-1.html`
- 第 7-12 章存在正文 HTML 与 md, 但没有从总目录进入:
  - `cciot-7-1.html`
  - `cciot-7-2.html`
  - `cciot-7-3.html`
  - `cciot-8-1.html`
  - `cciot-9-1.html`
  - `cciot-10-1.html`
  - `cciot-11-1.html`
  - `cciot-12-1.html`
- `课程资源` 链接到 `cciot-src.html`, 但该文件不存在。
- 总目录自身仍使用旧布局, `check_layout.py` 报 37 个问题。部分图片叠放是设计意图, 但目录页大量坐标超出当前 overview 规则, 需要作为重建时的布局债务处理。

## 最大结构问题

最大结构问题不是单个页面坏掉, 而是“课程链条有内容, 但入口和执行闭环缺失”:

- 学生从 `cciot-0.html` 只能看到云计算 1-6 章, 看不到物联网 7-12 章。
- 学生在任意分节的 `cXXq` 点击练习都会进入不存在的 `cciot-exec.html`。
- 学生在总目录点击课程资源会进入不存在的 `cciot-src.html`。
- 第 7 章的源 md 图片路径与当前 HTML 不一致, 说明“md 是唯一源”的约束已经被破坏过。
- `cciot-6-1.md` 使用 `#` / `##` 结构, 不符合当前 slide md 规范, 但对应 HTML 已经是成品页, 后续重生成风险较高。

## 逐文件问题记录

### `cciot-0.html`
- 实际标题: `云计算与物联网`
- 对应 md: 不适用
- 对应 mindmap md: 不适用
- 是否在总目录: 不适用
- 缺失链接/资源: `cciot-src.html`
- `cXXq` 状态: 未发现 cXXq
- 布局状态: check_layout 报 37 个问题: 3 overlap, 12 spacing, 22 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 重写
- 优先级: P0

补充记录:
- 实际标题: `云计算与物联网`
- 总目录只覆盖第 1-6 章, 漏掉第 7-12 章。
- `课程资源` 指向缺失文件 `cciot-src.html`。
- `check_layout.py --verbose` 报 37 个问题: 3 处 overlap、14 处 spacing、20 处 bounds。部分图片叠放可能是设计意图, 但总目录右侧章节列表整体远离 overview 可见区。
- 建议: 作为总入口重建, 补齐 12 章入口, 明确云计算与物联网两条主线的关系。

### `cciot-1-1.html`
- 实际标题: `1. 遇见云计算`
- 对应 md: `draft/cciot/cciot-1-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-1-1.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c11q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 48 个问题: 2 overlap, 18 spacing, 28 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `1. 遇见云计算`
- 对应源: `draft/cciot/cciot-1-1.md` 存在; `mindmap-1-1.md` 存在。
- 总目录已链接。
- `c11q` 有 5 个思考题, 上一页回总目录, 下一页到 `cciot-2-1.html`。
- `c11q` 的练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 48 个问题, 其中 2 处 overlap、18 处 spacing、28 处 bounds。源 md 中 `### 云计算的发展历程` 粗略计数有 11 条列表, 后续应拆分。
- 建议: 保留并更新, 重点是技术史与课程导入是否仍服务当前课程主线。

### `cciot-2-1.html`
- 实际标题: `2. 初探虚拟化`
- 对应 md: `draft/cciot/cciot-2-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-2-1.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c21q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 41 个问题: 8 overlap, 11 spacing, 22 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `2. 初探虚拟化`
- 对应源: `draft/cciot/cciot-2-1.md` 存在; `mindmap-2-1.md` 存在。
- 总目录已链接。
- `c21q` 有 5 个思考题, 导航从 `cciot-1-1.html` 到 `cciot-3-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 41 个问题, 其中 8 处 overlap、11 处 spacing、22 处 bounds。大量 overlap 与图片页/文字页同坐标相关, 需要视觉核验哪些是设计叠放, 哪些是真重叠。
- 建议: 保留, 但应确认虚拟化实践环境和软件版本是否仍可用于学生机器。

### `cciot-3-1.html`
- 实际标题: `3. 体验公有云`
- 对应 md: `draft/cciot/cciot-3-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-3-1.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c31q 存在, 7 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 46 个问题: 10 overlap, 12 spacing, 24 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `3. 体验公有云`
- 对应源: `draft/cciot/cciot-3-1.md` 存在; `mindmap-3-1.md` 存在。
- 总目录已链接。
- `c31q` 有 7 个思考题, 导航从 `cciot-2-1.html` 到 `cciot-4-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 46 个问题, 其中 10 处 overlap、12 处 spacing、24 处 bounds。
- 建议: 保留, 但云厂商、产品名称、账号开通、免费额度、区域/VPC/安全组示例需要更新。

### `cciot-4-1.html`
- 实际标题: `4. 体验私有云`
- 对应 md: `draft/cciot/cciot-4-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-4-1.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c41q 存在, 6 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 25 个问题: 5 overlap, 8 spacing, 12 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `4. 体验私有云`
- 对应源: `draft/cciot/cciot-4-1.md` 存在; `mindmap-4-1.md` 存在。
- 总目录已链接。
- `c41q` 有 6 个思考题, 导航从 `cciot-3-1.html` 到 `cciot-5-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 25 个问题, 其中 5 处 overlap、8 处 spacing、12 处 bounds。
- 建议: 保留或压缩。私有云产品生态变化较快, OpenStack、CloudStack、VMware、Microsoft private cloud 的教学价值需要重新排序。

### `cciot-5-1.html`
- 实际标题: `5. 体验容器云`
- 对应 md: `draft/cciot/cciot-5-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-5-1.md` 存在
- 是否在总目录: 是
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c51q 存在, 7 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 45 个问题: 9 overlap, 17 spacing, 19 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `5. 体验容器云`
- 对应源: `draft/cciot/cciot-5-1.md` 存在; `mindmap-5-1.md` 存在。
- 总目录已链接。
- `c51q` 有 7 个思考题, 导航从 `cciot-4-1.html` 到 `cciot-6-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 45 个问题, 其中 9 处 overlap、17 处 spacing、19 处 bounds。源 md 中 `### Kubernetes` 粗略计数有 9 条列表, 后续应拆分。
- 建议: 保留并重点更新。容器云是连接云计算与 IoT 平台部署的关键桥梁, 可以承接贯穿案例。

### `cciot-6-1.html`
- 实际标题: `6. 存储云`
- 对应 md: `draft/cciot/cciot-6-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-6-1.md` 缺失
- 是否在总目录: 是
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c61q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 35 个问题: 6 overlap, 6 spacing, 23 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `6. 存储云`
- 对应源: `draft/cciot/cciot-6-1.md` 存在, 但源文件使用 `#` / `##` 结构, 不符合当前 slide md SOP。
- 缺少 `draft/cciot/mindmap-6-1.md`, 但存在 `2cciot/img/c06/mindmap-6-1.html`。
- 总目录已链接。
- `c61q` 有 5 个思考题, 导航从 `cciot-5-1.html` 到 `cciot-7-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 35 个问题, 其中 6 处 overlap、6 处 spacing、23 处 bounds。
- 建议: 先恢复合格 md 与 mindmap md, 再考虑内容更新。该节可作为云计算到物联网数据链的过渡。

### `cciot-7-1.html`
- 实际标题: `7. 物联网绪论 / 7.1 物联网产生的背景`
- 对应 md: `draft/cciot/cciot-7-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-7-1.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c71q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 51 个问题: 7 overlap, 18 spacing, 26 bounds
- 源与结果是否分叉: 是
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `7. 物联网绪论` / `7.1 物联网产生的背景`
- 对应源: `draft/cciot/cciot-7-1.md` 存在; `mindmap-7-1.md` 存在。
- 总目录未链接。
- `c71q` 有 5 个思考题, 导航从 `cciot-6-1.html` 到 `cciot-7-2.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- HTML 中图片引用在 `img/c07/`, 但源 md 仍引用 `img/c10/` 下的 18 张图片, 这些路径在目标目录不存在。这是明确的 md/HTML 分叉。
- 布局检查报 51 个问题, 其中 7 处 overlap、18 处 spacing、26 处 bounds。
- 建议: 优先修源 md 图片路径, 再决定是否压缩本节历史背景内容。

### `cciot-7-2.html`
- 实际标题: `7. 物联网绪论 / 7.2 物联网形成与发展的主要线索`
- 对应 md: `draft/cciot/cciot-7-2.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-7-2.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c72q 存在, 4 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 58 个问题: 8 overlap, 21 spacing, 29 bounds
- 源与结果是否分叉: 是
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `7. 物联网绪论` / `7.2 物联网形成与发展的主要线索`
- 对应源: `draft/cciot/cciot-7-2.md` 存在; `mindmap-7-2.md` 存在。
- 总目录未链接。
- `c72q` 有 4 个思考题, 导航从 `cciot-7-1.html` 到 `cciot-7-3.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- HTML 中图片引用在 `img/c07/`, 但源 md 仍引用 `img/c10/` 下的 19 张图片, 这些路径在目标目录不存在。这也是明确的 md/HTML 分叉。
- 布局检查报 58 个问题, 其中 8 处 overlap、21 处 spacing、29 处 bounds。
- 建议: 优先修源 md 图片路径。内容上应避免把发展史讲成素材堆叠, 需要和后续“网络、标识、感知”章节形成清晰桥接。

### `cciot-7-3.html`
- 实际标题: `7. 物联网绪论 / 7.3 物联网的概念与特征`
- 对应 md: `draft/cciot/cciot-7-3.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-7-3.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c73q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 11 个问题: 3 spacing, 8 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `7. 物联网绪论` / `7.3 物联网的概念与特征`
- 对应源: `draft/cciot/cciot-7-3.md` 存在; `mindmap-7-3.md` 存在。
- 总目录未链接。
- `c73q` 有 5 个思考题, 导航从 `cciot-7-2.html` 到 `cciot-8-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 11 个问题, 主要是 3 处 spacing、8 处 bounds, 未见 overlap。
- 建议: 保留, 但定义与特征应作为后续技术体系的概念基座, 不宜停留在抽象词表。

### `cciot-8-1.html`
- 实际标题: `8. 物联网参考模型与技术体系`
- 对应 md: `draft/cciot/cciot-8-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-8-1.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c81q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 48 个问题: 6 overlap, 6 spacing, 36 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 重写
- 优先级: P0

补充记录:
- 实际标题: `8. 物联网参考模型与技术体系`
- 对应源: `draft/cciot/cciot-8-1.md` 存在; `mindmap-8-1.md` 存在。
- 总目录未链接。
- 源 md 标题为 `8. 物联网的参考模型与技术体系`, HTML 标题少了一个 `的`; 需要决定以哪一版为准。
- `c81q` 有 5 个思考题, 导航从 `cciot-7-3.html` 到 `cciot-9-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 48 个问题, 其中 6 处 overlap、6 处 spacing、36 处 bounds。源 md 中 `### 物联网参考模型 ITU-T`、`### 物联网参考模型 IWF`、`### 物联网技术体系功能域` 均有 9 条左右列表, 后续应拆分。
- 建议: 保留并重写为“架构地图”章节, 明确各后续章节在参考模型中的位置。

### `cciot-9-1.html`
- 实际标题: `9. 感知`
- 对应 md: `draft/cciot/cciot-9-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-9-1.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c91q 存在, 6 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 16 个问题: 16 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `9. 感知`
- 对应源: `draft/cciot/cciot-9-1.md` 存在; `mindmap-9-1.md` 存在; `textbook-9-1.md` 存在。
- 总目录未链接。
- `c91q` 有 6 个思考题, 导航从 `cciot-8-1.html` 到 `cciot-10-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 16 个 bounds 问题, 未见 overlap。
- 建议: 保留。需要补案例, 把感知从传感器枚举推进到数据质量、采样、误差、边缘预处理。

### `cciot-10-1.html`
- 实际标题: `10. 标识`
- 对应 md: `draft/cciot/cciot-10-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-10-1.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c101q 存在, 6 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 23 个问题: 23 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `10. 标识`
- 对应源: `draft/cciot/cciot-10-1.md` 存在; `mindmap-10-1.md` 存在; `textbook-10-1.md` 存在。
- 总目录未链接。
- `c101q` 有 6 个思考题, 导航从 `cciot-9-1.html` 到 `cciot-11-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 23 个 bounds 问题, 未见 overlap。
- 建议: 保留。应把 RFID、二维码、生物特征、编码解析、隐私安全等放进统一标识框架, 避免只列技术名。

### `cciot-11-1.html`
- 实际标题: `11. 定位与授时 / 11.1 定位与授时`
- 对应 md: `draft/cciot/cciot-11-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-11-1.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c111q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 24 个问题: 24 bounds
- 源与结果是否分叉: 未发现明确分叉
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `11. 定位与授时` / `11.1 定位与授时`
- 对应源: `draft/cciot/cciot-11-1.md` 存在; `mindmap-11-1.md` 存在; `textbook-11-1.md` 存在。
- 总目录未链接。
- `c111q` 有 5 个思考题, 导航从 `cciot-10-1.html` 到 `cciot-12-1.html`。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 24 个 bounds 问题, 未见 overlap。
- 建议: 保留。需要补充从定位/授时到 IoT 数据可信度、事件排序、同步误差的教学主线。

### `cciot-12-1.html`
- 实际标题: `12. 网络`
- 对应 md: `draft/cciot/cciot-12-1.md` 存在
- 对应 mindmap md: `draft/cciot/mindmap-12-1.md` 存在
- 是否在总目录: 否
- 缺失链接/资源: `cciot-exec.html`
- `cXXq` 状态: c121q 存在, 5 个问题; 缺失链接: cciot-exec.html
- 布局状态: check_layout 报 22 个问题: 22 bounds
- 源与结果是否分叉: 是
- 建议处理: 修复
- 优先级: P0

补充记录:
- 实际标题: `12. 网络`
- 对应源: `draft/cciot/cciot-12-1.md` 存在; `mindmap-12-1.md` 存在; `textbook-12-1.md` 存在。
- 总目录未链接。
- `c121q` 有 5 个思考题, 导航从 `cciot-11-1.html` 回总目录。
- 练习链接指向缺失的 `cciot-exec.html`。
- 布局检查报 22 个 bounds 问题, 未见 overlap。源 md 中 `### 移动通信网络技术` 粗略计数有 9 条列表, 后续应拆分。
- 建议: 保留, 但应决定网络章节是否作为课程收束, 或是否还需要补云边协同、安全、应用综合案例。

## Mindmap 状态

- 已有 mindmap md: `1-1`、`2-1`、`3-1`、`4-1`、`5-1`、`7-1`、`7-2`、`7-3`、`8-1`、`9-1`、`10-1`、`11-1`、`12-1`。
- 缺少 mindmap md: `mindmap-6-1.md`。
- 已有 mindmap HTML: `img/c01/mindmap-1-1.html`、`img/c02/mindmap-2-1.html`、`img/c03/mindmap-3-1.html`、`img/c04/mindmap-4-1.html`、`img/c05/mindmap-5-1.html`、`img/c06/mindmap-6-1.html`、`img/c07/mindmap-7-1.html`、`img/c07/mindmap-7-2.html`、`img/c07/mindmap-7-3.html`、`img/c08/mindmap-8-1.html`、`img/c09/mindmap-9-1.html`、`img/c10/mindmap-10-1.html`、`img/c11/mindmap-11-1.html`、`img/c12/mindmap-12-1.html`。
- 风险: `mindmap-6-1.html` 没有对应 md 源, 后续若要重建应先从 HTML 或正文内容恢复 md。

## 练习与评价状态

- `cciot-exec.html` 不存在, 但所有分节 `cXXq` 的中间练习链接都指向它。
- 当前只有每节思考题, 还没有统一的可执行练习页、作业节奏或评价映射。
- 后续应先决定统一题库还是分章练习, 再批量修 `cXXq` 中间链接。

## 资源与图片状态

- `cciot-src.html` 不存在, 总目录的课程资源入口断开。
- 第 7 章源 md 的图片路径与 HTML 不一致, 需要先回补到 md。
- 现有图片资源数量较多, 但尚未审查来源、授权、版本和长期可复用性。

## 工作建议

1. 先修复课程入口: 补齐 `cciot-0.html` 中第 7-12 章入口, 同时决定课程资源页是否要恢复。
2. 再修复源一致性: 先改 `draft/cciot/cciot-7-1.md` 和 `cciot-7-2.md` 的图片路径, 再恢复 `mindmap-6-1.md`。
3. 决定练习体系: 如果继续使用统一入口, 补建 `cciot-exec.html`; 如果改为分章练习, 则逐页改 `cXXq` 中间链接。
4. 重建 `cciot-6-1.md`: 把 `#` / `##` 结构改成当前 SOP 接受的 slide block, 并与现有 HTML 内容对齐。
5. 更新课程架构: 用一张总地图重新定义云计算、物联网、边缘/云端、数据链路、实验项目之间的关系。
6. 内容更新应按章推进: 先定每章教学目标和案例, 再更新 md, 最后经用户审阅后才生成 HTML。
7. 布局修复不要先做全量美化: 先修会阻碍使用的入口/练习/资源/源路径问题, 等章节内容稳定后再统一跑 layout。

## 后续执行原则

- `draft/cciot/*.md` 继续作为唯一长期源; 已经发现的 md/HTML 分叉必须先回补到 md。
- 未经审阅同意不生成 HTML。
- 如果运行旧生成器导致 HTML 先落到 `draft/cciot`, 必须立即移回 `2cciot`, 不在 `draft` 留 HTML。
- 每次重生成后都要重做布局和 `cXXq` 三项内容: 思考题、左右导航、中间练习链接。
- 对第 7-12 章, 不应只补总目录链接; 还要确认课程目标中物联网部分与云计算部分的关系。
- 对涉及云厂商、软件版本、IoT 协议、网络代际、平台截图的内容, 后续改写前需要重新核验时效性。

## 更新记录

- 2026-07-04: 建立课程审查与重建基线。
- 2026-07-04: 按统一 baseline 结构轻量规整, 增加固定元数据、关键风险、逐文件字段摘要、练习与资源状态。
