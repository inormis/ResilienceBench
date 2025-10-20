#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", "-i", type=Path, required=True)
    ap.add_argument("--out", "-o", type=Path, required=True)
    ap.add_argument("--metric", "-m", type=str, default="latency_ms")
    ap.add_argument("--window", "-w", type=int, default=60)
    ap.add_argument("--k", "-k", type=float, default=3.0)
    args = ap.parse_args()

    df = pd.read_csv(args.inp, parse_dates=["ts"])
    v = df[args.metric].astype(float)
    roll_mean = v.rolling(args.window, min_periods=max(2, args.window // 4)).mean()
    roll_std = v.rolling(args.window, min_periods=max(2, args.window // 4)).std(ddof=0).replace(0, np.nan)
    z = (v - roll_mean) / roll_std
    pred = (z.abs() > args.k).astype(int).fillna(0)
    out = df.assign(pred=pred)[["ts", "t_s", "pred"]]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)

if __name__ == "__main__":
    main()