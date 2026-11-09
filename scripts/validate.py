#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--root", default=".")
    root = Path(ap.parse_args().root)
    bad = [p for p in root.rglob("*") if p.is_file() and p.suffix in {".js", ".mjs", ".cjs", ".ts", ".tsx"} and ".git" not in p.parts]
    if bad:
        print("forbidden script files: " + ", ".join(str(p) for p in bad), file=sys.stderr); return 1
    html = sorted((root / "src/html").rglob("*.html"))
    css = sorted((root / "src/css").rglob("*.css"))
    if not html or not css:
        print("missing html or css", file=sys.stderr); return 1
    for p in html:
        if "components" not in p.parts and "<!doctype html>" not in p.read_text(encoding="utf-8").lower():
            print(f"{p}: missing doctype", file=sys.stderr); return 1
    for p in css:
        text = p.read_text(encoding="utf-8")
        if text.count("{") != text.count("}"):
            print(f"{p}: unbalanced braces", file=sys.stderr); return 1
    print(f"ui validation ok ({len(html)} html, {len(css)} css)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
