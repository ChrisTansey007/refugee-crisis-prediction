# Verification Gates

> **Every task must pass through these verification gates before it can be marked done.**

## Gate 1: Self-Check

**Performed by:** The implementing worker.

The worker verifies their own work against the task's acceptance criteria before submitting for review.

- [ ] Each acceptance criterion checked and confirmed.
- [ ] All tests pass locally.
- [ ] Linting passes.
- [ ] No obvious regressions.
- [ ] Documentation updated.

## Gate 2: Automated Check

**Performed by:** Scripts and CI.

Automated validation runs against the worker's changes.

- [ ] `npm test` passes.
- [ ] `npm run lint` passes.
- [ ] `npm run validate:tasks` passes.
- [ ] `npm run validate:handoffs` passes.
- [ ] `npm run check:dod` passes.

## Gate 3: Independent Worker Review

**Performed by:** A DIFFERENT worker (not the implementing worker).

A second worker reviews the implementation, evidence, and handoff.

- [ ] Reviewer confirms they are NOT the implementing worker.
- [ ] Reviewer reads the task file, handoff, and verification report.
- [ ] Reviewer independently verifies acceptance criteria.
- [ ] Reviewer checks for regressions.
- [ ] Reviewer approves or requests changes.

## Gate 4: Human Review

**Performed by:** The human project owner.

For critical tasks, security-sensitive changes, or when automated/worker review is insufficient.

- [ ] Human reads the task, handoff, and verification report.
- [ ] Human confirms the change meets expectations.
- [ ] Human approves merge.

## Evidence Requirements

All verification must produce evidence:
- **Self-check:** Notes in the handoff.
- **Automated:** CI logs, test output files.
- **Worker review:** Review comments, approval in the task file.
- **Human review:** Approval comment or PR merge.

## Escalation

If any gate fails:
1. Document the failure in the verification report.
2. Move the task back to `in-progress/` or to `blocked/`.
3. Note the failure in the handoff.
4. The implementing worker addresses the issues.

## Execution Mode Notes

- **Solo mode:** Gate 3 (Independent Worker Review) is replaced by automated validation or human review. The solo worker must not self-verify as "independent."
- **Multi-worker mode:** All gates apply. Gate 3 must use a different worker.
- **Hybrid mode:** Support workers may perform Gate 3 for the primary worker.

## Related Files

- [`definition-of-done.md`](./definition-of-done.md) — Completion criteria
- [`task-lifecycle.md`](./task-lifecycle.md) — Task state machine
- [`escalation-rules.md`](./escalation-rules.md) — Escalation rules
- [`execution-modes.md`](./execution-modes.md) — Execution modes
