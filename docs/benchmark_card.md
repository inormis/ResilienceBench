# Benchmark Card

## Name & Version

**ResilienceBench v1.0**

## Intended Use

- Research: evaluating and comparing failure detection methods on standardized scenarios
- Education: teaching resilience engineering concepts with reproducible examples
- Engineering: validating SRE practices against defined SLO thresholds

## Failure Types Covered

| Type | Description |
|------|-------------|
| `latency_spike` | Transient tail-latency degradation |
| `node_crash` | Complete node failure with throughput loss |
| `network_partition` | Network segmentation with latency and error increase |
| `slowdown` | Sustained performance degradation (e.g., GC pressure) |
| `corruption` | Silent data corruption with elevated error rates |

## Metrics

See [Metrics](metrics.md) for full definitions. Core metrics: availability (A), tail latency (p99, p99.9), error rate, SLO pass/fail, precision, recall, F1.

## System Profiles

| Profile | Nodes | Domain |
|---------|-------|--------|
| `default` | 3 (leader + 2 followers) | Generic distributed system |
| `cloud_small` | 3 | Cloud microservices |
| `k8s_mesh` | 4 | Kubernetes service mesh |
| `transport_scada` | 3 | Transportation SCADA |

## Known Limitations

See [Limitations](limitations.md) for a detailed scope boundary analysis.

## Maintenance

- Schema versioning follows semver (`1.0.x`)
- Scenarios are validated against JSON Schema on every CI run
- Contributions follow the process described in `CONTRIBUTING.md`

## Contact

Issues and contributions via [GitHub](https://github.com/inormis/ResilienceBench).
