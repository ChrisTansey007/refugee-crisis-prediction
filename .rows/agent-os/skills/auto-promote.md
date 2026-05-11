# auto-promote skill

> **Purpose:** Scan `tasks/backlog/` and move any fully-unblocked task to
> `tasks/ready/`. Run this skill whenever `tasks/ready/` is empty, or at the
> start of a new session to catch tasks whose blockers resolved while the
> worker was away.

---

## Algorithm

```
FOR EACH task file in tasks/backlog/:
  1. Parse the task's `blocked_by` list and `Dependencies` section
  2. Confirm the task has a `Context Snapshot` before it can become claimable
  3. FOR EACH blocker in blocked_by / Dependencies:
       CHECK whether tasks/done/<blocker>-*.md exists
       IF NOT found → task stays in backlog (still blocked)
  4. IF all blockers resolved (or list is empty):
       MOVE task file → tasks/ready/
       LOG promotion to agent-os/reports/promotion-log.md
       COMMIT + PUSH the move
```

---

## Execution steps

### Step 1 — read the backlog

```bash
ls agent-os/tasks/backlog/
```

For each `.md` file, read:
- `blocked_by`
- `Dependencies`
- `Required Capabilities`
- `Context Snapshot`

### Step 2 — check blockers

```bash
ls agent-os/tasks/done/ | grep "TASK-XXXX"
```

A blocker is resolved when its task file exists anywhere under `tasks/done/`.

### Step 3 — promote

```bash
mv agent-os/tasks/backlog/TASK-XXXX-*.md agent-os/tasks/ready/
```

Append a promotion record to `agent-os/reports/promotion-log.md`:
```
[<ISO-8601>] TASK-XXXX promoted: backlog → ready (all blockers resolved)
```

### Step 4 — commit and push

```bash
git add -A
git commit -m "chore(tasks): promote TASK-XXXX to ready"
git push origin <branch>
```

**Push is required** so other workers see the newly-ready tasks.

---

## When to run

| Trigger | Who runs it |
|---|---|
| `tasks/ready/` is empty during `worker-loop` Stage 2 | Current worker (automatic) |
| A task moves to `done/` | The closing worker (automatic, part of session-close) |
| GitHub Actions `on-task-done.yml` | CI (automatic on push) |
| Human owner requests sweep | Any available worker |

---

## Promotion log format

File: `agent-os/reports/promotion-log.md`

```markdown
# Task Promotion Log

| Timestamp | Task ID | Promoted by | Blockers resolved |
|---|---|---|---|
| 2026-05-07T14:00:00Z | TASK-0005 | claude-session-42 | TASK-0004 |
```

---

## Edge cases

- **Circular dependencies:** If TASK-A blocks TASK-B and TASK-B blocks TASK-A,
  neither will ever promote. Write an escalation to `agent-os/escalations/`
  and notify the human owner.
- **Missing blocker task file:** If a listed blocker ID does not exist anywhere
  in `tasks/`, treat it as resolved (the task may have been removed).
- **Missing context snapshot:** Do not promote until `enrich-task` has filled it in.
- **No backlog tasks:** Return 0 promoted, trigger idle state in `worker-loop`.

---

## Related files

- [worker-loop.md](./worker-loop.md) — calls this skill at Stage 2
- [../task-lifecycle.md](../task-lifecycle.md) — task state machine
- [../reports/promotion-log.md](../reports/promotion-log.md) — promotion history
