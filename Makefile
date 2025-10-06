.PHONY: install validate docker-build docker-run
PYTHON ?= python3
IMAGE  ?= resiliencebench:v0.1
DFILE  ?= docker/Dockerfile

install:
	$(PYTHON) -m pip install -r scripts/requirements.txt

validate:
	$(PYTHON) scripts/validate.py

docker-build:
	docker build -t $(IMAGE) -f $(DFILE) .

docker-run:
	docker run --rm $(IMAGE)

.PHONY: gen baseline eval run-phase3

gen:
	python3 scripts/generate.py --scenario benchmarks/scenarios/latency_spike.yaml --out eval/samples/latency_spike.csv

baseline:
	python3 scripts/baselines/threshold.py --inp eval/samples/latency_spike.csv --out eval/samples/latency_spike_pred.csv --scenario benchmarks/scenarios/latency_spike.yaml

eval:
	python3 scripts/evaluate.py --scenario benchmarks/scenarios/latency_spike.yaml --data eval/samples/latency_spike.csv --pred eval/samples/latency_spike_pred.csv --out eval/reports/latency_spike_report.csv

run-phase3: gen baseline eval