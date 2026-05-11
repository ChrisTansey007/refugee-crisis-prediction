# Review

Tasks in this folder are **awaiting independent verification**.

## Who Can Add Tasks Here

- The implementing worker (after completing work and writing handoff).

## What Belongs Here

- Tasks with completed implementation, handoff, and verification evidence.
- Tasks that need a DIFFERENT worker or human to verify.

## How Tasks Leave Here

- **Approved:** Independent reviewer moves the task to [`../done/`](../done/).
- **Changes requested:** Reviewer moves the task back to [`../in-progress/`](../in-progress/).
- **Blocked:** Reviewer moves the task to [`../blocked/`](../blocked/) if issues cannot be resolved by the implementing worker.

## Rules

- The reviewer MUST be different from the implementing worker.
- The reviewer must independently verify acceptance criteria.
- The reviewer must check that handoff and evidence are complete.
- Run `npm run check:dod` before approving.

## Related Files

- [`../../verification-gates.md`](../../verification-gates.md) — Verification process
- [`../../definition-of-done.md`](../../definition-of-done.md) — Completion criteria
