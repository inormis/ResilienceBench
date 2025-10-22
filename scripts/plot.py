#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml, pandas as pd, matplotlib.pyplot as plt


def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", "-s", type=Path, required=True)
    ap.add_argument("--data", "-d", type=Path, required=True)
    ap.add_argument("--out", "-o", type=Path, required=True)
    args = ap.parse_args()

    sc = load_yaml(args.scenario)
    df = pd.read_csv(args.data, parse_dates=["ts"])

    fig, ax = plt.subplots(figsize=(10, 4))
    if "latency_ms" in df.columns:
        ax.plot(df["ts"], df["latency_ms"], label="latency_ms")
    if "throughput_rps" in df.columns:
        ax.plot(df["ts"], df["throughput_rps"], label="throughput_rps")
    ax.set_xlabel("time");
    ax.legend(loc="best")
    g0, g1 = sc["ground_truth"]["positive_interval_s"]
    t = df["ts"]
    ax.axvspan(t.iloc[g0], t.iloc[min(g1, len(t) - 1)], alpha=0.12, label="fault")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.out, dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
