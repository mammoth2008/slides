#!/usr/bin/env python3
"""
chinese_fix.py — Markdown 源码排版修复工具

用法:
    python3 chinese_fix.py [file.md]
    cat file.md | python3 chinese_fix.py

排版规则(与 chinese_fix.md 同步):
  规则零 · 结构冻结:围栏代码块/行内代码/图片/链接/裸 URL 整段保护
  规则一 · 全角标点 → ASCII 等宽替换
  规则二 · 括号统一 ASCII,外侧加空格,内侧去空格
  规则三 · ASCII 双引号外侧加空格,内侧去空格
  规则四 · 列表行尾清理(ASCII 问号保留)
  规则五 · 英文标点 . , : ? 后跟 CJK 时加空格(数字两侧豁免)
  规则六 · CJK 与字母/数字/% 之间加空格(含 placeholder 边界)
  规则七 · 运算符 = < > + & 在 CJK 参与时两侧加空格
  规则八 · CJK 之间的斜杠 / 两侧加空格
"""

import sys
import re


# ─────────────────────────────────────────
#  字符类
# ─────────────────────────────────────────
CJK = r'[\u4E00-\u9FFF\u3400-\u4DBF]'
ANS = r'[a-zA-Z0-9%]'
OP = r'[=<>&+]'

FULLWIDTH_MAP = {
    '，': ',', '、': ',', '；': ',', '：': ':',
    '？': '?', '！': '!', '…': '...',
    '\u201c': '"', '\u201d': '"',  # 中文双引号 "" → ASCII "
    '\u2018': "'", '\u2019': "'",  # 中文单引号 '' → ASCII '
}


# ─────────────────────────────────────────
#  规则零 · Markdown 结构冻结
#    占位符双前缀:F<idx> = 跨行围栏,I<idx> = 行内片段
#    两层 storage 独立 — 避免 process_line 内层 thaw 吞掉外层 slot
# ─────────────────────────────────────────

SLOT_TOKEN = r'\x00[FI]\d+\x00'          # 规则六边界识别共用
FENCE_SLOT_RE = re.compile(r'\x00F(\d+)\x00')
INLINE_SLOT_RE = re.compile(r'\x00I(\d+)\x00')

FENCE_RE = re.compile(r'```[\s\S]*?```')
INLINE_CODE_RE = re.compile(r'`[^`\n]+`')
IMAGE_RE = re.compile(r'!\[[^\]]*\]\([^)]*\)')
LINK_RE = re.compile(r'\[[^\]]*\]\([^)]*\)')
URL_RE = re.compile(r'https?://[^\s\u4E00-\u9FFF]*[a-zA-Z0-9/]')


def _freeze(text: str, pattern: re.Pattern, storage: list, tag: str) -> str:
    def replace(m):
        idx = len(storage)
        storage.append(m.group(0))
        return f'\x00{tag}{idx}\x00'
    return pattern.sub(replace, text)


def _thaw(text: str, storage: list, slot_re: re.Pattern) -> str:
    prev = None
    while prev != text:
        prev = text
        text = slot_re.sub(lambda m: storage[int(m.group(1))], text)
    return text


# ─────────────────────────────────────────
#  规则一 · 全角标点 → ASCII
# ─────────────────────────────────────────

def fix_punctuation(line: str) -> str:
    line = line.replace('——', '-')
    return ''.join(FULLWIDTH_MAP.get(ch, ch) for ch in line)


# ─────────────────────────────────────────
#  规则二 · 括号间距
# ─────────────────────────────────────────

def fix_brackets(line: str) -> str:
    s = line.replace('（', '(').replace('）', ')')
    s = re.sub(r'\(\s*', '(', s)
    s = re.sub(r'\s*\)', ')', s)
    s = re.sub(r'(\S)\(', r'\1 (', s)
    s = re.sub(r'\)(\S)', r') \1', s)
    if s.startswith('('):
        s = ' ' + s
    if s.endswith(')'):
        s = s + ' '
    return s


# ─────────────────────────────────────────
#  规则三 · 引号间距
# ─────────────────────────────────────────

def fix_quotes(line: str) -> str:
    s = re.sub(r'"([^"]*)"', lambda m: '"' + m.group(1).strip() + '"', line)
    result = []
    count = 0
    for i, ch in enumerate(s):
        if ch == '"':
            count += 1
            if count % 2 == 1:
                if result and result[-1] not in ' \t':
                    result.append(' ')
                result.append('"')
            else:
                result.append('"')
                next_ch = s[i + 1] if i + 1 < len(s) else ''
                if next_ch and next_ch not in ' \t':
                    result.append(' ')
        else:
            result.append(ch)
    return ''.join(result)


# ─────────────────────────────────────────
#  规则四 · 列表项行尾清理
# ─────────────────────────────────────────

LIST_TRAIL_RE = re.compile(
    r'^(\s*- \s*)'
    r'([^\n]*?)'
    r'(\s*[，。、；：！…\-,.:]+\s*)$'
)

def fix_list_trailing(line: str) -> str:
    m = LIST_TRAIL_RE.match(line)
    if m:
        return m.group(1) + m.group(2).rstrip()
    return line


# ─────────────────────────────────────────
#  规则五 · 英文标点后跟 CJK 时加空格
#    后必须是 CJK → 自动豁免 1.5 / 1,000 / file.py / URL
# ─────────────────────────────────────────

ENG_PUNCT_SPACE_RE = re.compile(r'([.,:?])(' + CJK + ')')

def fix_english_punct_space(line: str) -> str:
    return ENG_PUNCT_SPACE_RE.sub(r'\1 \2', line)


# ─────────────────────────────────────────
#  规则六 · CJK ↔ 字母/数字/% 间距
#    同时处理 placeholder 与 CJK 的边界(代码/链接/URL 两侧)
# ─────────────────────────────────────────

CJK_ANS_RE1 = re.compile(r'(' + CJK + ')(' + ANS + ')')
CJK_ANS_RE2 = re.compile(r'(' + ANS + ')(' + CJK + ')')
CJK_SLOT_RE = re.compile(r'(' + CJK + ')(' + SLOT_TOKEN + ')')
SLOT_CJK_RE = re.compile(r'(' + SLOT_TOKEN + ')(' + CJK + ')')

def fix_cjk_ans(line: str) -> str:
    line = CJK_ANS_RE1.sub(r'\1 \2', line)
    line = CJK_ANS_RE2.sub(r'\1 \2', line)
    line = CJK_SLOT_RE.sub(r'\1 \2', line)
    line = SLOT_CJK_RE.sub(r'\1 \2', line)
    return line


# ─────────────────────────────────────────
#  规则七 · 运算符间距(= < > + &)
#    只在 CJK 参与时两侧加空格;纯 ASCII 场景不动(避免 a=b 被拆)
#    不含 | * - / # — 避开 Markdown 语法字符
# ─────────────────────────────────────────

CJK_OP_ANS_RE = re.compile(r'(' + CJK + r')\s*(' + OP + r')\s*(' + ANS + ')')
ANS_OP_CJK_RE = re.compile(r'(' + ANS + r')\s*(' + OP + r')\s*(' + CJK + ')')
CJK_OP_CJK_RE = re.compile(r'(' + CJK + r')\s*(' + OP + r')\s*(' + CJK + ')')

def fix_operators(line: str) -> str:
    line = CJK_OP_ANS_RE.sub(r'\1 \2 \3', line)
    line = ANS_OP_CJK_RE.sub(r'\1 \2 \3', line)
    line = CJK_OP_CJK_RE.sub(r'\1 \2 \3', line)
    return line


# ─────────────────────────────────────────
#  规则八 · 斜杠间距
#    只处理 CJK/CJK,URL 已由规则零冻结,安全
# ─────────────────────────────────────────

SLASH_RE = re.compile(r'(' + CJK + r')/(' + CJK + ')')

def fix_slashes(line: str) -> str:
    return SLASH_RE.sub(r'\1 / \2', line)


# ─────────────────────────────────────────
#  主流程
# ─────────────────────────────────────────

def _freeze_inline(line: str):
    storage = []
    line = _freeze(line, INLINE_CODE_RE, storage, 'I')
    line = _freeze(line, IMAGE_RE, storage, 'I')
    line = _freeze(line, LINK_RE, storage, 'I')
    line = _freeze(line, URL_RE, storage, 'I')
    return line, storage


def process_line(line: str) -> str:
    line, storage = _freeze_inline(line)
    line = fix_punctuation(line)
    line = fix_list_trailing(line)
    line = fix_brackets(line)
    line = fix_quotes(line)
    line = fix_english_punct_space(line)
    line = fix_cjk_ans(line)
    line = fix_operators(line)
    line = fix_slashes(line)
    line = _thaw(line, storage, INLINE_SLOT_RE)
    return line


def process(content: str) -> str:
    storage = []
    content = _freeze(content, FENCE_RE, storage, 'F')
    lines = [process_line(line) for line in content.splitlines()]
    content = '\n'.join(lines)
    return _thaw(content, storage, FENCE_SLOT_RE)


def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        if path == '-':
            print(process(sys.stdin.read()), end='')
        else:
            with open(path, 'r', encoding='utf-8') as f:
                original = f.read()
            fixed = process(original)
            if fixed != original:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(fixed)
                print(f'✓ {path}')
            else:
                print(f'  {path}  (无变化)')
    else:
        print(process(sys.stdin.read()), end='')


if __name__ == '__main__':
    main()
