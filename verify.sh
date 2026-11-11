#!/usr/bin/env bash
# Scans your work like the pipeline would and checks your decisions. Run with: ./verify.sh
cd "$(dirname "$0")" || exit 1
command -v trivy >/dev/null || { echo "trivy is not installed." >&2; exit 1; }
[ -f service/settings.py ] || { echo "Run ./setup.sh first." >&2; exit 1; }
exec python3 .lab/findingscheck.py
