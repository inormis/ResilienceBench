# Limitations & Scope Boundaries

## Synthetic Data Only

All data in ResilienceBench v1.0 is synthetically generated. No real production traces are included. Synthetic generation uses deterministic seeds for reproducibility, but generated distributions are simplified models of real-world behavior.

## Failure Types Not Covered

The following failure modes are out of scope for v1.0:

- **Byzantine faults** — arbitrary or malicious node behavior
- **Cascading failures** — multi-hop propagation across dependent services
- **Multi-region failures** — geographically distributed partition scenarios
- **Gradual degradation** — slow resource exhaustion (memory leaks, disk fill)
- **Configuration errors** — misconfigurations leading to subtle failures

## Scalability

- Data generation and evaluation run in-memory on a single machine
- Scenarios model small topologies (3–4 nodes)
- No distributed execution or large-scale simulation support

## Baseline Assumptions

- All included baselines are statistical (threshold, z-score, EWMA, CUSUM, IsolationForest)
- No deep learning or model-based detectors are included
- Baselines are intended as reference points, not production-grade detectors

## Scope Boundary

ResilienceBench is a benchmark protocol and toolset. It is not:

- A production monitoring system
- A chaos engineering platform (interop stubs are dry-run only)
- A certification or compliance tool
- A replacement for real-world testing
