#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    manifest = {"version": (root / "VERSION").read_text().strip(), "files": {}}
    for sub in ("html", "css"):
        src = root / "src" / sub
        for p in sorted(src.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(root / "src")
            dest = out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            manifest["files"][str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()
    (out / "ui.css").write_text(
        "\n".join((out / "css" / n).read_text() for n in ("reset.css", "tokens.css", "layout.css", "utilities.css", "components.css")),
        encoding="utf-8",
    )
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"built {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
