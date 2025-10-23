#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--reports", type=Path, default=Path("eval/reports"))
    ap.add_argument("-o", "--out", type=Path, default=Path("interop/out/report.ndjson"))
    args = ap.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    csvs = sorted(args.reports.glob("*_report.csv"))
    if not csvs: raise SystemExit("no report CSVs found")

    with args.out.open("w", encoding="utf-8") as w:
        for p in csvs:
            df = pd.read_csv(p)
            for _, row in df.iterrows():
                w.write(json.dumps(row.to_dict(), ensure_ascii=False) + "\n")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
