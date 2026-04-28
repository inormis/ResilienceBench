# Executive Brief

## Problem

Critical infrastructure software systems experience rare but high-impact failures — network partitions, latency spikes, silent corruption, node crashes, and service slowdowns. These events are difficult to reproduce, benchmark, and compare across detection methods. Existing chaos engineering tools focus on injection, not on standardized evaluation.

## Approach

ResilienceBench provides a protocol and toolset for reproducible failure benchmarking:

- **Scenario definitions** in versioned YAML with JSON Schema validation
- **Deterministic synthetic generation** from fixed seeds
- **SLO-aware evaluation** measuring tail latency, error rates, and availability
- **Detection quality metrics** (precision, recall, F1) against ground truth
- **Interoperability** with Litmus, Gremlin, and AWS FIS via dry-run generators

## Key Results

- 6 failure scenarios covering the most common critical infrastructure failure modes
- 4 system profiles (generic, cloud, Kubernetes mesh, transportation SCADA)
- 5 baseline detectors (threshold, z-score, EWMA, CUSUM, IsolationForest)
- Fully reproducible pipeline: `make ae` runs end-to-end in under 5 minutes
- JSON Schema-validated inputs, standardized CSV/HTML outputs

## Impact

ResilienceBench serves researchers evaluating detection methods, SRE teams validating resilience practices, and educators teaching fault tolerance concepts. The standardized protocol enables fair comparison across systems and mitigations, supporting evidence-based resilience engineering for critical infrastructure.
