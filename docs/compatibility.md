# Compatibility Matrix

| Component / Metric                | Chaos Monkey | Gremlin | AWS FIS | Litmus | ResilienceBench |
|-----------------------------------|--------------|---------|---------|--------|-----------------|
| Node crash injection              | ✅ basic      | ✅       | ✅       | ✅      | ✅ YAML scenario |
| Network partition                 | ❌            | ✅       | ✅       | ✅      | ✅ reproducible  |
| Latency spike / p99 evaluation    | ❌            | ❌       | ✅       | ✅      | ✅ required      |
| Error budget / SLO validation     | ❌            | ✅       | ✅       | ❌      | ✅ required      |
| MTBF / MTTR calculation           | ❌            | ❌       | ❌       | ❌      | ✅ required      |
| Standardized reproducibility seed | ❌            | ❌       | ❌       | ❌      | ✅ built-in      |