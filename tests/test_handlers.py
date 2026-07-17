"""Smoke tests for the reporting app's upstream calls."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from reporting_app.handlers import submit_documents_for_report

_DOCS = [{"id": "doc-1"}, {"id": "doc-2"}]


def test_submit_documents_passes_document_ids_upstream():
    with patch("reporting_app.handlers.submit_batch_jobs") as submit:
        submit.return_value = [{"id": "job-1"}]
        jobs = submit_documents_for_report(_DOCS)

    assert jobs == [{"id": "job-1"}]
    _client, kwargs = submit.call_args[0], submit.call_args[1]
    assert kwargs["doc_ids"] == ["doc-1", "doc-2"]


def test_documents_without_ids_are_skipped():
    with patch("reporting_app.handlers.submit_batch_jobs") as submit:
        submit.return_value = []
        submit_documents_for_report([{"id": "doc-1"}, {"title": "no id"}])

    assert submit.call_args[1]["doc_ids"] == ["doc-1"]
