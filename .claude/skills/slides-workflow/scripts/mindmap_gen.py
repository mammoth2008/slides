#!/usr/bin/env python3
"""
mindmap_gen.py — 从 mindmap md 文件生成 mindmap HTML

输入：mindmap md 文件（与课件 md 分离的独立文件，命名为 {course}-N-N-mindmap.md）
输出：markmap 格式的 mindmap HTML

用法:
    python3 mindmap_gen.py /Users/Freeman/Documents/products/courses/library/texts/gai-slide-drafts/mindmaps/gai-3-2-mindmap.md
    python3 mindmap_gen.py /Users/Freeman/Documents/products/courses/library/texts/gai-slide-drafts/mindmaps/gai-3-2-mindmap.md -o 5gai/img/c03/mindmap-3-2.html

输入文件标题层级:
    # 标题  → h1 (根节点，通常是章节名)
    ## 标题  → h2 (一级分支，主要知识模块)
    ### 标题 → h3 (二级分支，子主题)
    - 条目  → li (叶子节点，具体知识点)

注意：输入是 mindmap md（知识结构），不是课件 md（幻灯片结构）。
两者内容相关但结构不同，需分别维护。
"""

import re
import json
import argparse
import html as html_module
from pathlib import Path

# ─────────────────────────────────────────
#  解析
# ─────────────────────────────────────────

def parse_md(path: str) -> list[dict]:
    """
    返回 section 列表:

    {
      'start_line': int,
      'end_line':   int,
      'title':       str | None,    # 标题文本
      'heading_level': int,          # 1=h1 2=h2 3=h3
      'items':       list[(line, text)],
    }
    """
    with open(path, encoding='utf-8') as f:
        raw_lines = f.readlines()

    sections = []
    pending_items = []
    current_head = None
    current_head_level = 0
    last_head_line = 0

    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        line_num = i + 1
        stripped = line.strip()

        # 跳过 #### 图片标题
        if stripped.startswith('####'):
            i += 1
            continue

        # ### 标题
        mh = re.match(r'\s*#{1,3}\s+(.+)', stripped)
        if mh:
            if current_head is not None:
                sections.append(_make_section(
                    current_head[2], current_head[0], last_head_line,
                    current_head_level, pending_items))
                pending_items = []
            level = len(mh.group(0).lstrip().split()[0])
            current_head = (line_num, level, mh.group(1).strip())
            current_head_level = level
            last_head_line = line_num
            i += 1
            continue

        # 列表项
        ml = re.match(r'\s*-\s+(.+)', stripped)
        if ml:
            item_line = line_num
            text = ml.group(1).strip()
            j = i + 1
            while j < len(raw_lines):
                next_line = raw_lines[j].rstrip()
                if next_line and (raw_lines[j][0] in ' \t') \
                   and not next_line.strip().startswith('<!--'):
                    text += ' ' + next_line.strip()
                    j += 1
                else:
                    break
            pending_items.append((item_line, text))
            i = j
            last_head_line = line_num
            continue

        i += 1

    if current_head is not None:
        sections.append(_make_section(
            current_head[2], current_head[0], last_head_line,
            current_head_level, pending_items))

    return sections


def _make_section(title: str, start_line: int, end_line: int,
                  level: int, items: list) -> dict:
    return {
        'start_line': start_line,
        'end_line': max(end_line, start_line),
        'title': title,
        'heading_level': level,
        'items': items,
    }


# ─────────────────────────────────────────
#  构建树
# ─────────────────────────────────────────

def _make_h2(title: str, sec: dict, items: list) -> dict:
    return {'content': title, 'heading_level': 2,
            'start_line': sec['start_line'],
            'end_line': sec['end_line'],
            'children': [
                {'content': t, 'heading_level': 4,
                 'start_line': l, 'end_line': l, 'children': []}
                for l, t in items
            ]}


def build_tree(sections: list[dict], manifest: list[dict] = None) -> dict:
    """
    从 sections 构建 mindmap 树。

    直接按 markdown 标题层级构建：
    - #  → h1 (根节点)
    - ## → h2 (二级节点)
    - ### → h3 (三级节点)，若前面没有 h2 则自动提升为 h2
    - -  → li (叶子节点)
    manifest 参数保留但不再使用。
    """
    root = {'content': '', 'heading_level': 1, 'start_line': 1,
            'end_line': 1, 'children': []}
    h2_nodes = []
    h3_nodes = []

    for sec in sections:
        title = sec.get('title')
        level = sec.get('heading_level', 0)
        items = sec.get('items', [])

        if level == 1:
            root = {'content': title, 'heading_level': 1,
                    'start_line': sec['start_line'],
                    'end_line': sec['end_line'], 'children': []}
            h2_nodes = root['children']
            h3_nodes = []

        elif level == 2:
            h2 = _make_h2(title, sec, items)
            h2_nodes.append(h2)
            h3_nodes = h2['children']

        elif level == 3:
            if not h2_nodes:
                # 没有 h2 时，将 h3 提升为 h2
                h2 = _make_h2(title, sec, items)
                h2_nodes.append(h2)
                h3_nodes = h2['children']
            else:
                h3 = {'content': title, 'heading_level': 3,
                      'start_line': sec['start_line'],
                      'end_line': sec['end_line'],
                      'children': [
                          {'content': t, 'heading_level': 4,
                           'start_line': l, 'end_line': l, 'children': []}
                          for l, t in items
                      ]}
                h3_nodes.append(h3)

    root['end_line'] = h2_nodes[-1]['end_line'] if h2_nodes else 1
    return root


# ─────────────────────────────────────────
#  转换
# ─────────────────────────────────────────

TAG_MAP = {1: 'h1', 2: 'h2', 3: 'h3', 4: 'li'}

def node_to_json(node: dict) -> dict:
    tag = TAG_MAP.get(node.get('heading_level', 4), 'li')
    start = node.get('start_line', 0)
    end = node.get('end_line', 0)
    return {
        'content': node['content'],
        'children': [node_to_json(c) for c in node.get('children', [])],
        'payload': {'tag': tag, 'lines': f'{start},{end}'},
    }

def tree_to_json(tree: dict) -> str:
    node = node_to_json(tree)
    json_str = json.dumps(node, ensure_ascii=False)
    return (json_str
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;'))


# ─────────────────────────────────────────
#  HTML 模板
# ─────────────────────────────────────────

HTML_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta http-equiv="X-UA-Compatible" content="ie=edge" />
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; }}
html {{
  font-family: ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
}}
#mindmap {{ display: block; width: 100vw; height: 100vh; }}
</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/markmap-toolbar@0.18.12/dist/style.css">
</head>
<body>
<svg id="mindmap"></svg>
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-view@0.18.12/dist/browser/index.js"></script>
<script src="https://cdn.jsdelivr.net/npm/markmap-toolbar@0.18.12/dist/index.js"></script>
<script>(r => {{ setTimeout(r); }})(function renderToolbar() {{
  const {{ markmap, mm }} = window;
  const {{ el }} = markmap.Toolbar.create(mm);
  el.setAttribute('style', 'position:absolute;bottom:20px;right:20px');
  document.body.append(el);
}})</script>
<script>((getMarkmap, getOptions, root2, jsonOptions) => {{
  const markmap = getMarkmap();
  window.mm = markmap.Markmap.create(
    "svg#mindmap",
    (getOptions || markmap.deriveOptions)(jsonOptions),
    root2
  );
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {{
    document.documentElement.classList.add("markmap-dark");
  }}
}})(() => window.markmap, null, {json_str}, {{}})</script>
</body>
</html>
"""


# ─────────────────────────────────────────
#  主流程
# ─────────────────────────────────────────

COURSE_PREFIXES = {
    'gai': '5gai', 'pmi': '10pmi', 'cciot': '2cciot',
    'itpm': '3itpm', 'ita': '6ita', 'il': '8il',
    'dbpa': '1dbpa', 'fiit': '9fiit',
}


def _find_project_root(start: Path) -> Path:
    """查找 slides 项目根；外部 courses-vault 输入时从 cwd 回查。"""
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / 'CLAUDE.md').exists():
            return candidate
    import os
    cwd = Path(os.getcwd()).resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / 'CLAUDE.md').exists():
            return candidate
    return cwd


def _infer_course(md_path: Path) -> str:
    """兼容 courses-vault 源包路径和旧 draft/{course} 路径。"""
    resolved = md_path.resolve()
    for part in resolved.parts:
        if part.endswith('-slide-drafts'):
            return part.removesuffix('-slide-drafts')
    if md_path.parent.name in {'mindmaps', 'slide-drafts'}:
        parent_name = md_path.parent.parent.name
        if parent_name.endswith('-slide-drafts'):
            return parent_name.removesuffix('-slide-drafts')
    return md_path.parent.name


def generate(md_path: str, output_path: str = None) -> str:
    md_path = Path(md_path)
    sections = parse_md(str(md_path))
    tree = build_tree(sections)
    json_str = tree_to_json(tree)

    if output_path is None:
        stem = md_path.stem          # "gai-3-2-mindmap"
        course = _infer_course(md_path)
        m_chapter = re.search(r'(\d+)-(\d+)', stem)
        if m_chapter:
            ch = int(m_chapter.group(1))
            sec = int(m_chapter.group(2))
            img_subdir = f'c{ch:02d}'
            filename = f'mindmap-{ch}-{sec}.html'
        else:
            img_subdir = f'c{stem}'
            filename = f'mindmap-{stem}.html'
        prefix = COURSE_PREFIXES.get(course, course)
        root = _find_project_root(md_path)
        output_path = root / prefix / 'img' / img_subdir / filename
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    title = html_module.escape(tree.get('content', 'Mindmap'))
    html = HTML_TEMPLATE.format(title=title, json_str=json_str)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description='生成 mindmap HTML')
    parser.add_argument('md_path', help='课件 md 文件路径')
    parser.add_argument('-o', '--output', help='输出 HTML 路径')
    args = parser.parse_args()
    out = generate(args.md_path, args.output)
    print(f'✓ {out}')


if __name__ == '__main__':
    main()
