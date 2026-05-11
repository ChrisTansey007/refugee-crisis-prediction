# Escalation Rules

> **When blocked, uncertain, or facing a conflict, follow these rules. Do not guess. Do not proceed silently.**

## When to Escalate

Escalate immediately when encountering:

### Blockers
- A dependency task is not done and your task cannot proceed.
- Required information is missing from `PROJECT_GOAL.md` or task files.
- A required file is locked by another worker and the lock is not stale.

### Conflicting Instructions
- `AGENTS.md` contradicts a task file.
- A tool adapter file contradicts `AGENTS.md`.
- Two task files have overlapping or conflicting objectives.

### File Ownership Conflicts
- Another worker's lock covers files you need to modify.
- A file you need was recently changed by another worker.
- You discover uncommitted changes in your task's scope.

### Security Concerns
- You discover a secret, key, or credential in the codebase.
- A task asks you to implement something that seems insecure.
- You are asked to run a destructive command.

### Failing Tests
- Pre-existing tests fail before your changes.
- Your changes cause unrelated test failures.
- Flaky tests block verification.

### Assignment Issues
- The task's required capabilities do not match your strengths.
- The preferred worker list excludes you but you believe you can perform the task.
- The execution mode prevents you from claiming the task.
- A reassignment is needed but the previous worker is unavailable.

### Missing Context
- The task file is too vague to implement.
- Acceptance criteria are not testable.
- Required reading files are missing or empty.

### Scope Uncertainty
- The task seems too large for one session.
- The task's scope overlaps with another task.
- You are unsure whether a change is within scope.

## How to Escalate

1. **Document the issue** in your handoff file.
2. **Move the task to `blocked/`** if work cannot continue.
3. **Describe:** What is blocked, why, and what is needed to unblock.
4. **Propose:** A suggested resolution (if you have one).
5. **Notify:** The human owner (via PR comment, issue, or direct communication).

## Stale Lock Resolution

If a lock file's `expires_at` has passed:
1. Note the stale lock in your handoff.
2. Do NOT delete the lock file yourself.
3. Escalate to the human for resolution.
4. The human may delete the stale lock or contact the locking worker.
5. If reassignment is needed, follow [`worker-switching-protocol.md`](./worker-switching-protocol.md).
6. Create a reassignment record using [`reassignment/reassignment-template.md`](./reassignment/reassignment-template.md).

## Emergency Escalation

For security issues or destructive command risks:
- **Stop immediately.** Do not proceed.
- **Document** what triggered the concern.
- **Contact the human owner directly.**
- Do not commit, push, or deploy until resolved.

## Related Files

- [`worker-contract.md`](./worker-contract.md) — Worker obligations
- [`verification-gates.md`](./verification-gates.md) — Verification checkpoints
- [`locks/README.md`](./locks/README.md) — Lock protocol
- [`worker-switching-protocol.md`](./worker-switching-protocol.md) — Reassignment protocol
