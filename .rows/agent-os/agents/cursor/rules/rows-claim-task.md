---
description: Claim a ROWS task and begin work
---

# ROWS: Claim Task

Use this workflow to claim a task from `agent-os/tasks/ready/` and begin working on it.

## Steps

1. **List ready tasks**
   ```bash
   ls agent-os/tasks/ready/
   ```

2. **Choose a task** based on priority and your current branch context. Read the task file fully before claiming.

3. **Refresh context if needed**. If the task does not have a current `Context Snapshot`, run `agent-os/skills/enrich-task.md` first.

4. **Write a lock file** in `agent-os/locks/` to signal intent:
   ```bash
   cat > agent-os/locks/[TASK-ID]-cursor.json << EOF
   {
     "task_id": "[TASK-ID]",
     "claimed_by": "cursor",
     "claimed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
   }
   EOF
   ```

5. **Move task to in-progress**:
   ```bash
   mv agent-os/tasks/ready/[TASK-ID].md agent-os/tasks/claimed/[TASK-ID].md
   mv agent-os/tasks/claimed/[TASK-ID].md agent-os/tasks/in-progress/[TASK-ID].md
   ```

6. **Update task file** — set `Status` to `in-progress`, `Current Claimed Worker` to `cursor`, and refresh `Snapshot Freshness` if you enriched it.

7. **Update worker status**:
   ```bash
   jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg task "[TASK-ID]" \
     '.workers.cursor.status = "active" | .workers.cursor.current_task = $task | .workers.cursor.last_active = $ts' \
     agent-os/state/worker-status.json > /tmp/ws.json \
     && mv /tmp/ws.json agent-os/state/worker-status.json
   ```

8. **Commit and push**:
   ```bash
   git add agent-os/tasks/in-progress/[TASK-ID].md agent-os/state/worker-status.json
   git commit -m "chore(agent-os): claim [TASK-ID]"
   git push
   ```

9. **Begin work** on the task.
