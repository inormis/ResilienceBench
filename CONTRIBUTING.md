# Contributing to ResilienceBench

## Adding a Scenario

1. Copy `benchmarks/scenarios/_template.yaml`
2. Fill in all required fields (see `schemas/scenario_v1.json` for the schema)
3. Set `version: 1.0.0`
4. Validate: `make schema`
5. Run the scenario through the pipeline:
   ```bash
   python3 scripts/generate.py --scenario benchmarks/scenarios/your_scenario.yaml --out eval/samples/your_scenario.csv
   python3 scripts/baselines/threshold.py --inp eval/samples/your_scenario.csv --out eval/samples/your_scenario_pred.csv --scenario benchmarks/scenarios/your_scenario.yaml
   python3 scripts/evaluate.py --scenario benchmarks/scenarios/your_scenario.yaml --data eval/samples/your_scenario.csv --pred eval/samples/your_scenario_pred.csv --out eval/reports/your_scenario_report.csv
   ```

## Adding a Baseline Detector

1. Create a new script in `scripts/baselines/`
2. Follow the CLI interface pattern:
   - Required args: `--inp` (input CSV), `--out` (output CSV), `--metric` (column name)
   - Output CSV must have columns: `ts`, `t_s`, `pred` (0 or 1)
3. Test with an existing scenario to verify compatibility with `scripts/evaluate.py`

## Code Style

- Python 3.11
- Run `make lint` before submitting
- Follow existing patterns in `scripts/`
- Use `argparse`, `pathlib.Path`, standard library where possible

## Pull Requests

- One logical change per PR
- Include the validation commands you ran in the PR description
- Use conventional commit messages: `feat(...)`, `docs(...)`, `fix(...)`, `test(...)`

## Reporting Issues

Use the GitHub issue templates for bug reports and scenario requests.
