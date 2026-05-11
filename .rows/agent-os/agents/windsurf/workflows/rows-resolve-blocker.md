---
description: Resume a blocked ROWS task after a blocker has been resolved
---

# ROWS: Resolve Blocker

Use this workflow when a task in `agent-os/tasks/blocked/` has had its blocker cleared (either by auto-deadline resolution, human override, or manual resolution).

## Steps

1. **Find the blocker record** — read the task file in `agent-os/tasks/blocked/` and note the `blocker_id`

2. **Read the blocker record** at `agent-os/blockers/[BLOCKER-ID].md` — understand what was decided

3. **Check the decision register** if a human_decision was involved:
   ```bash
   cat docs/05-decisions/decision-register.md | grep -A5 "[BLOCKER-ID]"
   ```

4. **Load the decision into your context** before writing any code — this is the answer to what was blocking you

5. **Move task from blocked to in-progress**:
   ```bash
   mv agent-os/tasks/blocked/[TASK-ID].md agent-os/tasks/in-progress/[TASK-ID].md
   ```

6. **Clear blocker fields in task file** — set `blocker_id: ~`, `blocker_type: ~`, add `blocker_resolution: [summary]` and `blocker_resolved_at: [timestamp]`

7. **Update worker status**:
   ```bash
   jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg task "[TASK-ID]" \
     '.workers.windsurf.status = "active" | .workers.windsurf.current_task = $task | .workers.windsurf.last_active = $ts' \
     agent-os/state/worker-status.json > /tmp/ws.json \
     && mv /tmp/ws.json agent-os/state/worker-status.json
   ```

8. **Commit**:
   ```bash
   git add -A
   git commit -m "chore(agent-os): resolve [BLOCKER-ID] — resume [TASK-ID]"
   git push
   ```

9. **Continue work** on the task.
