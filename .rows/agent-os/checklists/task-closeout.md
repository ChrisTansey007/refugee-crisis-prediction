# Task Closeout Checklist

> **Complete this checklist when closing a task. ONLY the independent reviewer (not the implementing worker) may close a task.**

## Identity Check

- [ ] I am NOT the worker who implemented this task
- [ ] I am an independent reviewer (different worker or human)
- [ ] In solo mode: I am the human owner approving the work
- [ ] In multi-worker/hybrid mode: I am a different worker than the implementer

## Review

- [ ] Task file re-read
- [ ] Handoff reviewed
- [ ] Verification report reviewed
- [ ] All acceptance criteria independently verified
- [ ] `npm run check:dod` passes

## Close Actions

- [ ] Task moved to [`tasks/done/`](../tasks/done/)
- [ ] Lock file removed from [`locks/`](../locks/)
- [ ] Handoff moved from [`handoffs/active/`](../handoffs/active/) to [`handoffs/archive/`](../handoffs/archive/)
- [ ] Branch pushed to `origin` (`git push origin <branch>` confirmed — Rule 23)
- [ ] Branch merged (or PR approved for merge)
- [ ] [`state/worker-status.json`](../state/worker-status.json) updated

## Post-Close

- [ ] No orphaned branches
- [ ] No stale references
- [ ] Related tasks unblocked (if this task was a dependency)

## Related Files

- [`verification.md`](./verification.md) — Verification checklist
- [`../definition-of-done.md`](../definition-of-done.md) — Completion criteria
- [`../task-lifecycle.md`](../task-lifecycle.md) — Task state machine
