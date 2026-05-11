# Active Handoffs

This folder contains handoffs from **active or recently completed sessions**.

## Purpose

Active handoffs are the primary mechanism for continuity between worker sessions. Any worker picking up a task should read the most recent handoff for that task.

## What Belongs Here

- Handoffs from worker sessions that are still in progress.
- Handoffs from completed sessions awaiting review.
- Handoffs from blocked sessions.

## How Handoffs Leave Here

- **Archived:** When a task moves to `done/`, its handoffs move to [`../archive/`](../archive/).
- **Superseded:** When a new handoff for the same task is written, old handoffs can be archived.

## Naming Convention

`[TASK-ID]-[worker]-[YYYY-MM-DD].md`

Example: `TASK-0003-codex-2026-05-07.md`

## Related Files

- [`../handoff-template.md`](../handoff-template.md) — Handoff template
- [`../archive/`](../archive/) — Archived handoffs
