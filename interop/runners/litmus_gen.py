#!/usr/bin/env python3
from __future__ import annotations
import argparse, yaml
from pathlib import Path

MAP = {
    "node_crash": "pod-delete",
    "latency_spike": "pod-network-latency",
    "network_partition": "pod-network-loss",
    "slowdown": "pod-cpu-hog",
    "corruption": "pod-io-stress"
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--scenario", type=Path, required=True)
    ap.add_argument("-o", "--outdir", type=Path, default=Path("interop/out"))
    args = ap.parse_args()

    sc = yaml.safe_load(args.scenario.read_text(encoding="utf-8"))
    exp = MAP.get(sc["failure"]["type"], "pod-delete")
    dur = int(sc["failure"]["duration_s"])
    name = f"rb-{sc['id']}"
    doc = {
        "apiVersion": "litmuschaos.io/v1alpha1",
        "kind": "ChaosEngine",
        "metadata": {"name": name},
        "spec": {
            "engineState": "stop",
            "annotationCheck": "false",
            "chaosServiceAccount": "litmus-admin",
            "experiments": [
                {"name": exp, "spec": {"components": {"env": [
                    {"name": "TOTAL_CHAOS_DURATION", "value": str(dur)}
                ]}}}
            ]
        }
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    out = args.outdir / f"litmus_{sc['id']}.yaml"
    out.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
