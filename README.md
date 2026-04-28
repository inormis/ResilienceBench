# ResilienceBench

[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://inormis.github.io/ResilienceBench/)
![version](https://img.shields.io/badge/version-v1.0.0-blue)
[![CI](https://img.shields.io/github/actions/workflow/status/inormis/ResilienceBench/ci.yml?branch=main)](#)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](#)

> **Open benchmark for rare failures in critical infrastructures.**  
> Standardized scenarios (YAML), reproducible data generation, baseline detectors, SLO-aware evaluation, HTML reports,
> and interop stubs for chaos tools.

---

## Why it matters

Critical infrastructure fails in subtle, low-frequency ways (partitions, silent corruption, GC slowdowns). *
*ResilienceBench** provides a **protocol + tooling** to create, run, and compare such scenarios reproducibly. It helps
researchers and engineers measure tail-latency behavior, error budgets, and detection quality across systems and
mitigations.

---

## Features

- **Spec-first**: scenario & system profile in YAML (+ JSON Schemas for v1.0 freeze)
- **Generator**: synthetic traces seeded for reproducibility
- **Evaluator**: p99/p99.9, error budget, precision/recall/F1 vs. ground truth
- **Baselines**: threshold, rolling z-score, EWMA, CUSUM (optional IsolationForest)
- **Statistical rigor**: bootstrap confidence intervals for all evaluation metrics
- **Reports**: CSV + combined HTML (with per-scenario plots)
- **Interop**: JSON export + dry-run generators for Litmus, Gremlin, AWS FIS
- **CLI**: `resbench` for end-to-end runs
- **Quality gates**: lint (ruff), security scanning (bandit), results validation
- **Docs**: MkDocs site with standards mapping, benchmark card, compliance posture

---

## Table of contents

- [Quickstart](#quickstart)
- [Usage](#usage)
- [Scenarios & profiles](#scenarios--profiles)
- [Reports & artifacts](#reports--artifacts)
- [Interop](#interop)
- [Quality & compliance](#quality--compliance)
- [Docs](#docs)
- [How to cite](#how-to-cite)
- [Contributing](#contributing)
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
```

### Run the full pipeline

```bash
make ae
```

This runs YAML validation, schema checks, synthetic data generation, baseline detection, evaluation, and HTML report
generation. See [ARTIFACTS.md](ARTIFACTS.md) for full artifact evaluation instructions.

---

## Usage

### Single scenario

```bash
python3 scripts/generate.py --scenario benchmarks/scenarios/latency_spike.yaml --out eval/samples/latency_spike.csv
python3 scripts/baselines/threshold.py --inp eval/samples/latency_spike.csv --out eval/samples/latency_spike_pred.csv --scenario benchmarks/scenarios/latency_spike.yaml
python3 scripts/evaluate.py --scenario benchmarks/scenarios/latency_spike.yaml --data eval/samples/latency_spike.csv --pred eval/samples/latency_spike_pred.csv --out eval/reports/latency_spike_report.csv
```

### All scenarios via Make

```bash
make run-phase3        # latency_spike
make run-slowdown      # slowdown_gc_pause
make run-netpart-large # network_partition_large
make run-corruption    # corruption_silent
```

### Confidence intervals

```bash
python3 scripts/confidence.py --scenario benchmarks/scenarios/latency_spike.yaml --data eval/samples/latency_spike.csv --pred eval/samples/latency_spike_pred.csv --out eval/reports/latency_spike_ci.csv
```

### HTML report

```bash
make report
```

---

## Scenarios & profiles

### Scenarios (6)

| Scenario                  | Failure Type      | Duration | Domain               |
|---------------------------|-------------------|----------|----------------------|
| `latency_spike`           | latency_spike     | 900s     | Cloud checkout       |
| `slowdown_gc_pause`       | slowdown          | 900s     | K8s service mesh     |
| `network_partition_large` | network_partition | 1800s    | K8s mesh             |
| `corruption_silent`       | corruption        | 900s     | Cloud                |
| `node_crash`              | node_crash        | 1200s    | Cloud DB             |
| `transport_signal_loss`   | latency_spike     | 1800s    | Transportation SCADA |

### System profiles (4)

| Profile           | Nodes | Domain                     |
|-------------------|-------|----------------------------|
| `default`         | 3     | Generic distributed system |
| `cloud_small`     | 3     | Cloud microservices        |
| `k8s_mesh`        | 4     | Kubernetes service mesh    |
| `transport_scada` | 3     | Transportation SCADA       |

### Baselines (5)

| Baseline        | Method                                | Script                           |
|-----------------|---------------------------------------|----------------------------------|
| Threshold       | Static threshold from SLO             | `scripts/baselines/threshold.py` |
| Z-score         | Rolling z-score                       | `scripts/baselines/zscore.py`    |
| EWMA            | Exponentially weighted moving average | `scripts/baselines/ewma.py`      |
| CUSUM           | Cumulative sum control chart          | `scripts/baselines/cusum.py`     |
| IsolationForest | Scikit-learn IsolationForest          | `scripts/baselines/isoforest.py` |

---

## Reports & artifacts

- **CSV reports**: per-scenario metrics (precision, recall, F1, p99, SLO pass/fail)
- **HTML report**: combined dashboard at `eval/reports/index.html`
- **Confidence intervals**: bootstrap CIs via `scripts/confidence.py`
- **Artifact packaging**: `make artifact VERSION=1.0.0` creates a distributable tarball

See [ARTIFACTS.md](ARTIFACTS.md) for the full artifact evaluation checklist.

---

## Interop

Dry-run generators for chaos engineering tools:

```bash
make dry-litmus    # Litmus ChaosEngine YAML
make dry-gremlin   # Gremlin attack JSON
make dry-fis       # AWS FIS experiment template
make export-json   # NDJSON export of reports
```

---

## Quality & compliance

```bash
make lint              # ruff static analysis
make security-scan     # bandit security scanning
make validate          # YAML structure validation
make schema            # JSON Schema validation
make validate-results  # post-run report sanity checks
```

Standards and policy mapping: [docs/standards_mapping.md](docs/standards_mapping.md)  
Compliance posture: [docs/compliance.md](docs/compliance.md)  
Benchmark card: [docs/benchmark_card.md](docs/benchmark_card.md)  
Limitations: [docs/limitations.md](docs/limitations.md)

---

## Docs

Build and serve the MkDocs site locally:

```bash
make docs-build
make docs-serve
```

Key documentation pages:

- [Protocol](docs/protocol.md) — benchmark protocol specification
- [Metrics](docs/metric.md) — metric definitions and reporting rules
- [Standards Mapping](docs/standards_mapping.md) — NIST CSF, ISO 22301, SRE alignment
- [Benchmark Card](docs/benchmark_card.md) — intended use, scope, governance
- [Limitations](docs/limitations.md) — scope boundaries and assumptions
- [Compliance](docs/compliance.md) — NIST CSF, ISO 27001, SOC 2 mapping
- [Results Gallery](docs/results_gallery.md) — evaluation results across all scenarios
- [Executive Brief](docs/executive_brief.md) — one-page summary
- [Impact](docs/impact.md) — adoption metrics and community roadmap
- [Compatibility](docs/compatibility.md) — comparison with other tools

---

## How to cite

```bibtex
@software{resiliencebench,
  title   = {ResilienceBench: Open Benchmark for Rare Failures in Critical Infrastructure},
  url     = {https://github.com/inormis/ResilienceBench},
  version = {1.0.0}
}
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding scenarios, baselines, and submitting PRs.

---

## License

[Apache 2.0](LICENSE)
