# Status Reports

Generated system status reports.

## Purpose

Status reports provide a snapshot of the ROWS system at a point in time. They summarize active tasks, worker status, blockers, and overall project health.

## Generation

Run `npm run status:generate` to create a new status report. Reports are named `status-[YYYY-MM-DD].md`, and the same run refreshes the root `STATUS.md` dashboard.

## Contents

Each report includes:
- Active task count by lifecycle state
- Worker status summary
- Recent handoffs
- Blocked tasks
- Stale locks
- Risk summary

## Related Files

- [`../../schedules/daily.md`](../../schedules/daily.md) — Daily report schedule
- [`../../state/system-state.json`](../../state/system-state.json) — System state
- [`../../../STATUS.md`](../../../STATUS.md) — Root dashboard generated from the same data
