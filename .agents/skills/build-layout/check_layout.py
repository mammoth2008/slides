#!/usr/bin/env python3
"""
check_layout.py — Validate impress.js slide layout.

Usage:
    python3 check_layout.py 10pmi/pmi-1-1.html
    python3 check_layout.py 10pmi/pmi-1-1.html --verbose

Checks:
    1. Chain breaks: data-rel-to target does not exist
    2. Overlapping pages: two steps share identical absolute (x, y, z)
    3. Spacing violations: |dy| < 1000 and |dx| < 2000 for consecutive steps
    4. Out-of-bounds pages: x or y outside +/-1500px
    5. Null positions: steps with unresolvable absolute coordinates
    6. Depth stacks: non-adjacent steps share x/y and differ only by z
"""

import re
import sys
import argparse
from collections import defaultdict


def parse_step_divs(html_path: str) -> list[dict]:
    """Parse all .step divs from the HTML file."""
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    # Match the opening <div ...> tag containing class="...step..."
    step_pat = re.compile(
        r'<div\b[^>]*\bclass\s*=\s*"[^"]*step[^"]*"[^>]*>',
        re.DOTALL,
    )
    # Extract quoted attributes
    attr_pat = re.compile(
        r'(\b(?:id|data-rel-to|data-rel-x|data-rel-y|data-rel-z|'
        r'data-x|data-y|data-z))\s*=\s*"([^"]*)"',
    )
    # Handle bare numeric values (no quotes) in generated HTML
    bare_pat = re.compile(
        r'(\b(?:data-rel-x|data-rel-y|data-rel-z|'
        r'data-x|data-y|data-z))\s*=\s*([\d.\-]+)',
    )

    steps = []
    for match in step_pat.finditer(content):
        opening = match.group(0)
        attrs = dict(attr_pat.findall(opening))
        # bare attrs take precedence if present (no quotes = explicit numeric)
        bare = dict(bare_pat.findall(opening))
        for k, v in bare.items():
            attrs[k] = v

        sid = attrs.get("id", "")
        # Skip special divs
        if not sid or sid in ("impress", "overview"):
            continue

        # has_abs: must have data-x AND data-y (data-z optional)
        has_abs = ("data-x" in attrs) and ("data-y" in attrs)

        steps.append({
            "index": len(steps),
            "id": sid,
            "rel_to": attrs.get("data-rel-to"),
            "rel_x": _n(attrs.get("data-rel-x", 0)),
            "rel_y": _n(attrs.get("data-rel-y", 0)),
            "rel_z": _n(attrs.get("data-rel-z", 0)),
            "has_abs": has_abs,
            "abs_x": _n(attrs.get("data-x", 0)),
            "abs_y": _n(attrs.get("data-y", 0)),
            "abs_z": _n(attrs.get("data-z", 0)),
        })

    return steps


def _n(val):
    """Convert to float, or return 0.0 for None/empty."""
    if val is None or val == "":
        return 0.0
    return float(val)


def compute_absolute_coords(steps: list[dict]) -> list[dict]:
    """Walk steps in DOM order, computing absolute coordinates.

    impress.js guarantees data-rel-to only references a prior step,
    so a single DOM-order pass is sufficient.
    """
    id_map = {}
    prev_abs = (0.0, 0.0, 0.0)

    for step in steps:
        abs_pos = None
        if step["has_abs"]:
            # True absolute: data-x AND data-y present
            abs_pos = (step["abs_x"], step["abs_y"], step["abs_z"])
        elif step["rel_to"] is not None:
            target = step["rel_to"]
            if target in id_map and id_map[target] is not None:
                px, py, pz = id_map[target]
                abs_pos = (px + step["rel_x"], py + step["rel_y"], pz + step["rel_z"])
            # else: chain break — abs_pos stays None
        else:
            abs_pos = prev_abs

        id_map[step["id"]] = abs_pos
        step["abs"] = abs_pos
        if abs_pos:
            prev_abs = abs_pos

    return steps


def check_chain_breaks(steps: list[dict]) -> list[str]:
    ids = {s["id"] for s in steps}
    return [
        f"  CHAIN BREAK: {s['id']} references missing data-rel-to=\"{s['rel_to']}\""
        for s in steps
        if s["rel_to"] is not None and s["rel_to"] not in ids
    ]


def check_null_positions(steps: list[dict]) -> list[str]:
    return [
        f"  NULL POSITION: {s['id']} has no computable absolute position "
        f"(chain break with no absolute fallback)"
        for s in steps
        if s["abs"] is None and not s["has_abs"]
    ]


def check_overlaps(steps: list[dict]) -> list[str]:
    pos_seen = defaultdict(list)
    for s in steps:
        if s["abs"] is not None:
            pos_seen[s["abs"]].append(s["id"])
    return [
        f"  OVERLAP at (x={pos[0]:.0f}, y={pos[1]:.0f}, z={pos[2]:.0f}): "
        f"{' overlaps '.join(ids)}"
        for pos, ids in pos_seen.items() if len(ids) > 1
    ]


def check_depth_stacks(steps: list[dict], shallow_z: float = 80.0) -> list[str]:
    """Report steps that sit on the same sightline but differ only by z.

    Adjacent shallow stacks are allowed because the slide system intentionally
    uses them for image/detail overlays. Non-adjacent stacks, or deep adjacent
    stacks, usually cause inactive pages to visually pierce the active page.
    """
    xy_seen = defaultdict(list)
    for s in steps:
        if s["abs"] is None:
            continue
        x, y, z = s["abs"]
        xy_seen[(x, y)].append(s)

    issues = []
    for (x, y), group in xy_seen.items():
        if len(group) < 2:
            continue
        group = sorted(group, key=lambda s: s["index"])
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                za, zb = a["abs"][2], b["abs"][2]
                dz = abs(zb - za)
                if dz == 0:
                    continue
                adjacent = abs(b["index"] - a["index"]) == 1
                if adjacent and dz <= shallow_z:
                    continue
                reason = "non-adjacent" if not adjacent else f"deep dz={dz:.0f}px"
                issues.append(
                    f"  DEPTH STACK at (x={x:.0f}, y={y:.0f}): "
                    f"{a['id']} z={za:.0f} and {b['id']} z={zb:.0f} "
                    f"share the same sightline ({reason}); "
                    f"use x/y spacing unless this is an intentional adjacent shallow overlay"
                )
    return issues


def check_spacing(steps: list[dict]) -> list[str]:
    issues = []
    for i in range(1, len(steps)):
        prev, curr = steps[i - 1], steps[i]
        if prev["abs"] is None or curr["abs"] is None:
            continue
        px, py, _ = prev["abs"]
        cx, cy, _ = curr["abs"]
        dx, dy = abs(cx - px), abs(cy - py)
        # Violation: both x and y spacing are too tight
        if dy < 1000 and dx < 2000:
            issues.append(
                f"  SPACING: {prev['id']} -> {curr['id']}: "
                f"|dx|={dx:.0f}px, |dy|={dy:.0f}px "
                f"(need |dy|>=1000 or |dx|>=2000)"
            )
    return issues


def check_bounds(steps: list[dict], bound: float = 1500.0) -> list[str]:
    issues = []
    for s in steps:
        if s["abs"] is None:
            continue
        x, y, z = s["abs"]
        if abs(x) > bound or abs(y) > bound:
            issues.append(
                f"  BOUNDS: {s['id']} at (x={x:.0f}, y={y:.0f}, z={z:.0f}) "
                f"outside +/-{bound}px bounding box"
            )
    return issues


def print_summary(steps: list[dict]) -> None:
    """Print all steps with their absolute coordinates."""
    print(f"\n{'ID':<10} {'rel-to':<12} {'rel (x,y,z)':<25} {'abs (x,y,z)':<30}")
    print("-" * 80)
    for s in steps:
        rel = f"({s['rel_x']:.0f},{s['rel_y']:.0f},{s['rel_z']:.0f})"
        a = s["abs"]
        if a is None:
            abs_str = "UNRESOLVED"
        else:
            abs_str = f"({a[0]:.0f},{a[1]:.0f},{a[2]:.0f})"
        print(f"{s['id']:<10} {str(s['rel_to'] or ''):<12} {rel:<25} {abs_str:<30}")


def run_checks(html_path: str, verbose: bool = False) -> int:
    """Run all checks. Returns 0 if all pass, 1 otherwise."""
    steps = parse_step_divs(html_path)
    if not steps:
        print(f"No .step divs found in {html_path}")
        return 1

    steps = compute_absolute_coords(steps)

    print(f"\n=== Layout Check: {html_path} ===")
    print(f"Total steps found: {len(steps)}")

    if verbose:
        print_summary(steps)

    all_issues = []
    for check_fn in (check_chain_breaks, check_null_positions,
                     check_overlaps, check_depth_stacks,
                     check_spacing, check_bounds):
        all_issues.extend(check_fn(steps))

    if all_issues:
        print(f"\n*** {len(all_issues)} issue(s) found: ***")
        for issue in all_issues:
            print(issue)
        return 1
    else:
        print("\nAll checks passed.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate impress.js slide layout.")
    parser.add_argument("html", help="Path to the HTML file to check")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print all step coordinates"
    )
    args = parser.parse_args()
    sys.exit(run_checks(args.html, verbose=args.verbose))
