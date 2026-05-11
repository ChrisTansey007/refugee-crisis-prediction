# Verification Checklist

> **Complete this checklist when verifying a task (self-check or independent review).**

## Acceptance Criteria

- [ ] Each acceptance criterion checked individually
- [ ] All criteria pass
- [ ] Any failures documented

## Automated Checks

- [ ] `npm test` passes
- [ ] `npm run lint` passes
- [ ] `npm run validate:tasks` passes
- [ ] `npm run validate:handoffs` passes
- [ ] `npm run check:dod` passes

## Manual Verification

- [ ] Feature works as described
- [ ] Edge cases tested
- [ ] Error states handled correctly
- [ ] UI looks correct (if applicable)
- [ ] No performance regressions observed

## Evidence Review

- [ ] Test output captured
- [ ] Screenshots/recordings captured (if UI)
- [ ] Documentation updated
- [ ] Handoff is complete and accurate

## Risk Assessment

- [ ] New risks identified and documented
- [ ] No security concerns introduced
- [ ] No technical debt left unexplained

## Independence Check

- [ ] If multi-worker or hybrid mode: verifier is DIFFERENT from implementer
- [ ] If solo mode: automated validation passed; human review requested

## Verdict

- [ ] **Approved** — Ready to move to `done/`
- [ ] **Changes needed** — Return to `in-progress/`
- [ ] **Blocked** — Move to `blocked/`

## Related Files

- [`../verification-gates.md`](../verification-gates.md) — Verification process
- [`../definition-of-done.md`](../definition-of-done.md) — Completion criteria
