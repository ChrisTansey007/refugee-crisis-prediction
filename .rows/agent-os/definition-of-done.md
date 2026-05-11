# Definition of Done

> **A task is NOT done until ALL applicable criteria are satisfied. No exceptions.**

## Completion Criteria

### 1. Functional Completion
- [ ] All acceptance criteria from the task file are met.
- [ ] The feature works as described in the task objective.
- [ ] Edge cases identified in the task are handled.

### 2. Tests
- [ ] New code has corresponding tests.
- [ ] All existing tests continue to pass.
- [ ] Bug fixes include a regression test.
- [ ] Test coverage meets project standards (see [`docs/03-development/testing-standards.md`](../docs/03-development/testing-standards.md)).

### 3. Documentation
- [ ] Changed behavior is reflected in relevant docs.
- [ ] New APIs are documented in API contracts.
- [ ] New architectural decisions have an ADR.
- [ ] README or setup docs updated if needed.

### 4. Verification Evidence
- [ ] Test output captured and saved.
- [ ] Screenshots/recordings for UI changes.
- [ ] Verification report written in `reports/verification/`.
- [ ] Evidence is sufficient for an independent reviewer to confirm completion.

### 5. Handoff
- [ ] Handoff file written using the template.
- [ ] Handoff placed in `handoffs/active/`.
- [ ] Handoff includes: summary, files changed, evidence, known issues, risks, next steps.

### 6. Risk Review
- [ ] New risks documented in the handoff.
- [ ] Risk register updated if significant new risks discovered.
- [ ] No unresolved security concerns.

### 7. No Placeholders
- [ ] No unresolved task markers left in code (unless explicitly allowed by task).
- [ ] No placeholder values in configuration.
- [ ] No commented-out code without explanation.

### 8. Independent Review
- [ ] Task reviewed by a DIFFERENT worker or a human.
- [ ] Reviewer is NOT the implementing worker.
- [ ] Reviewer has confirmed all criteria independently.
- [ ] Reviewer has moved the task to `done/`.

## Execution Mode Considerations

### Solo Mode
- The implementing worker must not self-close.
- Automated validation (`npm run check:dod`) is required.
- Human approval is required for final closure.

### Multi-Worker Mode
- A different worker must perform the independent review.
- The reviewer must confirm they are not the implementer.
- Both implementer and reviewer handoffs are required.

### Hybrid Mode
- Support workers may act as independent reviewers.
- Primary worker must not self-close without support worker or human approval.

## Hard Rules

1. **No worker may mark its own task as done.** This is the most important rule in the system.
2. **Undocumented changes are incomplete changes.**
3. **Untested code is incomplete code.**
4. **Missing handoff = incomplete session.**
5. **No private-memory dependency.** All completion evidence must be in repo files.

## Related Files

- [`verification-gates.md`](./verification-gates.md) — Verification checkpoints
- [`task-lifecycle.md`](./task-lifecycle.md) — Task state machine
- [`worker-contract.md`](./worker-contract.md) — Worker obligations
- [`execution-modes.md`](./execution-modes.md) — Execution modes
