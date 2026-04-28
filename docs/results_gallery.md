# Results Gallery

Summary of evaluation results across all ResilienceBench v1.0 scenarios. All values are reproducible from committed scenario files using deterministic seeds.

## Results Table

| Scenario | Failure Type | Duration (s) | SLO Target | Baseline | F1 | p99 Latency (ms) | SLO Pass |
|----------|-------------|-------------|------------|----------|-----|------------------|----------|
| latency_spike_checkout | latency_spike | 900 | p99 ≤ 250 ms | threshold | 0.9556 | 287.9 | No |
| slowdown_gc_pause | slowdown | 900 | p99 ≤ 250 ms | zscore | 0.1033 | 229.1 | Yes |
| netpart_large_mesh | network_partition | 1800 | p99 ≤ 250 ms | threshold | 0.9617 | 378.7 | No |
| corruption_silent | corruption | 900 | err ≤ 1.0% | threshold | 0.9526 | 72.6 | Yes |
| node_crash_db_primary | node_crash | 1200 | p99 ≤ 300 ms, err ≤ 1.5% | threshold | 0.9267 | 316.7 | No |
| transport_signal_loss | latency_spike | 1800 | p99 ≤ 400 ms, err ≤ 0.5% | threshold | 0.9688 | 437.9 | No |

## Regenerating Results

```bash
make run-phase3        # latency_spike
make run-slowdown      # slowdown_gc_pause
make run-netpart-large # network_partition_large
make run-corruption    # corruption_silent
```

All commands produce deterministic output for the committed seeds.
