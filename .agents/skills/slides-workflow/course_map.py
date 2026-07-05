#!/usr/bin/env python3
from __future__ import annotations

"""
course_map.py — 扫描课程目录结构，输出进度对照表

用法：
    python3 course_map.py [课程目录]
    python3 course_map.py              # 扫描所有课程
    python3 course_map.py pmi          # 只扫描 pmi

输出格式：
    Markdown 表格，逐课程列出各节是否有 md 源码、是否有 html 输出。

课程目录对应关系：
    ~/Documents/products/courses/library/texts/{course}-slide-drafts/slide-drafts/  → md 源码
    {course_num}{course}/  → html 输出

例如：pmi-slide-drafts/slide-drafts/ ↔ 10pmi/，gai-slide-drafts/slide-drafts/ ↔ 5gai/
"""

import os
import re
import sys
from pathlib import Path

COURSES_TEXT_ROOT = (
    Path(os.environ['COURSES_TEXT_ROOT'])
    if os.environ.get('COURSES_TEXT_ROOT')
    else Path.home() / 'Documents/products/courses/library/texts'
)

# ─────────────────────────────────────────
#  课程配置：prefix → (html目录, 源包目录, 主课件 md 子目录)
# ─────────────────────────────────────────
# html_dir: 含数字前缀的目录名（生成产物）
# package:  courses vault library/texts/ 下的源包目录
# subdir:   源包内的主课件 md 子目录
COURSE_CONFIG = {
    'pmi':    ('10pmi', 'pmi-slide-drafts', 'slide-drafts'),
    'gai':    ('5gai', 'gai-slide-drafts', 'slide-drafts'),
    'cciot':  ('2cciot', 'cciot-slide-drafts', 'slide-drafts'),
    'itpm':   ('3itpm', 'itpm-slide-drafts', 'slide-drafts'),
    'ita':    ('6ita', 'ita-slide-drafts', 'slide-drafts'),
    'il':     ('8il', 'il-slide-drafts', 'slide-drafts'),
    'fiit':   ('9fiit', 'fiit-slide-drafts', 'slide-drafts'),
    'dbpa':   ('1dbpa', 'dbpa-slide-drafts', 'slide-drafts'),
}

# md 源码中哪些文件名不算课程节（忽略这些）
MD_IGNORE = {
    'pmi':    set(),
    'gai':    {'gai-2025.md'},
    'cciot':  set(),
    # mindmap 文件不计入 md 数量（它们不按 {course}-N-N.md 命名，生成同名但不同前缀的 html）
    'itpm':   set(),
    'ita':    {'ita-2-2-lecture.md'},  # 非节内容
    'il':     set(),
    'fiit':   set(),
    'dbpa':   set(),
    '_all':   {'_all'},  # 标记：以下课程统一忽略所有 mindmap 文件
}

# 以下课程统一忽略 mindmap 文件（md 文件名不以课程前缀命名）
MINDMAP_IGNORE_COURSES = {'cciot', 'ita', 'dbpa', 'il', 'fiit'}


def source_md_dir(course: str) -> Path:
    """返回课程资料库中的主课件 md 目录。"""
    _html_dir, package, subdir = COURSE_CONFIG[course]
    return COURSES_TEXT_ROOT / package / subdir


def md_files_by_section(course: str, md_dir: Path) -> dict[tuple[int, int], str]:
    """返回 {(章, 节): filename}，只含课程节，跳过忽略名单"""
    ignore = MD_IGNORE.get(course, set())
    is_mindmap_course = course in MINDMAP_IGNORE_COURSES
    result = {}
    path = Path(md_dir)
    if not path.exists():
        return result
    for f in sorted(path.iterdir()):
        if f.suffix != '.md':
            continue
        if f.name in ignore:
            continue
        # 忽略 mindmap 文件（部分课程）
        if is_mindmap_course and f.name.startswith('mindmap'):
            continue
        sec = parse_section(f.name)
        if sec:
            # PMI 源包同时可能有 pmi-* 和 gpmi-*；文本主课件 pmi-* 优先。
            if sec not in result or f.name.startswith(f'{course}-'):
                result[sec] = f.name
    return result


# ─────────────────────────────────────────
#  文件名解析
# ─────────────────────────────────────────

SECTION_RE = re.compile(r'^[a-z]+-(\d+)-(\d+)\.md$')


def parse_section(filename: str) -> tuple[int, int] | None:
    """返回 (章节号, 节号)，失败返回 None"""
    m = SECTION_RE.match(filename)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return None



def html_files_by_section(course: str, html_dir: str) -> dict[tuple[int, int], str]:
    """返回 {(章, 节): filename}"""
    result = {}
    path = Path(html_dir)
    if not path.exists():
        return result
    for f in sorted(path.iterdir()):
        if f.suffix != '.html':
            continue
        # 提取节编号：pmi-1-1.html, case-2-1.html 等
        name = f.stem
        # 先尝试主前缀模式
        m = re.match(r'^[a-z]+-(\d+)-(\d+)$', name)
        if m:
            sec = (int(m.group(1)), int(m.group(2)))
            if sec not in result or f.name.startswith(f'{course}-'):
                result[sec] = f.name
    return result


# ─────────────────────────────────────────
#  渲染
# ─────────────────────────────────────────

def section_key(k: tuple[int, int]) -> tuple:
    return k  # (章, 节) 自然顺序


def render_course(course: str, html_dir: str, md_dir: str) -> str:
    md_secs = md_files_by_section(course, md_dir)
    html_secs = html_files_by_section(course, html_dir)

    all_secs = sorted(set(md_secs.keys()) | set(html_secs.keys()), key=section_key)

    if not all_secs:
        return f'### {course.upper()}\n\n*目录为空*\n'

    # 表头
    lines = [
        f'### {course.upper()}',
        '',
        '| 章.节 | md 源码 | html 输出 |',
        '|-----|---------|----------|',
    ]

    for sec in all_secs:
        ch, num = sec
        label = f'{ch}.{num}'
        md_file = md_secs.get(sec, '')
        html_file = html_secs.get(sec, '')

        md_cell = f'`{md_file}`' if md_file else '—'
        html_cell = f'`{html_file}`' if html_file else '—'

        lines.append(f'| {label} | {md_cell} | {html_cell} |')

    lines.append('')
    return '\n'.join(lines)


# ─────────────────────────────────────────
#  汇总统计
# ─────────────────────────────────────────

def coverage_note(pct: float, md_count: int) -> str:
    """覆盖率旁注：超过 100% 时提示 html 溢出（无 md 对应）"""
    if md_count == 0:
        return '（无 md）'
    if pct > 100:
        extra = round((pct - 100) * md_count / 100)
        return f'（约 {extra} 个 html 无 md）'
    return ''


def render_summary(courses: list[str]) -> str:
    total_md = 0
    total_html = 0
    rows = ['| 课程 | md 源码 | html 输出 | 覆盖率 |',
            '|-----|---------|----------|-------|']

    for course in sorted(courses):
        html_dir = COURSE_CONFIG[course][0]
        md_secs = md_files_by_section(course, source_md_dir(course))
        html_secs = html_files_by_section(course, html_dir)
        total_md += len(md_secs)
        total_html += len(html_secs)
        pct = (len(html_secs) / len(md_secs) * 100) if md_secs else 0
        note = coverage_note(pct, len(md_secs))
        rows.append(f'| {course} | {len(md_secs)} | {len(html_secs)} | {pct:.0f}% {note} |')

    rows.append(f'| **合计** | **{total_md}** | **{total_html}** | — |')
    rows.append('')
    return '\n'.join(rows)


# ─────────────────────────────────────────
#  主入口
# ─────────────────────────────────────────

def main():
    if len(sys.argv) >= 2:
        courses = [arg for arg in sys.argv[1:] if arg in COURSE_CONFIG]
        if not courses:
            print(f'未知课程：{sys.argv[1]}，已知：{", ".join(COURSE_CONFIG)}', file=sys.stderr)
            sys.exit(1)
    else:
        courses = list(COURSE_CONFIG.keys())

    # 汇总
    print(f'Source root: `{COURSES_TEXT_ROOT}`\n')
    print(render_summary(courses))

    # 逐课程详情
    for course in sorted(courses):
        html_dir = COURSE_CONFIG[course][0]
        print(render_course(course, html_dir, source_md_dir(course)))


if __name__ == '__main__':
    main()
