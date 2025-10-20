#!/usr/bin/env python3
from __future__ import annotations
import argparse, random
from pathlib import Path
from datetime import datetime, timezone
import yaml, numpy as np, pandas as pd

def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def iso(ts0: datetime, t: np.ndarray) -> pd.Series:
    return pd.to_datetime(ts0) + pd.to_timedelta(t, unit="s")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", "-s", type=Path, required=True)
    ap.add_argument("--out", "-o", type=Path, required=True)
    args = ap.parse_args()

    sc = load_yaml(args.scenario)
    prof = load_yaml((args.scenario.parent / sc["system_profile"]).resolve())
    seed = int(sc["reproducibility"]["seed"])
    random.seed(seed); np.random.seed(seed)

    hz = int(prof.get("sampling_defaults_hz", 1))
    dur = int(sc["dataset"]["duration_s"])
    t = np.arange(0, dur, 1 / hz)
    ts0 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    lat_nom = float(prof["metrics"]["latency_ms"]["nominal"])
    thr_nom = float(prof.get("metrics", {}).get("throughput_rps", {}).get("nominal", 200))
    err_nom = float(prof["metrics"]["error_rate_pct"]["nominal"])

    latency = np.full_like(t, lat_nom, dtype=float) + np.random.normal(0, 5.0, size=t.size)
    throughput = np.full_like(t, thr_nom, dtype=float) + np.random.normal(0, thr_nom * 0.03, size=t.size)
    error_rate = np.clip(np.random.normal(err_nom, err_nom * 0.25, size=t.size), 0, None)

    f = sc["failure"]; start = float(f["start_s"]); end = start + float(f["duration_s"])
    mask = (t >= start) & (t <= end)

    if f["type"] == "latency_spike":
        mag = float(f["parameters"]["magnitude_ms"])
        decay = float(f["parameters"].get("decay_s", f["duration_s"]))
        latency[mask] += mag
        tail = (t > end) & (t <= end + decay)
        latency[tail] += mag * np.exp(-(t[tail] - end) / decay)
        error_rate[mask] += 0.2
    elif f["type"] == "node_crash":
        latency[mask] += 250; error_rate[mask] += 1.0; throughput[mask] *= 0.6
    elif f["type"] == "network_partition":
        latency[mask] += 300; error_rate[mask] += 1.5; throughput[mask] *= 0.5
    elif f["type"] == "slowdown":
        mag = float(f["parameters"].get("magnitude_ms", 120))
        drop = float(f["parameters"].get("throughput_drop_pct", 25)) / 100.0
        latency[mask] += mag; throughput[mask] *= (1.0 - drop)
    elif f["type"] == "corruption":
        spike = float(f["parameters"].get("error_spike_pct", 1.0))
        error_rate[mask] += spike

    df = pd.DataFrame({
        "ts": iso(ts0, t),
        "t_s": t.astype(int),
        "latency_ms": latency,
        "error_rate_pct": error_rate,
        "throughput_rps": throughput
    })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)

if __name__ == "__main__":
    main()