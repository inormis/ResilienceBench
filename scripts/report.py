#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports", "-r", type=Path, default=Path("eval/reports"))
    ap.add_argument("--out", "-o", type=Path, default=Path("eval/reports/index.html"))
    ap.add_argument("--title", "-t", type=str, default="ResilienceBench Report")
    args = ap.parse_args()

    args.reports.mkdir(parents=True, exist_ok=True)
    csvs = sorted(args.reports.glob("*.csv"))
    if not csvs:
        raise SystemExit("no CSV reports found")

    frames = []
    for p in csvs:
        df = pd.read_csv(p)
        df.insert(0, "file", p.name)
        frames.append(df)

    table = pd.concat(frames, ignore_index=True)
    combined_csv = args.reports / "combined.csv"
    table.to_csv(combined_csv, index=False)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{args.title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial,sans-serif;margin:24px}}
h1{{font-size:20px;margin:0 0 12px}}
small{{color:#666}}
table{{border-collapse:collapse;width:100%;margin-top:16px}}
th,td{{border:1px solid #ddd;padding:8px;font-size:14px;text-align:left}}
th{{background:#fafafa}}
tr:nth-child(even){{background:#fbfbfb}}
code{{background:#f5f5f5;padding:2px 4px;border-radius:4px}}
</style>
</head>
<body>
<h1>{args.title}</h1>
<small>Generated: {ts}</small>
{table.to_html(index=False, escape=False)}
<p>Combined CSV: <code>{combined_csv.name}</code></p>
</body>
</html>"""
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
