# shim-rag-test-sample-python-2 — downstream reporting app

A small Python service that consumes the `ingestion_utils` package published by
[`shim-rag-test-sample-python-1`](https://github.com/cognizhi/shim-rag-test-sample-python-1).

## Why this repository exists

It is the **consumer side of a cross-repository contract**. `python-1` provides
the `ingestion_utils` package; this app imports it and calls its API:

```python
from ingestion_utils.seeder import submit_batch_jobs

jobs = submit_batch_jobs(client, doc_ids=[d["id"] for d in docs])
```

That import creates a real dependency edge (`ingestion_utils`) from this
repository to `python-1`. When `python-1` changes the signature of a symbol this
app calls, the break lives **here** — in a repository the provider's pull request
does not touch and its author may never open.

That is the case cross-repository contract-impact analysis exists to catch, and
it is why this repository is deliberately small: it is a fixture, not a product.

## Layout

| Path                      | Role                                                    |
| ------------------------- | ------------------------------------------------------- |
| `reporting_app/handlers.py` | Calls `submit_batch_jobs(...)` — the contract under test |
| `reporting_app/pipeline.py` | A second caller, so fan-in is exercised                 |
| `reporting_app/client.py`   | Thin config holder                                       |

## Related fixtures

- `python-1` @ `codereview-test/hidden-caller-break` renames
  `submit_batch_jobs(doc_ids=...)` to `submit_batch_jobs(documents=...)`. Both
  callers in this repository still pass `doc_ids=` and would raise `TypeError`.
