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