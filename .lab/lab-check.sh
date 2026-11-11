#!/usr/bin/env bash
rc=0
grep -q 'TODO' TRIAGE.md && { echo "- ❌ TRIAGE.md still has TODO"; rc=1; } || echo "- ✅ TRIAGE.md is filled in"
test -f .github/workflows/security.yml && echo "- ✅ the security workflow exists" || { echo "- ❌ .github/workflows/security.yml is missing"; rc=1; }
git ls-files | xargs grep -lE 'AKIA[0-9A-Z]{16}' 2>/dev/null | grep -v '^[.]lab/' | grep -q . && { echo "- ❌ a key pattern is committed"; rc=1; } || echo "- ✅ no key committed"
grep -qE '^ALL CHECKS PASSED \(' SUBMISSION.md && echo "- ✅ SUBMISSION.md shows ALL CHECKS PASSED" || { echo "- ❌ paste the verify.sh output ('ALL CHECKS PASSED') into SUBMISSION.md"; rc=1; }
exit $rc
