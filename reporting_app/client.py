"""Configuration for the upstream ingestion service."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ReportingConfig:
    """Where the upstream java-1 ingestion service lives."""

    java1_url: str = os.environ.get("JAVA1_URL", "http://localhost:8081")
    requested_by: str = "reporting-app"


def default_config() -> ReportingConfig:
    return ReportingConfig()
