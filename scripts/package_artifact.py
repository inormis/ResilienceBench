#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, tarfile, hashlib, subprocess, sys, os, platform
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def git_commit() -> str:
    try:
        return subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT).decode().strip()
    except Exception:
        return "unknown"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--outdir", default="dist")
    args = ap.parse_args()

    outdir = (ROOT / args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    name = f"resiliencebench-{args.version}-artifact.tar.gz"
    out = outdir / name

    include = [
        "benchmarks", "scripts", "docs", "mkdocs.yml",
        "CITATION.cff", "LICENSE", "README.md", "requirements.txt",
        "eval/reports"
    ]
    manifest = {
        "name": "ResilienceBench",
        "version": args.version,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "git_commit": git_commit(),
        "files": []
    }

    with tarfile.open(out, "w:gz") as tar:
        for item in include:
            p = ROOT / item
            if not p.exists(): continue
            if p.is_dir():
                for sub in p.rglob("*"):
                    if sub.is_file():
                        tar.add(sub, arcname=sub.relative_to(ROOT))
                        manifest["files"].append({"path": str(sub), "sha256": sha256(sub)})
            else:
                tar.add(p, arcname=p.relative_to(ROOT))
                manifest["files"].append({"path": str(p), "sha256": sha256(p)})

        # write manifest.json into archive
        tmp = ROOT / ".artifact_manifest.json"
        tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        tar.add(tmp, arcname="artifact_manifest.json")
        tmp.unlink(missing_ok=True)

    print(out)

if __name__ == "__main__":
    main()