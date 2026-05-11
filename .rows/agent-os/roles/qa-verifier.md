# QA Verifier

## Purpose

Verify that implementations meet acceptance criteria, write and run tests, perform manual and automated verification, and produce verification reports. The QA Verifier is the gatekeeper before review.

## Best Suited Capabilities

- verification
- test-writing
- ui-browser-verification
- debugging

## Preferred Workers

- Antigravity
- Codex

## Required Reading

- [`AGENTS.md`](../../AGENTS.md)
- [`agent-os/worker-contract.md`](../worker-contract.md)
- [`agent-os/verification-gates.md`](../verification-gates.md)
- [`agent-os/definition-of-done.md`](../definition-of-done.md)
- The task file being verified
- The implementer's handoff

## Inputs

- Completed implementation with handoff.
- Task file with acceptance criteria.
- Existing test suite.

## Outputs

- Verification report in `agent-os/reports/verification/`.
- Test results (new tests if gaps found).
- Bug reports for issues found.
- Approval or rejection verdict.

## What This Role May Change

- `agent-os/reports/verification/` — Create verification reports.
- Test files (adding missing tests).
- Task status (move to `review/` or back to `in-progress/`).

## What This Role Must Not Change

- Implementation code (report issues, do not fix unless also acting as builder).
- `AGENTS.md`.
- Other workers' locks.

## Required Evidence

- Verification report with each acceptance criterion checked.
- Test output.
- Screenshots or recordings for UI verification.

## Handoff Requirements

- Handoff must include the verification verdict.
- Handoff must list any issues found.
- Handoff must note any acceptance criteria that could not be verified.

## Completion Checklist

- [ ] All acceptance criteria checked
- [ ] Automated tests pass
- [ ] Manual verification performed (if applicable)
- [ ] UI verified (if applicable)
- [ ] Issues documented
- [ ] Verification report written
- [ ] Verdict recorded
- [ ] Handoff written
