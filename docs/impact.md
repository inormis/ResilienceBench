# Impact & Adoption

## Adoption Metrics

Adoption data is tracked via GitHub Insights:

- **Stars and forks**: visible on the repository page
- **Clones and views**: available under Insights > Traffic (maintainers only)
- **PyPI downloads**: not yet published; planned for a future release

## Citations

If you use ResilienceBench in your research, please cite:

```bibtex
@software{resiliencebench,
  title  = {ResilienceBench: Open Benchmark for Rare Failures in Critical Infrastructure},
  url    = {https://github.com/inormis/ResilienceBench},
  version = {1.0.0}
}
```

See also: `CITATION.cff` in the repository root.

## Downstream Use Cases

- **Researchers**: evaluating and comparing anomaly detection methods on standardized failure scenarios
- **SRE teams**: validating resilience practices against reproducible benchmarks
- **Educators**: teaching fault tolerance, SLO management, and reliability engineering with practical examples
- **Tool developers**: testing chaos engineering integrations via interop stubs

## Community Roadmap

- Additional failure scenarios (cascading failures, multi-region partitions)
- Heavier baseline detectors under `extras/`
- PyPI package publication
- Integration with additional chaos engineering platforms
