> **New to this repo?** Read `agent-os/BOOTSTRAP.md` first.

# Prompt: Template Publish Check

> **Give this prompt to a worker to perform final template publish readiness review.**

---

Read the following files:

1. `AGENTS.md` — the constitution
2. `README.md` — the public face of the template
3. `PROJECT_GOAL.md` — the intake form
4. `TEMPLATE_READINESS.md` — readiness gates
5. `RELEASE_CHECKLIST.md` — publishing checklist
6. `HUMAN_OWNER_GUIDE.md` — human owner guide
7. `prompt-library/README.md` — prompt library overview
8. `examples/README.md` — examples overview

Your job:

Perform a final template publish readiness review.

Checklist:

1. Run `npm run audit` — all checks must pass.
2. Run `npm run validate:template` — template readiness must pass.
3. Inspect `README.md` — is it polished and fork-ready?
4. Inspect `AGENTS.md` — is the constitution complete?
5. Inspect `PROJECT_GOAL.md` — is it a usable intake form?
6. Inspect `prompt-library/` — are all prompts present and copy/paste ready?
7. Inspect `examples/` — are all examples present and clearly marked?
8. Check for Copilot files — none should exist.
9. Check for application-specific code — `src/` and `tests/` should be generic.
10. Check for empty files — none should exist.
11. Check for vague placeholders — none should exist outside intentional template markers.
12. Review validation reports in `agent-os/reports/`.

Output:

Write a final readiness assessment:
- Overall verdict: READY / NOT READY
- List of issues found (if any)
- Recommendations for fixes (if any)
- Confirmation that all gates pass (or which gates fail)
