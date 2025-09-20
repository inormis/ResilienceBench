#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Dict, Literal, Any
import sys, yaml
import typer
from rich.console import Console
from rich.table import Table
from pydantic import BaseModel, Field, ValidationError, field_validator

app = typer.Typer(add_completion=False)
console = Console()

# ---------- Models ----------

FailureType = Literal["network_partition", "node_crash", "latency_spike", "corruption", "slowdown"]


class Dataset(BaseModel):
    source: Literal["synthetic", "trace", "live"]
    duration_s: int = Field(gt=0)
    warmup_s: int = Field(ge=0)


class Failure(BaseModel):
    type: FailureType
    start_s: int = Field(ge=0)
    duration_s: int = Field(gt=0)
    parameters: Dict[str, Any]


class GroundTruth(BaseModel):
    label_name: str = "fault"
    positive_interval_s: List[int] = Field(min_length=2, max_length=2)


class Availability(BaseModel):
    mtbf_s: int = Field(gt=0)
    mttr_s: int = Field(gt=0)


class Tails(BaseModel):
    p99_targets: List[str] = Field(min_length=1)


class Detection(BaseModel):
    window_tolerance_s: int = Field(ge=0, le=60)
    metrics: List[Literal["precision", "recall", "f1"]] = Field(min_length=1)


class SLO(BaseModel):
    # add domain SLOs as needed (free-form numeric thresholds)
    __root__: Dict[str, float]


class Evaluation(BaseModel):
    availability: Optional[Availability] = None
    tails: Optional[Tails] = None
    detection: Optional[Detection] = None
    slo: Optional[SLO] = None

    @field_validator("availability")
    @classmethod
    def pairwise_availability(cls, v):
        # if present, both mtbf and mttr are required by type; nothing else needed
        return v


class Scenario(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9_]+$")
    title: str
    description: str
    tags: List[str] = Field(min_length=1)
    system_profile: str
    dataset: Dataset
    failure: Failure
    ground_truth: GroundTruth
    evaluation: Evaluation
    reproducibility: Dict[str, Any]
    version: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("reproducibility")
    @classmethod
    def require_seed(cls, v):
        if "seed" not in v:
            raise ValueError("reproducibility.seed is required")
        return v


class Node(BaseModel):
    id: str
    role: str


class MetricThresholds(BaseModel):
    nominal: float
    warning: Optional[float] = None
    critical: Optional[float] = None
    max: Optional[float] = None


class SystemProfile(BaseModel):
    name: str
    description: Optional[str] = ""
    sampling_defaults_hz: int = Field(gt=0)
    nodes: List[Node] = Field(min_length=1)
    metrics: Dict[str, MetricThresholds]
    notes: Optional[str] = None


# ---------- Helpers ----------

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_file(path: Path, kind: Literal["scenario", "profile"]) -> Optional[str]:
    try:
        data = load_yaml(path)
        if kind == "scenario":
            Scenario(**data)
        else:
            SystemProfile(**data)
        return None
    except ValidationError as e:
        return e.short_errors()
    except Exception as e:
        return str(e)


def collect(kind: Literal["scenario", "profile"]) -> List[Path]:
    root = Path(__file__).resolve().parents[1]
    if kind == "scenario":
        return sorted([p for p in (root / "benchmarks" / "scenarios").glob("*.yaml") if not p.name.startswith("_")])
    else:
        return sorted(
            [p for p in (root / "benchmarks" / "system_profiles").glob("*.yaml") if not p.name.startswith("_")])


def report(rows):
    t = Table(title="ResilienceBench Validation", show_lines=True)
    t.add_column("File", overflow="fold")
    t.add_column("Kind")
    t.add_column("Status")
    t.add_column("Details", overflow="fold")
    for file, kind, ok, msg in rows:
        t.add_row(str(file), kind, "[green]OK[/green]" if ok else "[red]FAIL[/red]", msg or "")
    Console().print(t)


@app.command()
def main(target: Optional[str] = typer.Argument(None, help="scenarios | profiles | all")):
    kinds = ["scenarios", "profiles"] if target in (None, "all") else [target]
    rows = []
    exit_code = 0
    for k in kinds:
        kind = "scenario" if k.startswith("scenario") else "profile"
        files = collect(kind)
        for f in files:
            err = validate_file(f, kind)
            ok = err is None
            if not ok:
                exit_code = 1
            rows.append((f.relative_to(Path(__file__).resolve().parents[1]), kind, ok, "" if ok else str(err)))
    report(rows)
    raise typer.Exit(code=exit_code)


if __name__ == "__main__":
    app()
