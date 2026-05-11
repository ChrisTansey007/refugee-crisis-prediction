# Windsurf Reading List

Load these in addition to the universal index. Windsurf-specific context that helps you operate ROWS without confusion.

---

## Required (Windsurf-specific)

| File | Why |
|---|---|
| `.windsurf/workflows/` | Confirm your installed workflows match what is in `agent-os/agents/windsurf/workflows/` |
| `agent-os/state/worker-status.json` | Find your entry (`windsurf`) — update it to active when you begin |
| `agent-os/state/system-state.json` | Confirm current phase and project name |
| `PROJECT_CONTEXT.md` | Distilled durable repo context — use this before chasing handoff history |

---

## Windsurf Operational Notes

- Your worker ID in `worker-status.json` is `windsurf`
- When updating worker status, use `jq` via terminal — do not hand-edit JSON
- Windsurf workflows are available via the Cascade workflow menu once installed
- You have terminal access — use it for git operations (push, status, ls-remote)
- Rule 23 (push gate): never close a task until `git ls-remote` confirms your branch is pushed
- Rule 24 (autonomous continuation): when a task is done, claim the next one without waiting
- Refresh a task's `Context Snapshot` before claiming if it is stale or missing

---

## Windsurf jq Pattern for Worker Status Update

```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.workers.windsurf.status = "active" | .workers.windsurf.last_active = $ts' \
  agent-os/state/worker-status.json > /tmp/ws.json \
  && mv /tmp/ws.json agent-os/state/worker-status.json
```
