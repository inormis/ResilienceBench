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