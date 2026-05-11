# Blocked

Tasks in this folder **cannot proceed** due to a dependency, issue, or uncertainty.

## Who Can Add Tasks Here

- The implementing worker (if blocked during implementation).
- The reviewer (if issues found during review cannot be resolved by the worker).

## What Belongs Here

- Tasks blocked by unfinished dependencies.
- Tasks blocked by missing information or unclear requirements.
- Tasks blocked by technical issues that need human intervention.

## How Tasks Leave Here

- **Unblocked:** Human moves the task back to [`../in-progress/`](../in-progress/) or [`../ready/`](../ready/).
- **Cancelled:** Human deletes the task or moves it out.

## Rules

- The reason for blocking MUST be documented in the task file or handoff.
- Only the human can unblock a task.
- Workers should not modify blocked tasks without human direction.
- Blocked tasks should be reviewed regularly (see [`../../schedules/audits.md`](../../schedules/audits.md)).

## Related Files

- [`../../escalation-rules.md`](../../escalation-rules.md) — When to escalate
- [`../../schedules/audits.md`](../../schedules/audits.md) — Audit schedule
