#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", "-s", type=Path, required=True)
    ap.add_argument("--data", "-d", type=Path, required=True)
    args = ap.parse_args()

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    val = Draft202012Validator(schema)

    errors = 0
    for i, line in enumerate(args.data.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        obj = json.loads(line)
        for e in val.iter_errors(obj):
            print(f"[line {i}] {e.message}")
            errors += 1
    if errors:
        raise SystemExit(f"validation failed: {errors} error(s)")
    print("ok")

if __name__ == "__main__":
    main()