# Artifact Evaluation

This document follows artifact evaluation conventions (USENIX, ACM) for reproducing ResilienceBench results.

## Overview

ResilienceBench is an open benchmark for modeling and evaluating rare failures in critical infrastructure software systems. This artifact includes scenario definitions, synthetic data generators, baseline detectors, an evaluator, and a report generator.

## Requirements

- Python 3.11
- `make`
- ~5 minutes for a full reproduction run
- No network access required

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
make install
```

## Full Reproduction

Run the complete artifact evaluation pipeline:

```bash
make ae
```

This executes: YAML validation, JSON schema validation, synthetic data generation, baseline detection, evaluation, and HTML report generation.

## Expected Outputs

After `make ae` completes:

| File | Description |
|------|-------------|
| `eval/samples/latency_spike.csv` | Generated synthetic trace |
| `eval/samples/latency_spike_pred.csv` | Baseline detector predictions |
| `eval/reports/latency_spike_report.csv` | Evaluation metrics (precision, recall, F1, p99, SLO) |
| `eval/reports/index.html` | Combined HTML report |

## Claims Supported

| Claim | Evidence |
|-------|----------|
| Reproducible scenario execution | Deterministic output from fixed seed (`make ae` produces identical results across runs) |
| SLO-aware evaluation | `SLO_pass` column in report CSV |
| Tail latency measurement | `p99_latency_ms` and `p99_9_latency_ms` in report |
| Detection quality metrics | Precision, recall, F1 against ground truth |
| Standardized scenario format | YAML files validated against JSON Schema (`make schema`) |

## Manual Verification

To verify determinism, run `make ae` twice and compare outputs:

```bash
make ae
cp eval/reports/latency_spike_report.csv /tmp/run1.csv
make ae
diff /tmp/run1.csv eval/reports/latency_spike_report.csv
```

The diff should produce no output (identical files).
