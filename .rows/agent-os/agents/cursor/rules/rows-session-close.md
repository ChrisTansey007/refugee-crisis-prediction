---
description: Close a ROWS work session cleanly with a handoff
---

# ROWS: Session Close

Use this workflow when ending a work session. Always close cleanly — never abandon mid-task without a handoff.

## Steps

1. **Commit all in-progress work** even if incomplete:
   ```bash
   git add -A
   git commit -m "wip([scope]): [what you did] — session close"
   git push
   ```

2. **Verify push**:
   ```bash
   BRANCH=$(git branch --show-current)
   git ls-remote origin $BRANCH | grep $BRANCH && echo "CONFIRMED" || echo "FAILED — push again"
   ```

3. **Write a handoff file** at `agent-os/handoffs/YYYY-MM-DD-cursor-[TASK-ID].md`:
   ```markdown
   # Handoff — [DATE]
   
   **Agent:** cursor
   **Task:** [TASK-ID] — [task title]
   **Status:** [what is done / what remains]
   
   ## What I Did
   [Summary of work completed]
   
   ## What Is Left
   [Specific remaining steps]
   
   ## Decisions Made
   [Any decisions you made that the next agent needs to know about]
   
   ## Watch Out For
   [Any gotchas, blockers, or context the next agent needs]
   
   ## Next Action
   [Exact first step the next agent should take]
   ```

4. **Update worker status** to idle:
   ```bash
   jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '.workers.cursor.status = "idle" | .workers.cursor.last_active = $ts' \
     agent-os/state/worker-status.json > /tmp/ws.json \
     && mv /tmp/ws.json agent-os/state/worker-status.json
   ```

5. **Commit handoff**:
   ```bash
   git add agent-os/handoffs/ agent-os/state/worker-status.json
   git commit -m "chore(agent-os): session close — cursor handoff"
   git push
   ```

Session closed.
