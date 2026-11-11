#!/usr/bin/env bash
# Proves the lab left nothing behind. Run with: ./verify-teardown.sh
cd "$(dirname "$0")" || exit 1
pass=0; failn=0
check() { local d="$1"; shift; if "$@" >/dev/null 2>&1; then echo "PASS  $d"; pass=$((pass+1)); else echo "FAIL  $d"; failn=$((failn+1)); fi; }
check "no scanner cache or Python cache in the lab folder" bash -c '[ ! -d .trivy-cache ] && [ -z "$(find . -name __pycache__ -type d)" ]'
check "no key pattern is left in a tracked file" bash -c '! git ls-files | xargs grep -lE "AKIA[0-9A-Z]{16}" 2>/dev/null | grep -v "^[.]lab/" | grep -q .'
echo
if [ "$failn" -eq 0 ]; then echo "TEARDOWN VERIFIED ($pass/$pass) on this machine"; else echo "NOT CLEAN: $failn leftover(s)."; fi
exit "$failn"
