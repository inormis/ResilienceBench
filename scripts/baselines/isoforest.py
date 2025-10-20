#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from sklearn.ensemble import IsolationForest

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", "-i", type=Path, required=True)
    ap.add_argument("--out", "-o", type=Path, required=True)
    ap.add_argument("--features", "-f", nargs="+", default=["latency_ms","error_rate_pct"])
    ap.add_argument("--contam", "-c", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df = pd.read_csv(args.inp, parse_dates=["ts"])
    X = df[args.features].astype(float).fillna(method="ffill").fillna(method="bfill")
    model = IsolationForest(contamination=args.contam, random_state=args.seed)
    pred = (model.fit_predict(X) == -1).astype(int)
    out = df.assign(pred=pred)[["ts", "t_s", "pred"]]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)

if __name__ == "__main__":
    main()