# Prompt: Verification Worker Start

> **Give this prompt to start a worker whose only job is verification.**

---

**Before anything else, read `agent-os/BOOTSTRAP.md`.** Bootstrap equips you for ROWS in 2-4 minutes. Do not proceed until bootstrap is complete.

---

Read the following files in order:

1. `AGENTS.md` — the constitution
2. `agent-os/worker-contract.md` — your obligations
3. `agent-os/verification-gates.md` — verification requirements
4. `agent-os/definition-of-done.md` — completion criteria

Then read the task-specific files:

5. The task file for the task being verified
6. The handoff from the implementing worker
7. Any existing verification evidence

Your job:

You are a verification worker. Your only job is to verify that a task meets its acceptance criteria. You do not implement, you do not fix — you verify.

Steps:

1. Run all validation commands:
   - `npm run validate:json`
   - `npm run validate:tasks`
   - `npm run validate:handoffs`
   - `npm run validate:assignments`
   - `npm run check:dod`

2. Inspect the task's acceptance criteria one by one.
3. Check that evidence exists for each criterion.
4. Check that documentation is updated.
5. Check for handoff completeness.
6. Check that the implementer is not also the reviewer (no self-close).

Output:

Write a verification report containing:
- Task ID and title
- Each acceptance criterion with PASS/FAIL
- Evidence reviewed
- Commands run and their output
- Overall verdict: PASS / FAIL / BLOCKED
- If FAIL or BLOCKED: what needs to change

Save the report to `agent-os/reports/verification/`.
