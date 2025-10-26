#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def validate_folder(folder: Path, schema_path: Path) -> list[tuple[Path, str | None]]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    val = Draft202012Validator(schema)
    rows = []
    for p in sorted(folder.glob("*.yaml")):
        if p.name.startswith("_"): continue
        obj = load_yaml(p)
        errs = list(val.iter_errors(obj))
        rows.append((p, None if not errs else "; ".join(e.message for e in errs)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenarios", action="store_true")
    ap.add_argument("--profiles", action="store_true")
    args = ap.parse_args()

    if not args.scenarios and not args.profiles:
        args.scenarios = args.profiles = True

    code = 0
    if args.scenarios:
        rows = validate_folder(ROOT / "benchmarks" / "scenarios", ROOT / "schemas" / "scenario_v1.json")
        for p, err in rows:
            print(f"[scenario] {p.relative_to(ROOT)} :: {'OK' if err is None else 'FAIL ' + err}")
            if err: code = 1
    if args.profiles:
        rows = validate_folder(ROOT / "benchmarks" / "system_profiles", ROOT / "schemas" / "system_profile_v1.json")
        for p, err in rows:
            print(f"[profile]  {p.relative_to(ROOT)} :: {'OK' if err is None else 'FAIL ' + err}")
            if err: code = 1
    raise SystemExit(code)


if __name__ == "__main__":
    main()
