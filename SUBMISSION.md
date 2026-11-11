# Submission

Fork URL: <!-- paste the URL of your fork here -->

## Files to commit

- [ ] `service/requirements.txt`, `service/settings.py`, `Dockerfile`: fixed
- [ ] `.github/workflows/security.yml`: the scan in the pipeline
- [ ] `.trivyignore`: only justified exceptions
- [ ] `TRIAGE.md`: your decisions

## Questions

Answer in your own words. Where a question asks for output, paste it in a code block.

### Q1. Paste the summary table of the first `trivy fs` run (counts per target). What is the difference between a vulnerability, a secret and a misconfiguration finding? Which of them can you fix by changing a file, and which need an action outside the repository?

**Your answer:**

<!-- replace this line with your answer -->

### Q2. The two leaked keys: you removed them from the file. Why is that not enough? List, in order, what you do in a real incident (hint: the first step is not in git). What does `git log -p` still show?

**Your answer:**

<!-- replace this line with your answer -->

### Q3. Pick two CVEs from the list. For each: what is it, what is the fixed version, does your code even reach the vulnerable function, and why do you upgrade anyway? Which is "reachable" and which is not?

**Your answer:**

<!-- replace this line with your answer -->

### Q4. What does `--ignore-unfixed` do and why is it a policy decision? What does a `.trivyignore` entry need (reason, owner, expiry) so that it does not become a permanent hole?

**Your answer:**

<!-- replace this line with your answer -->

### Q5. Show your pipeline step. Why does it fail the build on HIGH and CRITICAL but only report MEDIUM? What happens to a developer's morning if it fails on every finding, including LOW?

**Your answer:**

<!-- replace this line with your answer -->

### Q6. The database of known vulnerabilities changes every day. Your code did not. Why can a build that passed yesterday fail today, and is that a bug in the pipeline? What do you do about it (scheduled scans, Dependabot)?

**Your answer:**

<!-- replace this line with your answer -->

### Q7. Paste the output of `./verify.sh`. It must end with **ALL CHECKS PASSED**.

**Your answer:**

<!-- replace this line with your answer -->

### Q8. **Tear down.** Paste the output of `./verify-teardown.sh`. It must end with **TEARDOWN VERIFIED**.

**Your answer:**

<!-- replace this line with your answer -->
