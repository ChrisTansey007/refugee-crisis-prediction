# worker-loop skill

> **Purpose:** Keep a worker session running continuously without human
> intervention. After every task closes, this skill drives the agent back to
> the top of the task queue. Run it at the start of any session that should
> operate autonomously.

---

## Core loop (repeat until exit condition)

```
LOOP:
  1. SCAN     → inspect tasks/ready/ for unclaimed tasks
  2. PROMOTE  → if ready/ is empty, run auto-promote skill
  3. CLAIM    → pick the highest-priority unclaimed task; write lock file
  4. LOAD     → read task file, handoff (if any), related context
  5. EXECUTE  → do the work; write verification evidence
  6. CLOSE    → run session-close skill (commit + push + handoff)
  7. GOTO LOOP

EXIT CONDITIONS (clean):
  - Human owner sets agent-os/triggers/stop-<worker>.md
  - No tasks remain after auto-promote (write idle trigger, exit)
  - Task requires a capability this worker lacks (write escalation, exit)

EXIT CONDITIONS (abrupt — always write handoff before exiting):
  - Context window approaching limit
  - Unrecoverable error after 2 retries
```

---

## Stage 1 — SCAN

```bash
ls agent-os/tasks/ready/
```

Parse each file for:
- `Current Claimed Worker` — skip if already claimed
- `Required Capabilities` — skip if this worker lacks them
- `Context Snapshot` — refresh if missing or stale before you commit to the claim
- `blocked_by` and `Dependencies` — skip if blockers are unresolved

Select the first eligible task by priority. If none, go to Stage 2.

---

## Stage 2 — PROMOTE (run auto-promote skill)

See [`auto-promote.md`](./auto-promote.md). This skill:
1. Reads all `tasks/backlog/` files.
2. Checks each task's `blocked_by` list against `tasks/done/`.
3. Moves any fully-unblocked tasks to `tasks/ready/`.
4. Returns the count of tasks promoted.

If count > 0, return to Stage 1. If count = 0, write idle trigger (Stage 7).

---

## Stage 3 — CLAIM

```bash
# Write lock file
cat > agent-os/locks/TASK-XXXX-<worker>.json << EOF
{
  "task_id": "TASK-XXXX",
  "worker": "<worker-name>",
  "claimed_at": "<ISO-8601>",
  "branch": "<branch-name>"
}
EOF

# Update task file header
# Set: status: in-progress, assigned_to: <worker>, started_at: <ISO-8601>

git add -A && git commit -m "chore(task): claim TASK-XXXX" && git push origin <branch>
```

**Why commit the claim?** Other workers watching the repo see the lock
immediately and will not double-claim.

---

## Stage 4 — LOAD

Read in this order:
1. The task file (`tasks/ready/TASK-XXXX-*.md`)
2. The most recent handoff for this task (`handoffs/active/HANDOFF-XXXX-*.md`)
3. The task's `Context Snapshot` and `Required Context Links`
4. `AGENTS.md` Rules relevant to this task type
5. `PROJECT_GOAL.md` and `PROJECT_CONTEXT.md` for scope alignment

Do not begin executing until all context is loaded.

---

## Stage 5 — EXECUTE

Follow the task's acceptance criteria exactly. Write verification evidence
to `agent-os/reports/TASK-XXXX-verification.md` as you go. If you hit a
blocker:

1. Write a blocker note to the task file.
2. Create a new `tasks/backlog/TASK-XXXX-unblock-*.md` task describing what
   is needed.
3. Run `session-close` and go to Stage 7 (idle).

---

## Stage 6 — CLOSE

Run [`session-close.md`](./session-close.md) exactly:
1. `git add -A && git commit -m "..." && git push origin <branch>`
2. Write handoff to `handoffs/active/`
3. Move task to `tasks/done/` **only after** push is confirmed
4. Remove lock file
5. Update `worker-status.json`

Then **immediately** return to Stage 1 of this loop.

---

## Stage 7 — IDLE (exit path)

Only reached when no work is available.

```bash
# Write idle trigger
cat > agent-os/triggers/idle-<worker>-<date>.md << EOF
# Idle Trigger

**Worker:** <worker-name>
**Timestamp:** <ISO-8601>
**Reason:** No claimable tasks after auto-promote sweep.

## Tasks in backlog (still blocked)
<list>

## Suggested next action for human owner
<what needs to happen to unblock — new task creation, decision, etc.>
EOF

git add -A && git commit -m "chore(worker): <worker> idle — no tasks available" && git push origin <branch>
```

Then exit the session cleanly.

---

## Priority tiebreaking

When multiple tasks share the same priority:
1. Oldest `created_at` date wins (FIFO).
2. If still tied, prefer tasks blocking the most other tasks.
3. If still tied, prefer tasks matching this worker's primary capability.

---

## Related files

- [auto-promote.md](./auto-promote.md) — backlog promotion logic
- [enrich-task.md](./enrich-task.md) — task atomicity and snapshot refresh
- [session-close.md](./session-close.md) — commit + push + handoff
- [AGENTS.md Rule 24](../../AGENTS.md) — autonomous continuation rule
- [../protocols/autonomous-continuation.md](../protocols/autonomous-continuation.md) — full protocol
- [../triggers/README.md](../triggers/README.md) — trigger protocol
