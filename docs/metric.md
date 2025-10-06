# Metrics (v0.1)

This document defines **standard metrics** and **reporting rules** for ResilienceBench.  
All results must reference these definitions (do not redefine per scenario).

## 1) Availability & Reliability

**Availability**  
\[
A = \frac{MTBF}{MTBF + MTTR}
\]
- Report `MTBF` and `MTTR` in **seconds**.
- If unavailable (e.g., synthetic runs without repair cycles), omit `availability`.

**Reliability (optional)**  
- Survival function \(R(t)\) and hazard \( \lambda(t) \) may be reported for long-running traces.
- If used, document the estimation method (e.g., Kaplan–Meier for \(R(t)\)).

## 2) Tail Latency & Error Rate

**Tail latency**  
- Report **p99** and **p99.9** for targets listed in the scenario (`evaluation.tails.p99_targets`).
- Quantile method: **nearest-rank** (or equivalent deterministic algorithm); state the method if different.
- Units must be explicit (e.g., `latency_ms`).

**Error rate**  
- Percentage of failing requests over the reporting window.
- Name metrics explicitly (e.g., `error_rate_pct`).

## 3) SLO & Error Budget

- Scenarios define SLO thresholds under `evaluation.slo` (e.g., `latency_ms_p99: 250`, `error_rate_pct: 1.0`).
- Report:
  - `SLO_pass` (bool) for each SLO or an overall flag when all SLOs pass.
  - **Error budget** as the remaining allowance vs. the SLO (e.g., `budget_remaining_pct`).

## 4) Failure Detection Metrics

Evaluate detection against `ground_truth.positive_interval_s = [start, end]`.

- Windowing: a detected interval is a **true positive** if it intersects the ground-truth interval within  
  ±`evaluation.detection.window_tolerance_s`.
- Report **precision**, **recall**, **F1**:
  \[
  \text{precision}=\frac{TP}{TP+FP},\quad
  \text{recall}   =\frac{TP}{TP+FN},\quad
  F1=2\cdot\frac{\text{precision}\cdot\text{recall}}{\text{precision}+\text{recall}}
  \]
- If no detector is used in the run, omit this block.

## 5) Sampling & Windows

- Default sampling (if not specified) comes from `system_profile.sampling_defaults_hz`.
- Each scenario declares `dataset.duration_s` and `warmup_s`.
- **Exclude warmup** from tail-latency and error-rate calculations unless the scenario explicitly states otherwise.

## 6) Reporting Format (minimal table)

For each scenario/run, emit a row with:

| Field | Description |
|---|---|
| `scenario_id` | YAML `id` |
| `seed` | From `reproducibility.seed` |
| `A` | Availability (0–1), or `NA` |
| `MTBF_s`, `MTTR_s` | Seconds, or `NA` |
| `p99`, `p99_9` | Tail latency for declared targets (add suffix `_target` if multiple) |
| `error_rate_pct` | % over reporting window |
| `SLO_pass` | `true/false` (all SLOs) and/or per-SLO flags |
| `precision`, `recall`, `f1` | If detection evaluated; else `NA` |

> If multiple p99 targets exist, add columns like `p99_latency_ms`, `p99_9_latency_ms`.

## 7) Units & Naming

- Include units in metric names (e.g., `latency_ms`, `throughput_rps`).
- Use lowercase snake_case for columns.
- Be explicit about **time base** (UTC) and **window** (start/end timestamps or seconds since start).

## 8) Statistical Notes (recommended)

- For reported scalars (e.g., p99), provide **N** (sample size).
- If you repeat runs with different seeds, report **mean ± std** (and N).
- Confidence intervals (optional): 95% bootstrap for tail latencies; Wilson score for proportions.

## 9) Reproducibility

- Always record: `scenario_version` (if present), tool version, commit hash, environment summary (OS, container tag).

## 10) Non-goals (v0.1)

- No mandated estimator for \(R(t)\)/\( \lambda(t) \); treat as optional advanced metrics.
- No requirement to normalize metrics across domains; scenarios must define SLOs relevant to their domain.

---

### Example (single-row CSV)

