#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, yaml
from pathlib import Path

MAP = {
    "node_crash": {"attackType": "shutdown"},
    "latency_spike": {"attackType": "latency"},
    "network_partition": {"attackType": "blackhole"},
    "slowdown": {"attackType": "cpu"},
    "corruption": {"attackType": "io"}
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--scenario", type=Path, required=True)
    ap.add_argument("-o", "--outdir", type=Path, default=Path("interop/out"))
    args = ap.parse_args()

    sc = yaml.safe_load(args.scenario.read_text(encoding="utf-8"))
    spec = {
        "tool": "gremlin",
        "scenario_id": sc["id"],
        "failure": sc["failure"],
        "attack": MAP.get(sc["failure"]["type"], {"attackType": "cpu"})
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    out = args.outdir / f"gremlin_{sc['id']}.json"
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
