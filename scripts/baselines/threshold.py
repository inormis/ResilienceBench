#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import typer, yaml, pandas as pd

app = typer.Typer(add_completion=False)

def load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

@app.command()
def main(inp: Path, out: Path, metric: str = "latency_ms", threshold: float = -1.0, scenario: Path | None = None):
    if threshold <= 0 and scenario:
        sc = load_yaml(scenario)
        slo = sc.get("evaluation", {}).get("slo", {})
        key = f"{metric}_p99"
        threshold = float(slo.get(key, 0)) or float(slo.get(metric, 0)) or 250.0
    elif threshold <= 0:
        threshold = 250.0

    df = pd.read_csv(inp, parse_dates=["ts"])
    df["pred"] = (df[metric] > threshold).astype(int)
    out.parent.mkdir(parents=True, exist_ok=True)
    df[["ts", "t_s", "pred"]].to_csv(out, index=False)

if __name__ == "__main__":
    app()