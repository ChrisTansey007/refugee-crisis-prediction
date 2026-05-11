# Generic Reading List

Load these in addition to the universal index.

---

## Required

| File | Why |
|---|---|
| `agent-os/state/worker-status.json` | Find or create your worker entry |
| `agent-os/state/system-state.json` | Current phase and project context |
| `agent-os/agents/registry.md` | Understand what other agents are active and their capabilities |
| `PROJECT_CONTEXT.md` | Distilled durable context so you do not have to reconstruct history from raw handoffs |

---

## Operational Notes for Generic Agents

- Your worker ID in `worker-status.json` should be something unique to your agent type
- If you cannot determine what to use as a worker ID, use `agent-[timestamp]` as a temporary ID
- If you cannot write files, narrate your intended state changes so they can be applied by others
- All ROWS rules still apply to you — Rule 23 (push gate), Rule 24 (autonomous continuation), Rule 25/26 (blocker handling)
- When in doubt about how to do something, look at how other agents do it in `agent-os/agents/[windsurf|codex|claude]/`
