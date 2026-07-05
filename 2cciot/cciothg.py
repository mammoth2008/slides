#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / ".agents/skills/slides-workflow/scripts"
if not SCRIPT_DIR.exists():
    SCRIPT_DIR = ROOT / ".claude/skills/slides-workflow/scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from generate_html import main


if __name__ == "__main__":
    main(sys.argv[1:], default_course="cciot")
