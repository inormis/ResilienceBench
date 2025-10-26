# ResilienceBench

[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://<org-or-user>.github.io/ResilienceBench/)
![version](https://img.shields.io/badge/version-v1.0.0-blue)
[![CI](https://img.shields.io/github/actions/workflow/status/<org-or-user>/ResilienceBench/ci.yml?branch=main)](#)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](#)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.XXXXXXX-orange)](#)

> **Open benchmark for rare failures in critical infrastructures.**  
> Standardized scenarios (YAML), reproducible data generation, baseline detectors, SLO-aware evaluation, HTML reports, and interop stubs for chaos tools.

---

## Why it matters

Critical infrastructure fails in subtle, low-frequency ways (partitions, silent corruption, GC slowdowns). **ResilienceBench** provides a **protocol + tooling** to create, run, and compare such scenarios reproducibly. It helps researchers and engineers measure tail-latency behavior, error budgets, and detection quality across systems and mitigations.

---

## Features

- 📄 **Spec-first**: scenario & system profile in YAML (+ JSON Schemas for v1.0 freeze)
- 🧪 **Generator**: synthetic traces seeded for reproducibility
- 📈 **Evaluator**: p99/p99.9, error budget, precision/recall/F1 vs. ground truth
- 🧰 **Baselines**: threshold, rolling z-score (optional IsolationForest)
- 🖼️ **Reports**: CSV + combined HTML (with per-scenario plots)
- 🔌 **Interop**: JSON export + dry-run generators for Litmus, Gremlin, AWS FIS
- 🧩 **CLI**: `resbench` for end-to-end runs
- 📚 **Docs**: MkDocs site; templates and governance for contributions

---

## Table of contents

- [Quickstart](#quickstart)
- [Usage](#usage)
- [Scenarios & profiles](#scenarios--profiles)
- [Reports & artifacts](#reports--artifacts)
- [Interop (Phase 8)](#interop-phase-8)
- [Packaging & release](#packaging--release)
- [Docs](#docs)
- [How to cite](#how-to-cite)
- [Contributing & governance](#contributing--governance)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Quickstart

### Requirements
- Python **3.11**
- `make`
- (optional) Docker, GitHub account for CI/Pages

### Install
```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
make install