#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*cmd: str):
    r = subprocess.run(list(cmd), cwd=ROOT)
    sys.exit(r.returncode) if r.returncode else None


def main():
    ap = argparse.ArgumentParser(prog="resbench")
    sp = ap.add_subparsers(dest="cmd", required=True)

    g = sp.add_parser("gen")
    g.add_argument("--scenario", "-s", required=True)
    g.add_argument("--out", "-o", required=True)

    b = sp.add_parser("baseline")
    b.add_argument("--algo", choices=["threshold", "zscore"], default="threshold")
    b.add_argument("--inp", "-i", required=True)
    b.add_argument("--out", "-o", required=True)
    b.add_argument("--scenario", "-s")
    b.add_argument("--metric", "-m", default="latency_ms")

    e = sp.add_parser("eval")
    e.add_argument("--scenario", "-s", required=True)
    e.add_argument("--data", "-d", required=True)
    e.add_argument("--pred", "-p")
    e.add_argument("--out", "-o")

    r = sp.add_parser("report")
    r.add_argument("--reports", "-r", default="eval/reports")
    r.add_argument("--out", "-o", default="eval/reports/index.html")
    r.add_argument("--title", "-t", default="ResilienceBench Report")

    p = sp.add_parser("plot")
    p.add_argument("--scenario", "-s", required=True)
    p.add_argument("--data", "-d", required=True)
    p.add_argument("--out", "-o", required=True)

    a = sp.add_parser("all")
    a.add_argument("--scenario", "-s", required=True)
    a.add_argument("--prefix", default="eval/samples/sample")

    args = ap.parse_args()

    if args.cmd == "gen":
        run(sys.executable, "scripts/generate.py", "--scenario", args.scenario, "--out", args.out)
    elif args.cmd == "baseline":
        script = "scripts/baselines/threshold.py" if args.algo == "threshold" else "scripts/baselines/zscore.py"
        cmd = [sys.executable, script, "--inp", args.inp, "--out", args.out, "--metric", args.metric]
        if args.scenario: cmd += ["--scenario", args.scenario]
        run(*cmd)
    elif args.cmd == "eval":
        cmd = [sys.executable, "scripts/evaluate.py", "--scenario", args.scenario, "--data", args.data]
        if args.pred: cmd += ["--pred", args.pred]
        if args.out: cmd += ["--out", args.out]
        run(*cmd)
    elif args.cmd == "report":
        run(sys.executable, "scripts/report.py", "--reports", args.reports, "--out", args.out, "--title", args.title)
    elif args.cmd == "plot":
        run(sys.executable, "scripts/plot.py", "--scenario", args.scenario, "--data", args.data, "--out", args.out)
    elif args.cmd == "all":
        data = f"{args.prefix}.csv"
        pred = f"{args.prefix}_pred.csv"
        rep = f"eval/reports/{Path(args.scenario).stem}_report.csv"
        img = f"eval/reports/{Path(args.scenario).stem}.png"
        os.makedirs(Path(data).parent, exist_ok=True)
        run(sys.executable, "scripts/generate.py", "--scenario", args.scenario, "--out", data)
        run(sys.executable, "scripts/baselines/threshold.py", "--inp", data, "--out", pred, "--scenario", args.scenario)
        run(sys.executable, "scripts/evaluate.py", "--scenario", args.scenario, "--data", data, "--pred", pred, "--out",
            rep)
        run(sys.executable, "scripts/plot.py", "--scenario", args.scenario, "--data", data, "--out", img)


if __name__ == "__main__":
    main()
