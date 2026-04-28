#!/usr/bin/env python3
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {"scenario_id", "seed"}
BOUNDED_COLUMNS = {"precision", "recall", "f1"}
BOOLEAN_COLUMNS = {"SLO_pass"}


def validate_file(path: Path) -> list[str]:
    errors = []
    try:
        df = pd.read_csv(path)
    except Exception as e:
        return [f"cannot read CSV: {e}"]

    if df.empty:
        return ["file is empty"]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        errors.append(f"missing required columns: {missing}")

    for col in df.select_dtypes(include=[np.number]).columns:
        nans = int(df[col].isna().sum())
        if nans > 0:
            errors.append(f"column '{col}' has {nans} NaN values")

    for col in BOUNDED_COLUMNS & set(df.columns):
        vals = df[col].dropna()
        if (vals < 0).any() or (vals > 1).any():
            errors.append(f"column '{col}' has values outside [0, 1]")

    for col in BOOLEAN_COLUMNS & set(df.columns):
        vals = df[col].dropna()
        allowed = {True, False, 0, 1, "True", "False", "true", "false"}
        bad = set(vals.unique()) - allowed
        if bad:
            errors.append(f"column '{col}' has non-boolean values: {bad}")

    return errors


def main():
    ap = argparse.ArgumentParser(
        description="Validate ResilienceBench result CSV files")
    ap.add_argument(
        "--reports-dir", "-r", type=Path, default=Path("eval/reports"))
    args = ap.parse_args()

    csvs = sorted(args.reports_dir.glob("*_report.csv"))
    if not csvs:
        print(f"No report CSVs found in {args.reports_dir}")
        sys.exit(1)

    total_errors = 0
    for path in csvs:
        errors = validate_file(path)
        status = "PASS" if not errors else "FAIL"
        print(f"[{status}] {path.name}")
        for e in errors:
            print(f"  - {e}")
        total_errors += len(errors)

    print(f"\n{len(csvs)} files checked, {total_errors} errors")
    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
