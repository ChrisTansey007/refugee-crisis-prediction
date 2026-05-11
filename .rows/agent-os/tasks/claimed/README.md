# Claimed

Tasks in this folder have been **claimed by a worker** and a lock has been created.

## Who Can Add Tasks Here

- The claiming worker (by moving from `ready/`).

## What Belongs Here

- Tasks that a worker has formally claimed.
- A corresponding lock file MUST exist in [`../../locks/`](../../locks/).

## How Tasks Leave Here

- **Work begins:** Worker moves the task to [`../in-progress/`](../in-progress/).
- **Released:** Worker moves the task back to [`../ready/`](../ready/) and removes the lock.

## Rules

- A lock file is REQUIRED before a task enters this state.
- The worker must update [`../../state/worker-status.json`](../../state/worker-status.json).
- Tasks should not stay in `claimed/` for long — move to `in-progress/` promptly.

## Related Files

- [`../../locks/lock-template.json`](../../locks/lock-template.json) — Lock template
- [`../../worker-contract.md`](../../worker-contract.md) — Claiming process
