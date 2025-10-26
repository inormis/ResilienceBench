#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def bump(folder: Path, version: str) -> int:
    n = 0
    for p in folder.glob("*.yaml"):
        if p.name.startswith("_"): continue
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if data.get("version") != version:
            data["version"] = version
            p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
            n += 1
    return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="1.0.0")
    args = ap.parse_args()
    changed = 0
    changed += bump(ROOT/"benchmarks"/"scenarios", args.version)
    changed += bump(ROOT/"benchmarks"/"system_profiles", args.version)
    print(f"updated files: {changed}")

if __name__ == "__main__":
    main()