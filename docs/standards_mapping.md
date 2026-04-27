# Standards & Policy Mapping

This document maps ResilienceBench concepts to established resilience, continuity, and reliability standards.

## Mapping Table

| Standard               | Section                                | ResilienceBench Mapping                               | Notes                                                                       |
|------------------------|----------------------------------------|-------------------------------------------------------|-----------------------------------------------------------------------------|
| NIST CSF v1.1          | ID.RA (Risk Assessment)                | Scenario modeling with defined failure types and SLOs | Each YAML scenario encodes a risk scenario with measurable thresholds       |
| NIST CSF v1.1          | DE.CM (Security Continuous Monitoring) | Baseline detectors (threshold, z-score, EWMA, CUSUM)  | Detection metrics (precision, recall, F1) quantify monitoring effectiveness |
| NIST CSF v1.1          | RC.RP (Recovery Planning)              | Availability metrics (MTBF, MTTR, A)                  | Recovery time is encoded in scenario evaluation blocks                      |
| NIST SP 800-160 Vol. 2 | Anticipate                             | Synthetic fault injection with ground truth           | Scenarios define expected failure windows for anticipation testing          |
| NIST SP 800-160 Vol. 2 | Withstand                              | SLO pass/fail evaluation under fault conditions       | SLO thresholds measure whether the system withstands degradation            |
| NIST SP 800-160 Vol. 2 | Recover                                | MTTR and availability proxy                           | Quantifies recovery characteristics post-fault                              |
| ISO 22301:2019         | 8.2 (Business Impact Analysis)         | Scenario-driven impact modeling                       | Each scenario quantifies impact via tail latency, error rate, SLO breach    |
| ISO 22301:2019         | 8.3 (Business Continuity Strategy)     | System profiles with defined node roles               | Profiles model system topology for continuity assessment                    |
| ISO 22301:2019         | 9.1 (Monitoring and Evaluation)        | Reproducible evaluation pipeline                      | Deterministic seed + standardized metrics enable consistent monitoring      |
| SRE (Google)           | Error Budgets                          | SLO evaluation with error_rate_pct thresholds         | Direct mapping to SRE error budget methodology                              |
| SRE (Google)           | SLIs/SLOs                              | evaluation.slo in scenario YAML                       | Latency p99 and error rate SLOs are first-class scenario fields             |
| SRE (Google)           | Incident Detection                     | Detection metrics with window tolerance               | Precision/recall evaluation mirrors incident detection quality measurement  |

## Scope

This mapping documents conceptual alignment between ResilienceBench and recognized standards. It does not constitute
certification or compliance with any standard.

## References

- NIST Cybersecurity Framework v1.1 (2018)
- NIST SP 800-160 Vol. 2 Rev. 1: Developing Cyber-Resilient Systems (2021)
- ISO 22301:2019 Security and Resilience — Business Continuity Management Systems
- Beyer et al., Site Reliability Engineering (O'Reilly, 2016)
