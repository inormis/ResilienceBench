#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def main():
    ap = argparse.ArgumentParser(
        description="CUSUM (Cumulative Sum) control chart anomaly detector")
    ap.add_argument("--inp", "-i", type=Path, required=True)
    ap.add_argument("--out", "-o", type=Path, required=True)
    ap.add_argument("--metric", "-m", type=str, default="latency_ms")
    ap.add_argument("--drift", type=float, default=0.5,
                    help="Allowance parameter (in std dev units)")
    ap.add_argument("--threshold", "-t", type=float, default=5.0,
                    help="Decision threshold (in std dev units)")
    args = ap.parse_args()

    df = pd.read_csv(args.inp, parse_dates=["ts"])
    v = df[args.metric].astype(float).to_numpy()
    mu = np.mean(v)
    sigma = np.std(v, ddof=0)
    if sigma == 0:
        sigma = 1.0

    z = (v - mu) / sigma
    n = len(z)
    s_hi = np.zeros(n)
    s_lo = np.zeros(n)
    pred = np.zeros(n, dtype=int)

    for i in range(1, n):
        s_hi[i] = max(0, s_hi[i - 1] + z[i] - args.drift)
        s_lo[i] = max(0, s_lo[i - 1] - z[i] - args.drift)
        if s_hi[i] > args.threshold or s_lo[i] > args.threshold:
            pred[i] = 1
            s_hi[i] = 0
            s_lo[i] = 0

    out = df.assign(pred=pred)[["ts", "t_s", "pred"]]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)


if __name__ == "__main__":
    main()
