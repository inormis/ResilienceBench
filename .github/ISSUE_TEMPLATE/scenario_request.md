---
name: Scenario request
about: Propose a new rare-failure scenario
labels: enhancement, scenario
---

**Scenario id/title**
…

**Failure type**
(network_partition | node_crash | latency_spike | corruption | slowdown)

**Parameters**

- start/duration/affected nodes/…
- required SLO keys:
    - latency_spike/slowdown → `latency_ms_p99`
    - node_crash/network_partition/corruption → `error_rate_pct` (+ `latency_ms_p99` for network_partition)

**Motivation**
…