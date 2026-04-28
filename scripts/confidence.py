#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np
import pandas as pd
import yaml


def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def dilate(mask: np.ndarray, k: int) -> np.ndarray:
    if k <= 0:
        return mask
    m = mask.copy()
    for _ in range(k):
        left = np.concatenate(([False], m[:-1]))
        right = np.concatenate((m[1:], [False]))
        m = m | left | right
    return m


def compute_metrics(sc: dict, data: pd.DataFrame, pred: pd.DataFrame) -> dict:
    warmup = int(sc["dataset"].get("warmup_s", 0))
    x = data[data["t_s"] >= warmup].copy()
    pr = pred[pred["t_s"] >= warmup]

    targets = sc.get("evaluation", {}).get("tails", {}).get("p99_targets", ["latency_ms"])
    row = {}
    for m in targets:
        v = x[m].astype(float)
        row[f"p99_{m}"] = float(np.percentile(v, 99))

    row["error_rate_pct"] = float(x["error_rate_pct"].mean())

    gt = sc["ground_truth"]["positive_interval_s"]
    tol = int(sc.get("evaluation", {}).get("detection", {}).get("window_tolerance_s", 0))
    t = x["t_s"].to_numpy()
    gt_mask = (t >= gt[0]) & (t <= gt[1])
    gt_mask = dilate(gt_mask, tol)

    y = pr["pred"].to_numpy().astype(bool)
    tp = int(np.sum(y & gt_mask))
    fp = int(np.sum(y & ~gt_mask))
    fn = int(np.sum(~y & gt_mask))
    row["precision"] = tp / (tp + fp) if (tp + fp) else 0.0
    row["recall"] = tp / (tp + fn) if (tp + fn) else 0.0
    row["f1"] = (2 * row["precision"] * row["recall"] /
                 (row["precision"] + row["recall"])
                 if (row["precision"] + row["recall"]) else 0.0)
    return row


def main():
    ap = argparse.ArgumentParser(
        description="Bootstrap confidence intervals for ResilienceBench evaluation metrics")
    ap.add_argument("--scenario", "-s", type=Path, required=True)
    ap.add_argument("--data", "-d", type=Path, required=True)
    ap.add_argument("--pred", "-p", type=Path, required=True)
    ap.add_argument("--n-bootstrap", "-n", type=int, default=1000)
    ap.add_argument("--alpha", "-a", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", "-o", type=Path, required=True)
    args = ap.parse_args()

    sc = load_yaml(args.scenario)
    data = pd.read_csv(args.data, parse_dates=["ts"])
    pred = pd.read_csv(args.pred, parse_dates=["ts"])

    np.random.seed(args.seed)
    n = len(data)
    results: dict[str, list[float]] = {}

    for _ in range(args.n_bootstrap):
        idx = np.random.choice(n, size=n, replace=True)
        sample_data = data.iloc[idx].reset_index(drop=True)
        sample_pred = pred.iloc[idx].reset_index(drop=True)
        row = compute_metrics(sc, sample_data, sample_pred)
        for k, v in row.items():
            results.setdefault(k, []).append(v)

    lo = args.alpha / 2
    hi = 1.0 - lo
    rows = []
    for metric, vals in results.items():
        arr = np.array(vals)
        rows.append({
            "metric": metric,
            "mean": round(float(np.mean(arr)), 6),
            "ci_lower": round(float(np.percentile(arr, lo * 100)), 6),
            "ci_upper": round(float(np.percentile(arr, hi * 100)), 6),
        })

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["metric", "mean", "ci_lower", "ci_upper"])
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {args.out} ({len(rows)} metrics, {args.n_bootstrap} bootstrap iterations)")


if __name__ == "__main__":
    main()
