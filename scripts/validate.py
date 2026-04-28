#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Dict, Literal, Any
import yaml
from rich.console import Console
from rich.table import Table
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

console = Console()

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


class Evaluation(BaseModel):
    availability: Optional[Availability] = None
    tails: Optional[Tails] = None
    detection: Optional[Detection] = None
    slo: Optional[Dict[str, float]] = None


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
    version: str

    @field_validator("reproducibility")
    @classmethod
    def require_seed(cls, v):
        if "seed" not in v:
            raise ValueError("reproducibility.seed is required")
        return v

    @model_validator(mode="after")
    def check_slo_rules(self):
        slo = self.evaluation.slo or {}
        f = self.failure.type
        req = set()
        if f in ("latency_spike", "slowdown"):
            req.add("latency_ms_p99")
        if f in ("node_crash", "network_partition", "corruption"):
            req.add("error_rate_pct")
        if f == "network_partition":
            req.add("latency_ms_p99")
        missing = [k for k in req if k not in slo]
        if missing:
            raise ValueError(f"evaluation.slo missing for {f}: {', '.join(missing)}")
        return self

    @model_validator(mode="after")
    def check_version_semver(self):
        import re
        if not self.version:
            raise ValueError("Version is not defined")
        if not re.fullmatch(r"1\.0(?:\.\d+)?", self.version):
            raise ValueError(f"version {self.version} must match ^1.0(.x)? for v1 freeze")
        return self

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


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_file(path: Path, kind: Literal["scenario", "profile"]) -> Optional[str]:
    try:
        data = load_yaml(path)
        (Scenario if kind == "scenario" else SystemProfile)(**data)
        return None
    except ValidationError as e:
        return _fmt_pydantic_errors(e)
    except Exception as e:
        return str(e)


def collect(kind: Literal["scenario", "profile"]) -> List[Path]:
    root = Path(__file__).resolve().parents[1]
    folder = "scenarios" if kind == "scenario" else "system_profiles"
    return sorted([p for p in (root / "benchmarks" / folder).glob("*.yaml") if not p.name.startswith("_")])

def report(rows):
    """
    Generates and prints the ResilienceBench validation report.
    """
    table = _build_validation_table(rows)
    console.print(table)


def _build_validation_table(rows):
    table = Table(title="ResilienceBench Validation", show_lines=True)
    table.add_column("File", overflow="fold")
    table.add_column("Kind")
    table.add_column("Status")
    table.add_column("Details", overflow="fold")

    for filename, kind, is_success, details in rows:
        status_markup = "[green]OK[/green]" if is_success else "[red]FAIL[/red]"
        table.add_row(
            str(filename),
            kind,
            status_markup,
            details or ""
        )
    return table
    
def _fmt_pydantic_errors(e: ValidationError) -> str:
    parts = []
    for error in e.errors():
        loc = "/".join(str(x) for x in error.get("loc", ()))
        msg = error.get("msg", "")
        parts.append(f"{loc}: {msg}" if loc else msg)
    return "; ".join(parts)


if __name__ == "__main__":
    import sys

    kinds = ["scenario", "profile"]
    rows, exit_code = [], 0
    for k in kinds:
        for f in collect(k):
            err = validate_file(f, k)
            ok = err is None
            if not ok:
                exit_code = 1
            rows.append((f, k, ok, "" if ok else str(err)))
    report(rows)
    sys.exit(exit_code)
