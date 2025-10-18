FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./scripts/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY benchmarks ./benchmarks
COPY scripts ./scripts
COPY README.md ./README.md

CMD ["python", "scripts/validate.py"]