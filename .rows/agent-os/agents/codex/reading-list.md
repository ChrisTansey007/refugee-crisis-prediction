# Codex Reading List

Load these in addition to the universal index.

---

## Required (Codex-specific)

| File | Why |
|---|---|
| `.codex/README.md` | Your startup instructions — should already be loaded |
| `agent-os/state/worker-status.json` | Find your entry (`codex`) and confirm or update it |
| `agent-os/state/system-state.json` | Current phase and project context |
| `PROJECT_CONTEXT.md` | Distilled durable repo context — prefer this before scanning raw handoffs |

---

## Codex Operational Notes

- Your worker ID in `worker-status.json` is `codex`
- You work on a specific branch defined in `.codex/README.md` — do not switch branches without a task that requires it
- Use `jq` for all JSON state updates — never hand-edit state files
- Rule 23 (push gate): confirm push with `git ls-remote origin [branch] | grep [branch]` before closing any task
- Rule 24 (autonomous continuation): when a task completes, immediately claim and begin the next ready task
- Treat `Context Snapshot` in task files as the first-stop task briefing; refresh it when stale

---

## Codex jq Pattern for Worker Status Update

```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.workers.codex.status = "active" | .workers.codex.last_active = $ts' \
  agent-os/state/worker-status.json > /tmp/ws.json \
  && mv /tmp/ws.json agent-os/state/worker-status.json
```
