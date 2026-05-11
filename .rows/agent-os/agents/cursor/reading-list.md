# Cursor Reading List

Load these in addition to the universal index.

---

## Required (Cursor-specific)

| File | Why |
|---|---|
| `.cursor/rules/` | Confirm installed rules match `agent-os/agents/cursor/rules/` |
| `agent-os/state/worker-status.json` | Find your entry (`cursor`) and update to active |
| `agent-os/state/system-state.json` | Current phase and project context |
| `PROJECT_CONTEXT.md` | Distilled durable project context — read this before defaulting to raw handoffs |

---

## Cursor Operational Notes

- Your worker ID in `worker-status.json` is `cursor`
- Cursor rules are available natively once installed — no extra invocation needed
- Use terminal for all git operations and JSON state updates via jq
- Rule 23 (push gate): confirm push before closing any task
- Rule 24 (autonomous continuation): claim next task immediately after completing one
- Treat `Context Snapshot` as part of claim readiness, not optional garnish

---

## Cursor jq Pattern for Worker Status Update

```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.workers.cursor.status = "active" | .workers.cursor.last_active = $ts' \
  agent-os/state/worker-status.json > /tmp/ws.json \
  && mv /tmp/ws.json agent-os/state/worker-status.json
```
