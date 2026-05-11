---
description: File a ROWS blocker when a task cannot proceed
---

# ROWS: Escalate Blocker

Use this workflow when a task is blocked and you have exhausted Tier 1 (resolve from context) and Tier 2 (assume and flag) options from `agent-os/protocols/blocker-protocol.md`.

## Steps

1. **Confirm you have tried Tier 1 and Tier 2** — re-read `agent-os/protocols/blocker-protocol.md` if unsure

2. **Determine blocker type**: `dependency` | `external` | `human_decision` | `capability` | `environment`

3. **Determine severity and deadline**:
   - trivial → 5 min | low → 15 min | moderate → 30 min | high → 60 min | critical → 24h

4. **Get next blocker ID**:
   ```bash
   ls agent-os/blockers/ | grep "^BLOCKER-" | sort | tail -1
   # Increment the number for your new blocker
   ```

5. **Write blocker record** using template at `agent-os/blockers/blocker-template.md`

6. **Calculate resolve_at**:
   ```bash
   # Example: 30 minute deadline
   date -u -d "+30 minutes" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || \
   date -u -v+30M +%Y-%m-%dT%H:%M:%SZ
   ```

7. **Update task file** — add blocker fields (blocker_id, blocker_type, blocker_resolved_at)

8. **Move task to blocked**:
   ```bash
   mv agent-os/tasks/in-progress/[TASK-ID].md agent-os/tasks/blocked/[TASK-ID].md
   ```

9. **Write trigger file** if human decision needed (see `agent-os/triggers/README.md`)

10. **Update worker status** to idle and commit everything:
    ```bash
    jq '.workers.windsurf.status = "idle" | .workers.windsurf.current_task = null' \
      agent-os/state/worker-status.json > /tmp/ws.json \
      && mv /tmp/ws.json agent-os/state/worker-status.json
    git add -A
    git commit -m "chore(agent-os): block [TASK-ID] — [BLOCKER-ID]"
    git push
    ```

11. **Claim next ready task** (Rule 24 — never stop silently):
    Run `ROWS: Claim Task` immediately.
