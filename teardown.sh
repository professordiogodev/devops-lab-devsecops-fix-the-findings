#!/usr/bin/env bash
# Removes the scanner cache of this lab. Run with: ./teardown.sh
cd "$(dirname "$0")" || exit 1
rm -rf .trivy-cache
find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null
echo "Now run ./verify-teardown.sh"
