# Compliance & Security Posture

This document maps ResilienceBench practices to recognized security and resilience frameworks. This is an alignment reference, not a certification claim.

## NIST Cybersecurity Framework (CSF)

| CSF Function | Practice | ResilienceBench Implementation |
|-------------|----------|-------------------------------|
| **Identify** (ID) | Asset and risk identification | Scenario YAML defines failure types, affected components, and impact thresholds |
| **Protect** (PR) | Protective technology | SLO thresholds define acceptable degradation limits |
| **Detect** (DE) | Detection processes | Baseline detectors with measured precision/recall/F1 |
| **Respond** (RS) | Response planning | Interop stubs for Litmus, Gremlin, AWS FIS enable response testing |
| **Recover** (RC) | Recovery planning | MTBF/MTTR metrics quantify recovery characteristics |

## ISO 27001 Relevance

| Control Area | Relevance |
|-------------|-----------|
| A.17 Information Security Aspects of BCM | Scenario-driven continuity impact modeling |
| A.12 Operations Security | Deterministic, reproducible evaluation pipeline |
| A.16 Incident Management | Detection metrics measure incident identification quality |

## SOC 2 Trust Principles

| Principle | Alignment |
|-----------|-----------|
| Availability | Availability proxy (A), MTBF, MTTR |
| Processing Integrity | Deterministic generation with fixed seeds, schema-validated inputs |

## Code Quality

- Static analysis: `make lint` (ruff)
- Security scanning: `make security-scan` (bandit)
- Schema validation: `make schema` (jsonschema)
- CI enforcement: all checks run on every push and pull request
