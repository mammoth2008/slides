#!/usr/bin/env python3
"""
auto_layout.py — 读取 YAML 配置，计算 impress.js 布局坐标，写回 HTML。

工作流:
    1. LLM 读取课件内容，起草分支分组（见 SKILL.md）
    2. 用户审阅修改，确认分组后写成 YAML 文件
    3. 运行此脚本生成最终布局

YAML 格式示例（见 SKILL.md 完整说明）:
    html: 5gai/gai-3-2.html
    single_branch_x: 400
    right_branch_extra_x: 600
    branches:
      - name: 工作模式
        steps: [a1, a2, a3, a4, a5]
      - name: 课堂练习
        steps: [a6, a7, a8, a9]

用法:
    python3 .agents/skills/build-layout/auto_layout.py gai-3-2-layout.yaml
    python3 .agents/skills/build-layout/auto_layout.py gai-3-2-layout.yaml --dry-run
"""

import re
import sys
import argparse
from pathlib import Path


# ── 内嵌 YAML 解析（仅支持本工具所需的简单格式）──────────────────────────

def _parse_scalar(val: str):
    if not val:
        return None
    if (val.startswith('"') and val.endswith('"')) or \
       (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


def _parse_flow_seq(val: str) -> list:
    """解析 [a1, a2, a3] 格式。"""
    val = val.strip()
    if val.startswith('[') and val.endswith(']'):
        return [i.strip().strip('"\'') for i in val[1:-1].split(',') if i.strip()]
    return []


def _load_yaml(text: str) -> dict:
    """最小 YAML 解析器，支持本工具的 config 格式。"""
    result = {}
    branches = None
    cur_branch = None
    cur_indent = -1

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            continue
        indent = len(raw_line) - len(raw_line.lstrip())

        if indent == 0:
            k, _, v = stripped.partition(':')
            k = k.strip()
            v = v.strip()
            if k == 'branches':
                branches = []
                result['branches'] = branches
            elif v:
                result[k] = _parse_scalar(v)

        elif branches is not None and indent == 2 and stripped.startswith('-'):
            rest = stripped[1:].strip()
            cur_branch = {}
            branches.append(cur_branch)
            if ':' in rest:
                k, _, v = rest.partition(':')
                cur_branch[k.strip()] = _parse_scalar(v.strip())
            cur_indent = indent

        elif cur_branch is not None and indent > 2:
            if ':' in stripped:
                k, _, v = stripped.partition(':')
                k = k.strip()
                v = v.strip()
                if k == 'steps':
                    cur_branch['steps'] = _parse_flow_seq(v)
                else:
                    cur_branch[k] = _parse_scalar(v)

    return result


# ── HTML 解析 ──────────────────────────────────────────────────────────────

_STEP_TAG_RE = re.compile(
    r'<div\b[^>]*\bclass\s*=\s*"[^"]*\bstep\b[^"]*"[^>]*>',
    re.DOTALL,
)
_ID_RE = re.compile(r'\bid\s*=\s*"([^"]*)"')
_COORD_RE = re.compile(
    r'[ \t]*\bdata-(?:rel-(?:to|x|y|z)|[xyz])\s*=\s*"[^"]*"\n?',
    re.IGNORECASE,
)
_SPECIAL_ID_RE = re.compile(r'^(overview|c\d+t|c\d+q|mm\d+)$')
_HEADING_RE = re.compile(r'<h[23]|^#{2,3} ', re.I | re.MULTILINE)
_IMG_RE = re.compile(r'<img\b|!\[', re.I)


def _parse_steps(html: str) -> list[dict]:
    """返回所有 step 的 {id, is_picture}。"""
    steps = []
    for m in _STEP_TAG_RE.finditer(html):
        tag = m.group(0)
        id_m = _ID_RE.search(tag)
        if not id_m:
            continue
        sid = id_m.group(1)
        if sid in ('impress', 'overview'):
            continue

        content_end = html.find('</div>', m.end())
        content = html[m.end():content_end] if content_end > 0 else ''

        is_pic = (
            not _SPECIAL_ID_RE.match(sid)
            and bool(_IMG_RE.search(content))
            and not bool(_HEADING_RE.search(content))
        )
        steps.append({'id': sid, 'is_picture': is_pic})
    return steps


def _get_tag_range(html: str, step_id: str):
    """返回 (start, end) — 目标 step 的 <div...> 开始标签范围。"""
    m = re.search(r'\bid\s*=\s*"' + re.escape(step_id) + r'"', html)
    if not m:
        return None, None
    div_start = html.rfind('<div', 0, m.start())
    if div_start < 0:
        return None, None
    i = div_start
    in_q = False
    qc = ''
    while i < len(html):
        c = html[i]
        if in_q:
            if c == qc:
                in_q = False
        elif c in '"\'':
            in_q = True
            qc = c
        elif c == '>':
            return div_start, i + 1
        i += 1
    return None, None


def _fmt(coords: dict) -> str:
    """生成规范格式的坐标属性行。"""
    if 'rel_to' in coords:
        return (
            f'    data-rel-to   = "{coords["rel_to"]}"\n'
            f'    data-rel-x    = "{coords["rel_x"]}"\n'
            f'    data-rel-y    = "{coords["rel_y"]}"\n'
            f'    data-rel-z    = "{coords["rel_z"]}"'
        )
    return (
        f'    data-x        = "{coords["x"]}"\n'
        f'    data-y        = "{coords["y"]}"\n'
        f'    data-z        = "{coords["z"]}"'
    )


def _apply(html: str, step_id: str, coords: dict) -> str:
    """将坐标写入 HTML 中指定 step 的开始标签。"""
    start, end = _get_tag_range(html, step_id)
    if start is None:
        print(f'  WARNING: {step_id!r} 未找到', file=sys.stderr)
        return html
    tag = _COORD_RE.sub('', html[start:end])  # 删除旧坐标属性
    body = tag.rstrip()
    if body.endswith('>'):
        body = body[:-1].rstrip()
    new_tag = body + '\n' + _fmt(coords) + '>\n'
    return html[:start] + new_tag + html[end:]


# ── 布局计算 ───────────────────────────────────────────────────────────────

def _project_root(start: Path) -> Path:
    for p in [start.resolve(), *start.resolve().parents]:
        if (p / 'CLAUDE.md').exists():
            return p
    import os
    cwd = Path(os.getcwd()).resolve()
    for p in [cwd, *cwd.parents]:
        if (p / 'CLAUDE.md').exists():
            return p
    return cwd


def _auto(ids: list, pattern: str):
    re_p = re.compile(pattern)
    return next((s for s in ids if re_p.match(s)), None)


def compute_coords(config: dict, steps: list[dict]) -> dict:
    """返回 {step_id: coords_dict}，只含需要更新坐标的步骤。"""
    ids = [s['id'] for s in steps]
    pic_ids = {s['id'] for s in steps if s['is_picture']}

    title_id = config.get('title') or _auto(ids, r'^c\d+t$')
    mindmap_id = config.get('mindmap') or _auto(ids, r'^mm\d+$')
    # nav (cXXq) 不修改坐标 — 保留手工设置的旋转和缩放

    spacing_y = int(config.get('spacing_y', 1100))
    corridor_x = int(config.get('corridor_x', 2200))
    single_branch_x = int(config.get('single_branch_x', 400))
    right_branch_extra_x = int(config.get('right_branch_extra_x', 600))
    mindmap_y = int(config.get('mindmap_y', -2000))
    mindmap_x = int(config.get('mindmap_x', 0))
    layout_mode = str(config.get('layout_mode', 'standard'))
    wrap_title_inner_y = int(config.get('wrap_title_inner_y', 1200))
    wrap_title_outer_y = int(config.get('wrap_title_outer_y', -2000))

    branches = config.get('branches', [])
    n = len(branches)
    half = (n - 1) / 2.0
    if n == 1:
        # 标题居中而正文左对齐时，唯一内容组放在 x=0 会显得偏左。
        # 默认向右补偿 400，让视觉重心更接近标题中心。
        base_x_offsets = [single_branch_x]
    else:
        base_x_offsets = [int((i - half) * corridor_x) for i in range(n)]

    # 视觉补偿只影响最终摆位，不应改变 wrap-title 的内外侧判断。
    # 否则像 4 分支这类偶数布局，右内侧分支会因额外 +600 被误判成外侧。
    x_offsets = [
        x + right_branch_extra_x if x > 0 else x
        for x in base_x_offsets
    ]

    result = {}

    if mindmap_id and title_id:
        result[mindmap_id] = {
            'rel_to': title_id, 'rel_x': mindmap_x,
            'rel_y': mindmap_y, 'rel_z': 0,
        }

    for bi, branch in enumerate(branches):
        x = x_offsets[bi]
        wrap_ref_x = base_x_offsets[bi]
        prev_id = title_id
        first_content = True

        for sid in branch.get('steps', []):
            if sid in pic_ids:
                # 图片页叠加在前一内容页上（z=10）
                result[sid] = {
                    'rel_to': prev_id, 'rel_x': 0, 'rel_y': 0, 'rel_z': 10,
                }
            else:
                if first_content:
                    # 分支第一步：从 title 出发，按 x 偏移定位
                    first_y = spacing_y
                    if layout_mode == 'wrap-title':
                        # 标题保护区: |x_offset| <= corridor_x / 2
                        # 内侧分支放在标题下方，外侧分支上移包围标题
                        if abs(wrap_ref_x) <= (corridor_x / 2.0):
                            first_y = wrap_title_inner_y
                        else:
                            first_y = wrap_title_outer_y
                    result[sid] = {
                        'rel_to': title_id, 'rel_x': x,
                        'rel_y': first_y, 'rel_z': 0,
                    }
                    first_content = False
                else:
                    result[sid] = {
                        'rel_to': prev_id, 'rel_x': 0,
                        'rel_y': spacing_y, 'rel_z': 0,
                    }
                prev_id = sid

    return result


# ── 主流程 ─────────────────────────────────────────────────────────────────

def run(yaml_path: str, dry_run: bool = False) -> None:
    cfg = Path(yaml_path).resolve()
    with open(cfg, encoding='utf-8') as f:
        config = _load_yaml(f.read())

    html_rel = config.get('html')
    if not html_rel:
        sys.exit('YAML 缺少 html 字段')

    root = _project_root(cfg.parent)
    html_path = root / html_rel
    if not html_path.exists():
        sys.exit(f'HTML 不存在: {html_path}')

    with open(html_path, encoding='utf-8') as f:
        html = f.read()

    steps = _parse_steps(html)
    pic_list = [s['id'] for s in steps if s['is_picture']]
    print(f'解析到 {len(steps)} 个步骤', end='')
    print(f'，图片页: {pic_list}' if pic_list else '')

    coords_map = compute_coords(config, steps)

    if dry_run:
        print('\n[干跑] 以下坐标不写入文件:')
        for sid, c in coords_map.items():
            if 'rel_to' in c:
                print(f'  {sid:12s} rel-to={c["rel_to"]:10s} x={c["rel_x"]:6} y={c["rel_y"]:6} z={c["rel_z"]}')
            else:
                print(f'  {sid:12s} x={c["x"]:6} y={c["y"]:6} z={c["z"]}')
        return

    for sid, coords in coords_map.items():
        html = _apply(html, sid, coords)
        print(f'  ✓ {sid}')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\n✓ 写入: {html_path}')
    print(f'  建议运行: python3 .claude/skills/build-layout/check_layout.py {html_rel} --verbose')


def main():
    p = argparse.ArgumentParser(description='生成 impress.js 布局坐标')
    p.add_argument('yaml', help='YAML 配置文件路径')
    p.add_argument('--dry-run', '-n', action='store_true', help='只打印，不写入')
    args = p.parse_args()
    run(args.yaml, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
