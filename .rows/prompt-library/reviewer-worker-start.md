# Prompt: Reviewer Worker Start

> **Give this prompt to start a worker reviewing another worker's output.**

---

**Before anything else, read `agent-os/BOOTSTRAP.md`.** Bootstrap equips you for ROWS in 2-4 minutes. Do not proceed until bootstrap is complete.

---

Read the following files in order:

1. `AGENTS.md` — the constitution
2. `agent-os/worker-contract.md` — your obligations
3. `agent-os/verification-gates.md` — verification requirements
4. `agent-os/definition-of-done.md` — completion criteria

Then read the task-specific files:

5. The task file in `agent-os/tasks/review/` (or wherever the task currently is)
6. The handoff from the implementing worker in `agent-os/handoffs/active/`
7. The verification report in `agent-os/reports/verification/`
8. Any changed files referenced in the handoff

Your job:

You are reviewing another worker's completed task. Your role is to independently verify that the work meets all acceptance criteria.

Rules you MUST follow:

1. Confirm you are NOT the implementing worker. If you implemented this task, you cannot review it.
2. Read the task file, handoff, and verification evidence thoroughly.
3. Independently verify each acceptance criterion.
4. Check for regressions, edge cases, and documentation updates.
5. Write your review findings.
6. If the task passes: approve it for closure.
7. If the task fails: document what needs to be fixed and move it back to `in-progress/` or `blocked/`.

Do NOT:
- Start implementing fixes (unless explicitly asked).
- Approve without thorough review.
- Rely on the implementer's self-assessment alone.

After review:
- Write review findings in the task file or a separate review note.
- If approving: move task to `done/`, remove the lock, archive the handoff.
- If rejecting: move task back to `in-progress/` with clear feedback.
