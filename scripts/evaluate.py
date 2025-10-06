#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd, typer, yaml

app = typer.Typer(add_completion=False)

def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def dilate(mask: np.ndarray, k: int) -> np.ndarray:
    if k <= 0: return mask
    n = mask.size
    m = mask.copy()
    for _ in range(k):
        left = np.concatenate(([False], m[:-1]))
        right = np.concatenate((m[1:], [False]))
        m = m | left | right
    return m

@app.command()
def main(scenario: Path, data: Path, pred: Path | None = None, out: Path | None = None):
    sc = load_yaml(scenario)
    df = pd.read_csv(data, parse_dates=["ts"])
    warmup = int(sc["dataset"].get("warmup_s", 0))
    x = df[df["t_s"] >= warmup].copy()

    p99 = float(np.percentile(x["latency_ms"], 99))
    p999 = float(np.percentile(x["latency_ms"], 99.9))
    err = float(x["error_rate_pct"].mean())

    av = sc.get("evaluation", {}).get("availability", None)
    A = None
    MTBF = None
    MTTR = None
    if av:
        MTBF = float(av.get("mtbf_s", 0))
        MTTR = float(av.get("mttr_s", 0))
        if MTBF > 0 and MTTR > 0:
            A = MTBF / (MTBF + MTTR)

    slo = sc.get("evaluation", {}).get("slo", {})
    slo_ok = True
    if "latency_ms_p99" in slo:
        slo_ok = slo_ok and (p99 <= float(slo["latency_ms_p99"]))
    if "error_rate_pct" in slo:
        slo_ok = slo_ok and (err <= float(slo["error_rate_pct"]))

    gt = sc["ground_truth"]["positive_interval_s"]
    tol = int(sc.get("evaluation", {}).get("detection", {}).get("window_tolerance_s", 0))
    t = x["t_s"].to_numpy()
    gt_mask = (t >= gt[0]) & (t <= gt[1])
    gt_mask = dilate(gt_mask, tol)

    if pred:
        pr = pd.read_csv(pred, parse_dates=["ts"])
        pr = pr[pr["t_s"] >= warmup]
        y = pr["pred"].to_numpy().astype(bool)
    else:
        y = np.zeros_like(gt_mask, dtype=bool)

    tp = int(np.sum(y & gt_mask))
    fp = int(np.sum(y & ~gt_mask))
    fn = int(np.sum(~y & gt_mask))
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    row = {
        "scenario_id": sc["id"],
        "seed": sc["reproducibility"]["seed"],
        "A": round(A, 6) if A is not None else "NA",
        "MTBF_s": MTBF if MTBF is not None else "NA",
        "MTTR_s": MTTR if MTTR is not None else "NA",
        "p99_latency_ms": round(p99, 3),
        "p99_9_latency_ms": round(p999, 3),
        "error_rate_pct": round(err, 4),
        "SLO_pass": bool(slo_ok),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }
    outp = out or Path("eval/reports") / f"{sc['id']}_report.csv"
    outp.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(outp, index=False)
    print(pd.DataFrame([row]).to_markdown(index=False))

if __name__ == "__main__":
    app()