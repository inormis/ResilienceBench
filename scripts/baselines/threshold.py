#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml, pandas as pd

def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", "-i", type=Path, required=True)
    ap.add_argument("--out", "-o", type=Path, required=True)
    ap.add_argument("--metric", "-m", type=str, default="latency_ms")
    ap.add_argument("--threshold", "-t", type=float, default=-1.0)
    ap.add_argument("--scenario", "-s", type=Path)
    args = ap.parse_args()

    thr = args.threshold
    if thr <= 0 and args.scenario:
        sc = load_yaml(args.scenario)
        slo = sc.get("evaluation", {}).get("slo", {})
        key = f"{args.metric}_p99"
        thr = float(slo.get(key, 0)) or float(slo.get(args.metric, 0)) or 250.0
    elif thr <= 0:
        thr = 250.0

    df = pd.read_csv(args.inp, parse_dates=["ts"])
    df["pred"] = (df[args.metric] > thr).astype(int)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df[["ts", "t_s", "pred"]].to_csv(args.out, index=False)

if __name__ == "__main__":
    main()