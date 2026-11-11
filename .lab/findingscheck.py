#!/usr/bin/env python3
import datetime, json, os, re, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
passed = failed = 0


def check(desc, ok, hint=""):
    global passed, failed
    if ok:
        passed += 1; print("PASS  " + desc, flush=True)
    else:
        failed += 1; print("FAIL  " + desc + (("   -> " + hint) if hint else ""), flush=True)


def sh(*a, timeout=900):
    r = subprocess.run(a, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def code(path):
    return "\n".join(l for l in open(path).read().split("\n") if not l.lstrip().startswith("#"))


print("== The scanner, exactly as the pipeline runs it ==")
rc, out, err = sh("trivy", "fs", "--scanners", "vuln,secret,misconfig", "--severity", "HIGH,CRITICAL", "--ignore-unfixed", "--exit-code", "1",
                  "--skip-dirs", ".lab", "--skip-dirs", ".trivy-cache", "--cache-dir", ".trivy-cache", "-f", "json", "-q", ".")
try:
    rep = json.loads(out)
except Exception:
    rep = {"Results": []}
vulns = [(r["Target"], v["VulnerabilityID"]) for r in rep.get("Results", []) for v in r.get("Vulnerabilities") or []]
secrets = [(r["Target"], s["RuleID"]) for r in rep.get("Results", []) for s in r.get("Secrets") or []]
misc = [(r["Target"], m["ID"]) for r in rep.get("Results", []) for m in r.get("Misconfigurations") or [] if m.get("Status") == "FAIL"]
check("no HIGH or CRITICAL vulnerability in the dependencies (found %d)" % len(vulns), not vulns, ", ".join(sorted({v for _, v in vulns}))[:150])
check("no secret in any file (found %d)" % len(secrets), not secrets, ", ".join("%s:%s" % s for s in secrets)[:150])
check("no HIGH or CRITICAL misconfiguration in the Dockerfile (found %d)" % len(misc), not misc, ", ".join(m for _, m in misc))
check("trivy exits 0 with --exit-code 1 (this is what the pipeline gate does)", rc == 0 and not (vulns or secrets or misc))

print("== The fixes are real, not hidden ==")
ign = [l.strip() for l in open(".trivyignore").read().split("\n") if l.strip() and not l.strip().startswith("#")]
ok_ign = True
for l in ign:
    m = re.search(r"reason:\s*\S+.*owner:\s*\S+.*expires:\s*(\d{4}-\d{2}-\d{2})", l)
    if not m or datetime.date.fromisoformat(m.group(1)) < datetime.date.today():
        ok_ign = False
check(".trivyignore has no entry, or only entries with a reason, an owner and a future expiry (%d entries)" % len(ign), ok_ign and len(ign) <= 2, "CVE-ID   # reason: ...  owner: ...  expires: YYYY-MM-DD")
req = open("service/requirements.txt").read()
check("the dependencies were upgraded, not deleted: requests, PyYAML, Jinja2 and urllib3 are still required", all(re.search(r"(?im)^\s*%s\b" % p, req) for p in ("requests", "pyyaml", "jinja2", "urllib3")))
check("every dependency is pinned to an exact version with == (a scanner cannot judge `>=`, and neither can a reproducible build)", all("==" in l for l in req.split("\n") if l.strip() and not l.strip().startswith("#")))
check("no dependency is pinned to the old versions any more", not re.search(r"(?i)requests==2\.19|pyyaml==5\.3|jinja2==2\.10|urllib3==1\.24", req))
s = open("service/settings.py").read()
check("settings.py reads the keys from the environment (os.environ), with no key written in it", "os.environ" in s and not re.search(r"AKIA[0-9A-Z]{16}", s) and not re.search(r"[A-Za-z0-9+/]{40}", s.replace("pollie-announcements", "")))
rc, o, e = sh(sys.executable, "-m", "unittest", "discover", "-s", "tests")
check("the unit tests still pass (the service still works)", rc == 0, e[-300:])

print("== The Dockerfile ==")
d = code("Dockerfile")
check("the base image is pinned to a version, not :latest", re.search(r"^FROM\s+\S+:(?!latest)\S+", d, re.M) is not None and ":latest" not in d)
check("no ADD of a remote URL (use COPY, or download with a checksum)", not re.search(r"^ADD\s+https?://", d, re.M))
check("the container runs as a non-root user (USER ...)", re.findall(r"^USER\s+(\S+)", d, re.M)[-1:] not in ([], ["root"], ["0"]))
check("there is a HEALTHCHECK", re.search(r"^HEALTHCHECK\s", d, re.M) is not None)
check("apt installs use --no-install-recommends and clean the lists (or apt is not used)", "apt-get" not in d or ("--no-install-recommends" in d and "rm -rf /var/lib/apt/lists" in d))

print("== The pipeline ==")
wf = ".github/workflows/security.yml"
check(".github/workflows/security.yml exists", os.path.exists(wf))
if os.path.exists(wf):
    import yaml
    doc = yaml.safe_load(open(wf)) or {}
    on = doc.get("on", doc.get(True))
    trig = set(on) if isinstance(on, (dict, list)) else {on}
    text = open(wf).read()
    check("it runs on pull_request and on push to main", "pull_request" in trig and "push" in trig)
    check("it has `permissions: contents: read`", (doc.get("permissions") or {}).get("contents") == "read" if isinstance(doc.get("permissions"), dict) else False)
    check("it runs Trivy and fails the build (exit-code 1) on HIGH and CRITICAL", "trivy" in text.lower() and re.search(r"exit-code['\"]?:?\s*['\"]?1", text) and "HIGH" in text and "CRITICAL" in text)
    uses = re.findall(r"uses:\s*(\S+)", text)
    check("every action in it is pinned to a full commit SHA", bool(uses) and all(re.fullmatch(r"[0-9a-f]{40}", u.partition("@")[2]) for u in uses if not u.startswith("./")))
    check("it also runs on a schedule (the vulnerability database changes every day)", "schedule" in trig)
t = open("TRIAGE.md").read()
check("TRIAGE.md is filled in (no TODO left)", "TODO" not in t and len(t.split()) > 80)
print()
print(("ALL CHECKS PASSED (%d/%d)" % (passed, passed)) if failed == 0 else ("%d check(s) failed, %d passed" % (failed, passed)))
sys.exit(1 if failed else 0)
