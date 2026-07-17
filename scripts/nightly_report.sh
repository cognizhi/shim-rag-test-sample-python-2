#!/usr/bin/env bash
# Nightly reporting run.
#
# Cross-repository contract fixture — the SHELL channel. Everything this script
# depends on is a contract owned by shim-rag-test-sample-python-1, and none of it
# is visible to an import-based dependency index:
#
#   * the CLI subcommand name        `submit_batch_jobs`
#   * the flag names                 `--requested-by`, `--java1-url`
#   * the exit-code semantics        0 = every job submitted
#   * the stdout shape              (grepped below)
#
# A rename on any of them breaks this file, which lives in a repository the
# provider's pull request never touches.
set -uo pipefail

# Contract: env var name owned by this repo's client.py, consumed here.
INGESTION_URL="${JAVA1_URL:-http://localhost:8081}"
REQUESTER="${REPORT_REQUESTER:-nightly-report}"

echo "[nightly] submitting batch jobs via ${INGESTION_URL}"

# Contract: subcommand + flag names owned by ingestion_utils/cli.py (python-1).
python -m ingestion_utils.cli submit_batch_jobs \
  --java1-url "${INGESTION_URL}" \
  --requested-by "${REQUESTER}" \
  > /tmp/nightly_submit.log 2>&1
rc=$?

# Contract: exit-code semantics. 0 is documented as "all jobs submitted".
# A provider that starts returning 2 for "partial success" silently sends this
# script down the failure branch — or worse, a provider that returns 0 on
# partial success sends it down the success branch with jobs missing.
if [ $rc -ne 0 ]; then
  echo "[nightly] FAILED (rc=${rc}) — see /tmp/nightly_submit.log" >&2
  exit "$rc"
fi

# Contract: stdout shape. The CLI prints "  [OK] IngestionJob: <id> ..." per job;
# this count feeds the report. A format change silently yields zero.
submitted=$(grep -c '\[OK\] IngestionJob:' /tmp/nightly_submit.log || true)
echo "[nightly] submitted ${submitted} job(s)"

if [ "${submitted}" -eq 0 ]; then
  echo "[nightly] WARNING: no jobs parsed from output — CLI format may have changed" >&2
fi
