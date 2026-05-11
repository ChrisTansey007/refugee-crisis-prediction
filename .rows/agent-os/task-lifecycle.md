# Task Lifecycle

> **The complete state machine for tasks in the ROWS system.**

## State Diagram

```
                    ┌──────────┐
                    │  backlog │  ← Task proposed, not yet approved
                    └────┬─────┘
                         │ Human approves
                         ▼
                    ┌──────────┐
                    │  ready   │  ← Approved and claimable
                    └────┬─────┘
                         │ Worker claims
                         ▼
                    ┌──────────┐
                    │ claimed  │  ← Claimed, lock created
                    └────┬─────┘
                         │ Worker begins
                         ▼
                    ┌──────────┐      ┌──────────┐
                    │in-progress│─────▶│ blocked  │  ← Cannot proceed
                    └────┬─────┘      └──────────┘
                         │ Worker completes
                         ▼
                    ┌──────────┐
                    │  review  │  ← Awaiting verification
                    └────┬─────┘
                         │ Independent verifier approves
                         ▼
                    ┌──────────┐
                    │   done   │  ← Verified and complete
                    └──────────┘
```

## States

### `backlog`
- **Meaning:** Task has been proposed but not yet approved for work.
- **Who can move here:** Any worker (task decomposition), human.
- **Who can move from here:** Human only.
- **Required evidence:** None — this is a proposal state.
- **Next allowed states:** `ready` (approved), deleted (rejected).

### `ready`
- **Meaning:** Task is approved and ready to be claimed.
- **Who can move here:** Human only.
- **Who can move from here:** Any worker (by claiming).
- **Required evidence:** None — approval is implicit by being in this folder.
- **Next allowed states:** `claimed`.

### `claimed`
- **Meaning:** A worker has claimed this task and created a lock.
- **Who can move here:** The claiming worker.
- **Who can move from here:** The claiming worker.
- **Required evidence:** Lock file must exist in `locks/`.
- **Next allowed states:** `in-progress`, `ready` (if released).

### `in-progress`
- **Meaning:** Work is actively happening.
- **Who can move here:** The claiming worker.
- **Who can move from here:** The claiming worker.
- **Required evidence:** Branch created, work begun.
- **Next allowed states:** `review`, `blocked`.

### `review`
- **Meaning:** Work is complete and awaiting independent verification.
- **Who can move here:** The implementing worker.
- **Who can move from here:** Independent reviewer (different worker or human).
- **Required evidence:** Handoff written, verification report created, tests passing.
- **Next allowed states:** `done` (approved), `in-progress` (changes requested), `blocked`.

### `blocked`
- **Meaning:** Task cannot proceed due to a dependency, issue, or uncertainty.
- **Who can move here:** The implementing worker or reviewer.
- **Who can move from here:** Human (after unblocking).
- **Required evidence:** Reason for blocking documented in task file or handoff.
- **Next allowed states:** `in-progress`, `ready` (if reassigned).

### `done`
- **Meaning:** Task is verified and complete.
- **Who can move here:** Independent reviewer ONLY (NOT the implementing worker).
- **Who can move from here:** No one — this is a terminal state.
- **Required evidence:** Verification report, passing tests, approved review, handoff archived.
- **Next allowed states:** None (terminal).

## Execution Mode Notes

- **Solo mode:** One worker moves tasks through all states. The worker must not self-close to `done/` without independent verification or human approval.
- **Multi-worker mode:** Different workers may move tasks through different states. Review must be by a different worker.
- **Hybrid mode:** Primary worker handles most state transitions. Support workers handle specialized states (verification, review).

## Related Files

- [`worker-contract.md`](./worker-contract.md) — Worker obligations
- [`definition-of-done.md`](./definition-of-done.md) — Completion criteria
- [`verification-gates.md`](./verification-gates.md) — Verification checkpoints
- [`assignment-model.md`](./assignment-model.md) — Assignment hierarchy
- [`execution-modes.md`](./execution-modes.md) — Execution modes
