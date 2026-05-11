# Audit Reports

System audit findings and reports.

## Purpose

Audit reports document the results of regular system health checks. They identify issues like stale locks, malformed tasks, incomplete handoffs, or process violations.

## What Goes Here

- Task queue audit results.
- Handoff quality audit results.
- Lock audit results (stale locks, missing locks).
- Process compliance audit results.

## Naming

`audit-[type]-[YYYY-MM-DD].md`

## Related Files

- [`../../schedules/audits.md`](../../schedules/audits.md) — Audit schedule
- [`../../escalation-rules.md`](../../escalation-rules.md) — When to escalate findings
