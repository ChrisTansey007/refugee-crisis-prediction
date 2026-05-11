# session-close skill

> **Purpose:** Enforce the push gate (Rule 23) and produce a clean handoff at
> the end of every working session.  Run this skill before ending any session
> that touched task files, application code, or ROWS config.

---

## When to run

- You are about to hit a context limit and need to hand off to another agent.
- You have finished the work described in your current task(s).
- You are switching focus and another agent (or a future session) will
  continue.
- A human owner asks you to "wrap up" or "push and hand off".

---

## Workflow

### Stage 1 — Verify local state

```bash
# Confirm you are on the correct branch (not main/master)
git branch --show-current

# List all modified / untracked files
git status --short
```

If you are on `main`, stop and create a feature branch first:
```bash
git checkout -b feat/<task-slug>
```

---

### Stage 2 — Stage and commit

```bash
git add -A
git status --short   # review staged files one last time
git commit -m "type(scope): imperative description of work done"
```

Commit message rules (from AGENTS.md Rule 5):
- `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`
- Scope = component or area affected (e.g., `src/app`, `agent-os`)
- Description: imperative, ≤72 chars, no trailing period

---

### Stage 3 — Push to origin *(Rule 23 gate)*

```bash
git push origin <branch-name>
```

Verify the push succeeded:
```bash
git ls-remote --heads origin <branch-name>
```

If the branch name appears in the output, the push is confirmed.
**Do not advance to Stage 4 until this command returns the branch.**

---


---

### Stage 3b — Write NEXT_TASK.md *(required at every session end)*

After pushing, write `NEXT_TASK.md` to the repo root. This file is the
**single most important handoff artifact** — it tells the next session
exactly what to do in the first 30 seconds, with zero reading required.

```markdown
# NEXT_TASK

> Read this first. Run the command at the bottom to continue immediately.

**Last session:** <ISO-8601>
**Worker:** <your-name>
**Branch:** <branch>
**Push confirmed:** yes

## What was just finished

<One sentence — "Completed TASK-XXXX: [title]">

## What to do next

<Numbered list of 3-5 actions, specific enough to paste into a terminal>

## Ready tasks (claimable now)

<List from agent-os/tasks/ready/ — or "none, run auto-promote first">

## One-liner to continue

```bash
cd rows-template && cat agent-os/tasks/ready/<next-task>.md
```
```

Commit and push `NEXT_TASK.md` as part of the session-close commit.

### Stage 4 — Write the handoff file

Create `agent-os/handoffs/active/HANDOFF-<TASK-ID>-<date>.md`:

```markdown
# Handoff — <TASK-ID>: <Task Title>

**Session closed:** <ISO-8601 datetime>
**Worker:** <your agent name>
**Branch:** <branch-name>
**Pushed:** yes — confirmed via `git ls-remote`

## Work completed this session

<Bullet list of what was done — concrete, verifiable>

## Current state

<Describe exactly where the code/files are right now — what works, what
doesn't, what is partial>

## Next steps for the continuing agent

<Numbered list of the next actions, specific enough to execute without
re-reading this conversation>

## Files changed

<List of files added/modified/deleted in this session>

## Known issues / blockers

<Anything the next worker needs to know before continuing>
```

---

### Stage 5 — Move task files (if closing a task)

Only move a task to `done/` if ALL of the following are true:
- [ ] Push confirmed (Stage 3)
- [ ] Handoff written (Stage 4)
- [ ] Independent reviewer has verified (or human owner has approved)

```bash
mv agent-os/tasks/in-progress/TASK-XXXX-*.md agent-os/tasks/done/
rm agent-os/locks/TASK-XXXX.lock   # if a lock file exists
```

If the task is NOT fully done, leave it in `in-progress/` and note progress
in the handoff.

---

### Stage 6 — Update worker status

Edit `agent-os/state/worker-status.json`:
- Set your worker entry `status` to `"idle"` (or remove it if ephemeral).
- Record `last_push` timestamp.
- Record `branch` pushed.

---

## Quick-reference checklist

```
[ ] On correct feature branch (not main)
[ ] git add -A
[ ] git commit -m "type(scope): description"
[ ] git push origin <branch>
[ ] git ls-remote --heads origin <branch>  → branch appears
[ ] Handoff file written in handoffs/active/
[ ] Task moved to done/ ONLY after push confirmed
[ ] Lock file removed
[ ] worker-status.json updated
```

---

## Related rules and files

- [AGENTS.md Rule 23](../../AGENTS.md) — Push gate
- [before-commit.md](../checklists/before-commit.md) — Pre-commit checklist
- [task-closeout.md](../checklists/task-closeout.md) — Task closeout checklist
- [handoff-template.md](../handoffs/handoff-template.md) — Handoff format
- [task-lifecycle.md](../task-lifecycle.md) — Task state machine
