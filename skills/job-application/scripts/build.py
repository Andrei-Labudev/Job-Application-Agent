"""
Build a resume or cover letter PDF from JSON and report the page count.

  python3 build.py resume <resume.json> <output.pdf>
  python3 build.py cover  <cover.json>  <output.pdf>

Requires: pip install reportlab pypdf
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cover_builder import build_cover  # noqa: E402
from resume_builder import build_resume  # noqa: E402


def page_count(path: str) -> int:
    from pypdf import PdfReader
    return len(PdfReader(path).pages)


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in ("resume", "cover"):
        print(__doc__)
        return 2
    kind, src, out = sys.argv[1:]
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    (build_resume if kind == "resume" else build_cover)(data, out)
    pages = page_count(out)
    print(f"Built {out}: {pages} page(s)")
    if pages > 1:
        print("OVER ONE PAGE: cut the least relevant bullets and rebuild (don't shrink fonts/margins).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
