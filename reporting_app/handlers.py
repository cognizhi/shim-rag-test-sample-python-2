"""Request handlers for the reporting app.

Consumes the `ingestion_utils` package from shim-rag-test-sample-python-1. The
`submit_batch_jobs` call below is the cross-repository contract under test: it
passes `doc_ids=`, the parameter name published on `python-1@main`.
"""

from __future__ import annotations

from typing import Any

from ingestion_utils.client import IngestionClient
from ingestion_utils.seeder import submit_batch_jobs

from reporting_app.client import ReportingConfig, default_config


def submit_documents_for_report(
    documents: list[dict[str, Any]],
    config: ReportingConfig | None = None,
) -> list[dict[str, Any]]:
    """Submit the given documents for ingestion and return the created jobs.

    Cross-repository contract: `submit_batch_jobs` is owned by python-1's
    `ingestion_utils` package. This call site is what breaks if its signature
    changes — and it lives in a repository python-1's pull request never touches.
    """
    cfg = config or default_config()
    client = IngestionClient(cfg.java1_url)
    doc_ids = [d["id"] for d in documents if d.get("id")]
    return submit_batch_jobs(client, doc_ids=doc_ids, requested_by=cfg.requested_by)


def submit_single_document(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Convenience wrapper for a one-document report run."""
    return submit_documents_for_report([document])
