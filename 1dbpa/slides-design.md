# DBPA Slides Design Baseline

Updated: 2026-07-04

This document records the first visual baseline for the DBPA course slides. It is a design reference for rebuilding and improving `数据库原理与应用`, not a replacement for the markdown source files under `draft/dbpa/`.

Global size rule: all courses now use `1280 x 960` / 4:3 as the primary design size. Older `1024 x 768` pages are compatibility or migration targets, not the new visual baseline.

## 1. Purpose

The DBPA slides should feel like a course about database systems, not a generic presentation theme. The visual system should help students recognize:

- data objects: tables, rows, fields, keys, constraints, results
- system structures: schema layers, mappings, models, storage, transactions
- operation paths: query, join, update, recovery, concurrency
- course navigation: each page sits in a larger database architecture map

The current first-version prototype is the design starting point. Future work may adjust details, but should not casually replace the whole direction.

## 2. Current Prototype Files

- `1dbpa/prototype/dbpa-visual-prototype.html`
- `1dbpa/prototype/dbpa-visual-identity.css`
- `1dbpa/img/c00/dbpa-cover-bg-2608-final.png`
- `1dbpa/dbpa-cover-preview.html`
- `1dbpa/dbpa-body-font-preview.html`
- `1dbpa/dbpa-body-serif-preview.html`
- `1dbpa/dbpa-body-tech-preview.html`

The prototype is not yet the formal generated course deck. It is a visual system package for evaluating and later applying to real DBPA slides.

## 3. Visual Identity

Working identity:

- Chinese course name: `数据库原理与应用`
- English name: `Database Principles and Applications`
- Design concept: `Data Architecture Atlas`
- Version marker: `VER. 2608`

Core visual direction:

- warm paper background, not a cold dark dashboard
- deep blue text for academic weight
- copper accent for structure, keys, paths, and progress
- subtle grid lines to suggest data architecture and coordinate systems
- table, relation, schema, SQL, and transaction objects as native page elements

Avoid:

- generic cyberpunk/neon database imagery
- one-note blue dashboards
- over-decorated cards
- default bullet lists as the main visual language
- large database-cylinder icons as the central identity
- text embedded directly inside generated cover images

## 4. Cover Strategy

The cover background image should not include final title text. The title should be rendered in HTML/CSS so that it stays editable, crisp, and consistent with the rest of the deck.

The current cover image direction is acceptable:

- realistic city and people
- data, relation, security, and analytics hints in the upper visual field
- bright center area reserved for the course title
- weaker database-cylinder symbolism

The cover title should retain the current title-page spirit: large Chinese title, English subtitle, and version marker. The title should stay readable over projection and should not depend on image-generation text quality.

## 5. Typography

Current baseline:

```css
--serif: "Source Han Serif CN", "Songti SC", STSong, SimSun, "Noto Serif CJK SC", serif;
--sans: "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB", "Source Han Sans SC", "Noto Sans CJK SC", Arial, sans-serif;
--latin: "Avenir Next", "Segoe UI", Arial, sans-serif;
--mono: "SF Mono", Menlo, Monaco, Consolas, "Inconsolata", "Courier New", monospace;
```

Use:

- `--serif` for `h1`, `h2`, `h3`, and other strong title text
- `--sans` for Chinese body text, lead text, notes, descriptions, and list content
- `--latin` for labels, badges, chapter markers, English metadata, and page footer
- `--mono` for SQL, table fields, code, and database identifiers

Reasoning:

- full serif body text has more character, but can feel heavy and less clear on projection
- full sans-serif slides can feel clean but less distinctive
- title serif + body sans-serif is the current compromise: recognizable, readable, and less generic
- `PingFang SC` first suits macOS; `Microsoft YaHei` as the first fallback suits most Windows student devices
- avoid bundling large Chinese font files unless there is a strong reason; web review should not depend on slow font downloads

Known issue:

- some CJK serif fonts can make individual Chinese glyphs look uneven or unexpectedly bold at large sizes. If this appears in title or lead text, first check the actual fallback font and font weight before changing content.

## 6. Color And Texture

Current palette:

```css
--paper: #fbf3df;
--paper-deep: #f2e4c6;
--ink: #062f49;
--ink-soft: #31566b;
--muted: #667986;
--accent: #a8732a;
--accent-soft: rgba(168, 115, 42, 0.18);
--line: rgba(6, 47, 73, 0.18);
```

Guidance:

- keep the warm paper base as the course identity
- use deep blue for high-contrast academic text
- use copper sparingly for keys, numbering, relation paths, and progress
- keep background grid subtle; it should support structure, not compete with text
- in dense body pages, reduce grid visibility if it interferes with reading

## 7. Page Types

The prototype defines six page patterns that should guide later DBPA redesign.

### 7.1 Cover Page

Purpose: establish course first impression.

Elements:

- generated or curated image background
- HTML-rendered title
- English subtitle
- version marker
- design label or course identity label

### 7.2 Course Map Page

Purpose: show the whole course as a database-system map.

Use for:

- opening overview
- chapter roadmaps
- review pages

Design notes:

- use numbered modules instead of bullets
- each module should include a Chinese name and concise English hint
- the map should help students place the current section inside the full course

### 7.3 Concept Page

Purpose: explain definitions, distinctions, and key terms.

Current pattern:

- large serif title
- sans-serif lead
- numbered records instead of default bullets
- English terms shown as muted inline labels

Use for:

- data/schema/instance/model
- key/constraint/dependency
- transaction/recovery/concurrency concepts

### 7.4 Structure Page

Purpose: show layered structures directly, rather than describing them as a list.

Use for:

- three-schema architecture
- conceptual/logical/physical models
- storage/index/log hierarchy
- normalization/dependency layers

Design notes:

- make the structure itself the layout
- do not put a diagram in a decorative card if the whole slide can become the diagram

### 7.5 Relation Page

Purpose: show database case objects as tables and relationships.

Current lesson:

- avoid hand-positioned rotated `div` lines when the board can resize
- use SVG paths in the same coordinate system as the table layout
- give the ER board a stable width before positioning tables and links

Recommended grammar:

- table box = relation
- header = relation name
- row = field
- `PK` / `FK` = visible constraint marker
- copper line = relation path or foreign-key path
- optional label on path = join or constraint meaning

### 7.6 SQL Page

Purpose: turn a query page into a path from question to statement to result.

Elements:

- question panel
- SQL code window
- result table
- small reasoning steps

Design notes:

- code should stay mono
- result tables should look like database output, not generic HTML tables
- preserve enough whitespace for projection readability

### 7.7 Mechanism Page

Purpose: explain state changes and system processes.

Use for:

- transaction timeline
- recovery
- concurrency control
- authorization/check flow

Design notes:

- prefer timeline, state machine, or process path over bullets
- make conflict, failure, commit, redo, undo visually distinct

## 8. 3D Impress.js Layout Rules

Use 3D layout as course structure, not as decoration.

Suggested semantics:

- `x` axis: knowledge module or topic family
- `y` axis: learning progression within a module
- `z` axis: abstraction depth or detail overlay

Important rule:

- normal content pages should not share the same `x/y` and differ only by `z`
- z-only stacking can make inactive pages visually pierce the current page
- only adjacent shallow overlays, such as image/detail pages with small `rel-z`, are acceptable

Always run:

```bash
python3 .agents/skills/build-layout/check_layout.py 1dbpa/prototype/dbpa-visual-prototype.html --verbose
```

For formal generated slides, run the same checker on the target `dbpa-*.html` after layout edits.

## 9. Navigation And Progress

Use impress.js native progress markup:

```html
<div class="impress-progressbar">
    <div></div>
</div>
<div class="impress-progress"></div>
```

Do not replace it with a static custom `.progressbar`. Native progress keeps the page number and progress width synchronized with impress.js.

Footer guidance:

- keep the footer above the very bottom edge
- ensure footer text remains readable on complex backgrounds
- use footer for course identity and page role, not for long explanations

## 10. Projection Readability

Current body scale is intentionally large:

- lead text around `32px`
- primary list text around `32px`
- field-list text around `28px`
- timeline body text around `26px`
- SQL code around `20px`

Guidance:

- projection readability is more important than fitting too many points
- most slides should contain only a few lines
- if a slide requires small text, split it or convert the content into a diagram/table
- avoid text that depends on exact browser font rendering to fit tightly

Before applying the system broadly, test representative pages at:

- `1280 x 960` as the primary projection design size
- `1024 x 768` only when checking old projector or legacy-page compatibility
- `1280 x 720` only as a web-review compatibility check, not as the main design target
- classroom projector if available

Check:

- title does not dominate the body
- body text is readable from the back of the room
- grid texture does not interfere
- footer and progress are visible
- tables and SQL are legible
- no element overlaps after scaling

## 11. Implementation Rules

For design prototypes:

- it is acceptable to hand-edit `1dbpa/prototype/*.html` and `*.css`
- keep prototype decisions documented here
- run browser or screenshot verification for visual issues

For formal course slides:

- `draft/dbpa/` markdown remains the source of teaching content
- generated HTML under `1dbpa/` is the output deck
- if formal content changes, update markdown first unless the change is a narrow HTML-only visual prototype
- after running the generator, restore layout and `cXXq` navigation
- if adding or replacing visual resources, place assets under `1dbpa/img/cNN/`

Do not let design experiments silently diverge from the formal workflow.

## 12. Lessons From This Round

### 12.1 Cover Text

Generated image text is not reliable enough for formal course titles. Use a text-free generated background and render the title in HTML.

### 12.2 Font Weight

Large Chinese serif text may show uneven glyph weight depending on the available system font. Diagnose fallback and weight before assuming the phrase itself is wrong.

### 12.3 Body Font

Non-serif body text improves clarity, but can feel generic. Keep the course character in titles, data objects, structure lines, and page composition.

### 12.4 Relation Lines

Absolute rotated lines are fragile when their container width changes. Use SVG paths for ER or relation links when the line must connect semantic endpoints.

### 12.5 Depth Stacking

Passing `OVERLAP=0` is not enough. Pages can still visually interfere if they share `x/y` and differ only by `z`. Use the updated `DEPTH STACK` check and inspect the page in browser.

### 12.6 Progress Bar

The bottom progress bar should remain impress.js native. It is part of the slide system, not a decorative asset.

### 12.7 Design Before Batch Conversion

Do not batch-convert all DBPA slides immediately. First apply the baseline to one real section, test projection readability and navigation, then expand.

## 13. Next Recommended Step

Choose one DBPA section as the first real redesign pilot. Good candidates:

- `dbpa-1-1.html`: early concept pages, useful for typography and numbered records
- `dbpa-3-1.html` or `dbpa-3-2.html`: relation / SQL material, useful for database-object grammar

Pilot process:

1. read the existing section HTML and corresponding `draft/dbpa/*.md`
2. identify page types in this design baseline
3. adjust one section only
4. run layout check
5. inspect in browser at projection-like size
6. update this file with any new rule that survives the pilot

The goal is not to make every page decorative. The goal is to make the whole DBPA course feel like a coherent database-system atlas.
