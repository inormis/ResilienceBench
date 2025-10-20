.PHONY: install validate docker-build docker-run gen baseline eval run-phase3 report ci

SHELL := /bin/bash
PYTHON ?= python3
IMAGE  ?= resiliencebench:v0.1
DFILE  ?= Dockerfile

ROOT   := $(CURDIR)
SCEN   := $(ROOT)/benchmarks/scenarios/latency_spike.yaml
DATA   := $(ROOT)/eval/samples
REPORT := $(ROOT)/eval/reports

install:
	$(PYTHON) -m pip install -r scripts/requirements.txt

validate:
	$(PYTHON) scripts/validate.py

docker-build:
	docker build -t $(IMAGE) -f $(DFILE) .

docker-run:
	docker run --rm $(IMAGE)

gen:
	mkdir -p $(DATA)
	$(PYTHON) scripts/generate.py --scenario $(SCEN) --out $(DATA)/latency_spike.csv

baseline:
	$(PYTHON) scripts/baselines/threshold.py --inp $(DATA)/latency_spike.csv --out $(DATA)/latency_spike_pred.csv --scenario $(SCEN)

eval:
	mkdir -p $(REPORT)
	$(PYTHON) scripts/evaluate.py --scenario $(SCEN) --data $(DATA)/latency_spike.csv --pred $(DATA)/latency_spike_pred.csv --out $(REPORT)/latency_spike_report.csv

run-phase3: gen baseline eval

report:
	$(PYTHON) scripts/report.py --reports $(REPORT) --out $(REPORT)/index.html --title "ResilienceBench Report"

ci: validate run-phase3 report

.PHONY: docs-build docs-serve docs-deploy

docs-build:
	$(PYTHON) -m mkdocs build

docs-serve:
	$(PYTHON) -m mkdocs serve -a 0.0.0.0:8000

docs-deploy:
	$(PYTHON) -m mkdocs gh-deploy --force

.PHONY: run-slowdown run-netpart-large run-corruption

SLOW_SCEN := $(ROOT)/benchmarks/scenarios/slowdown_gc_pause.yaml
NETP_SCEN := $(ROOT)/benchmarks/scenarios/network_partition_large.yaml
CORR_SCEN := $(ROOT)/benchmarks/scenarios/corruption_silent.yaml

run-slowdown:
	mkdir -p $(DATA) $(REPORT)
	$(PYTHON) scripts/generate.py --scenario $(SLOW_SCEN) --out $(DATA)/slowdown.csv
	$(PYTHON) scripts/baselines/zscore.py --inp $(DATA)/slowdown.csv --out $(DATA)/slowdown_pred.csv --metric latency_ms --window 60 --k 3.0
	$(PYTHON) scripts/evaluate.py --scenario $(SLOW_SCEN) --data $(DATA)/slowdown.csv --pred $(DATA)/slowdown_pred.csv --out $(REPORT)/slowdown_report.csv

run-netpart-large:
	mkdir -p $(DATA) $(REPORT)
	$(PYTHON) scripts/generate.py --scenario $(NETP_SCEN) --out $(DATA)/netpart_large.csv
	$(PYTHON) scripts/baselines/threshold.py --inp $(DATA)/netpart_large.csv --out $(DATA)/netpart_large_pred.csv --scenario $(NETP_SCEN) --metric latency_ms
	$(PYTHON) scripts/evaluate.py --scenario $(NETP_SCEN) --data $(DATA)/netpart_large.csv --pred $(DATA)/netpart_large_pred.csv --out $(REPORT)/netpart_large_report.csv

run-corruption:
	mkdir -p $(DATA) $(REPORT)
	$(PYTHON) scripts/generate.py --scenario $(CORR_SCEN) --out $(DATA)/corruption.csv
	$(PYTHON) scripts/baselines/threshold.py --inp $(DATA)/corruption.csv --out $(DATA)/corruption_pred.csv --scenario $(CORR_SCEN) --metric error_rate_pct
	$(PYTHON) scripts/evaluate.py --scenario $(CORR_SCEN) --data $(DATA)/corruption.csv --pred $(DATA)/corruption_pred.csv --out $(REPORT)/corruption_report.csv