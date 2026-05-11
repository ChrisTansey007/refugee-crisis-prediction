# Done

Tasks in this folder are **verified and complete**.

## Who Can Add Tasks Here

- Independent reviewer ONLY (NOT the implementing worker).

## What Belongs Here

- Tasks that have passed all verification gates.
- Tasks with completed handoffs (archived in [`../../handoffs/archive/`](../../handoffs/archive/)).
- Tasks with removed lock files.

## How Tasks Leave Here

- Tasks do NOT leave this folder. This is a terminal state.

## Rules

- This is the only terminal state in the lifecycle.
- The implementing worker CANNOT move their own task here. This is a hard rule.
- The lock file must be removed when the task enters `done/`.
- The handoff must be archived.

## Related Files

- [`../../definition-of-done.md`](../../definition-of-done.md) — Completion criteria
- [`../../verification-gates.md`](../../verification-gates.md) — Verification process
