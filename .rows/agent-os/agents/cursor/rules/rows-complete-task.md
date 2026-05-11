---
description: Complete a ROWS task, verify push, and move to done
---

# ROWS: Complete Task

Use this workflow when your work on a task is finished and you are ready to close it.

## Steps

1. **Run final checks** — all tests pass, lint clean, no console errors

2. **Commit your work**:
   ```bash
   git add -A
   git commit -m "type(scope): description closes TASK-ID"
   ```

3. **Push** (Rule 23 — push gate):
   ```bash
   git push
   ```

4. **Verify push confirmed** (Rule 23 — do not skip):
   ```bash
   BRANCH=$(git branch --show-current)
   git ls-remote origin $BRANCH | grep $BRANCH && echo "PUSH CONFIRMED" || echo "PUSH FAILED"
   ```
   If `PUSH FAILED`: re-run `git push` before continuing.

5. **Move task to done**:
   ```bash
   mv agent-os/tasks/in-progress/[TASK-ID].md agent-os/tasks/done/[TASK-ID].md
   ```

6. **Update task file** — set `status: done`, `completed_at: [timestamp]`

7. **Update worker status**:
   ```bash
   jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.workers.cursor.status = "idle" | .workers.cursor.current_task = null | .workers.cursor.last_active = $ts' \
     agent-os/state/worker-status.json > /tmp/ws.json \
     && mv /tmp/ws.json agent-os/state/worker-status.json
   ```

8. **Commit state files**:
   ```bash
   git add agent-os/tasks/done/[TASK-ID].md agent-os/state/worker-status.json
   git commit -m "chore(agent-os): complete [TASK-ID]"
   git push
   ```

9. **Claim next task** (Rule 24 — autonomous continuation):
   Run the `ROWS: Claim Task` workflow immediately.
