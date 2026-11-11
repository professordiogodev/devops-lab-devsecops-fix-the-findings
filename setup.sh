#!/usr/bin/env bash
# Creates service/settings.py with two FAKE leaked keys (random each time) and checks that Trivy is installed. Run: ./setup.sh
set -u
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "MISSING: python3"; exit 1; }
command -v trivy >/dev/null || { echo "MISSING: trivy.  macOS: brew install trivy   Linux/WSL: https://trivy.dev/latest/getting-started/installation/"; exit 1; }
python3 - <<'PY'
import random, string
r = random.SystemRandom()
akid = "AKIA" + "".join(r.choice(string.ascii_uppercase + string.digits) for _ in range(16))
secret = "".join(r.choice(string.ascii_letters + string.digits + "+/") for _ in range(40))
open("service/settings.py", "w").write('''"""Settings of the service. Written in a hurry, the week before the demo."""
AWS_ACCESS_KEY_ID = "%s"
AWS_SECRET_ACCESS_KEY = "%s"
BUCKET = "pollie-announcements"
''' % (akid, secret))
PY
echo "service/settings.py now contains two (fake) keys, as if a colleague had committed them."
echo "Run your first scan:   trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --ignore-unfixed ."
