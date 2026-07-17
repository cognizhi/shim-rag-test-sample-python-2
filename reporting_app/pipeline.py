"""Nightly reporting pipeline.

A second, independent call site for the same upstream contract, so a signature
change in `ingestion_utils` fans in to more than one location in this
repository.
"""

from __future__ import annotations

from typing import Any

from ingestion_utils.client import IngestionClient
from ingestion_utils.seeder import submit_batch_jobs

from reporting_app.client import default_config


def run_nightly_batch(document_ids: list[str]) -> list[dict[str, Any]]:
    """Resubmit a fixed set of document IDs for the nightly report."""
    cfg = default_config()
    client = IngestionClient(cfg.java1_url)
    # Same upstream contract as handlers.submit_documents_for_report.
    return submit_batch_jobs(client, doc_ids=document_ids, requested_by="nightly-report")
