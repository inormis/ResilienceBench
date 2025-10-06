#!/usr/bin/env python3
from __future__ import annotations
import math, random
from pathlib import Path
from datetime import datetime, timezone, timedelta
import typer, yaml, numpy as np, pandas as pd

app = typer.Typer(add_completion=False)

def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def iso(ts0: datetime, t: np.ndarray) -> pd.Series:
    return pd.to_datetime(ts0) + pd.to_timedelta(t, unit="s")

@app.command()
def main(scenario: Path, out: Path):
    sc = load_yaml(scenario)
    prof = load_yaml((scenario.parent / sc["system_profile"]).resolve())
    seed = int(sc["reproducibility"]["seed"])
    random.seed(seed); np.random.seed(seed)

    hz = int(prof.get("sampling_defaults_hz", 1))
    dur = int(sc["dataset"]["duration_s"])
    warmup = int(sc["dataset"].get("warmup_s", 0))
    t = np.arange(0, dur, 1 / hz)
    ts0 = datetime(2025, 1, 1, tzinfo=timezone.utc)

    latency = np.full_like(t, float(prof["metrics"]["latency_ms"]["nominal"]), dtype=float)
    latency += np.random.normal(0, 5.0, size=t.size)

    err_nom = float(prof["metrics"]["error_rate_pct"]["nominal"])
    error_rate = np.clip(np.random.normal(err_nom, err_nom * 0.25, size=t.size), 0, None)

    f = sc["failure"]
    start = float(f["start_s"])
    end = start + float(f["duration_s"])

    if f["type"] == "latency_spike":
        mag = float(f["parameters"]["magnitude_ms"])
        decay = float(f["parameters"].get("decay_s", f["duration_s"]))
        mask = (t >= start) & (t <= end)
        latency[mask] += mag
        tail = (t > end) & (t <= end + decay)
        latency[tail] += mag * np.exp(-(t[tail] - end) / decay)
        error_rate[mask] += 0.2
    elif f["type"] == "node_crash":
        mask = (t >= start) & (t <= end)
        latency[mask] += 250
        error_rate[mask] += 1.0
    elif f["type"] == "network_partition":
        mask = (t >= start) & (t <= end)
        latency[mask] += 300
        error_rate[mask] += 1.5

    df = pd.DataFrame({
        "ts": iso(ts0, t),
        "t_s": t.astype(int),
        "latency_ms": latency,
        "error_rate_pct": error_rate
    })
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

if __name__ == "__main__":
    app()