#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, yaml
from pathlib import Path

MAP = {
    "node_crash": {"actionId": "aws:ec2:stop-instances"},
    "network_partition": {"actionId": "aws:fis:disrupt-network-connections"},
    "latency_spike": {"actionId": "aws:fis:introduce-latency"},
    "slowdown": {"actionId": "aws:fis:cpu-stress"},
    "corruption": {"actionId": "aws:fis:io-stress"}
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--scenario", type=Path, required=True)
    ap.add_argument("-o", "--outdir", type=Path, default=Path("interop/out"))
    args = ap.parse_args()

    sc = yaml.safe_load(args.scenario.read_text(encoding="utf-8"))
    action = MAP.get(sc["failure"]["type"], {"actionId": "aws:fis:cpu-stress"})
    tpl = {
        "description": f"RB {sc['id']}",
        "targets": {},
        "actions": {"attack": {"actionId": action["actionId"], "parameters": {}}},
        "stopConditions": []
    }
    args.outdir.mkdir(parents=True, exist_ok=True)
    out = args.outdir / f"awsfis_{sc['id']}.json"
    out.write_text(json.dumps(tpl, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
