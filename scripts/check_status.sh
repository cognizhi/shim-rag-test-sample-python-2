#!/usr/bin/env bash
# Poll job status for the report.
#
# Cross-repository contract fixture — the HTTP/JSON channel reached from shell.
# The `processingStatus` field name is owned by java-1's IngestionJob model and
# is read here with `jq`. java-1 renaming it to `status` makes this print
# "null" forever: no error, no non-zero exit, just a wrong report.
set -uo pipefail

INGESTION_URL="${JAVA1_URL:-http://localhost:8081}"

# Contract: JSON field name emitted by java-1 (Jackson derives it from the Java
# field). Renaming the field silently turns this into `null`.
curl -sS "${INGESTION_URL}/documents" \
  | jq -r '.[] | "\(.id) \(.processingStatus)"'

# Contract: the enum's value domain. java-1 adding RETRYING means this
# exhaustive check silently classifies a live job as "unknown".
curl -sS "${INGESTION_URL}/documents" | jq -r '.[].processingStatus' | while read -r st; do
  case "$st" in
    PENDING|RUNNING) echo "in-flight: $st" ;;
    COMPLETED|FAILED) echo "terminal: $st" ;;
    *) echo "unknown status: $st" >&2 ;;
  esac
done
