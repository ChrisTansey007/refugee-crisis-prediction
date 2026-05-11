# Claude Reading List

Load these in addition to the universal index. Claude-specific context for operating ROWS effectively.

---

## Required (Claude-specific)

| File | Why |
|---|---|
| `agent-os/state/worker-status.json` | Find the `claude` entry — your current assignments and last active time |
| `agent-os/state/system-state.json` | Project name, current phase, active sprint goals |
| `PROJECT_CONTEXT.md` | Distilled durable project context — prefer this before raw handoffs |

---

## Claude Operational Notes

**Context window management:**
- You have a finite context window. Prioritize Required files, load Conditional files only as needed.
- When context gets long, write a handoff file (`agent-os/handoffs/`) before the session ends — it is your memory for next time.
- Never hold everything in memory. Write decisions to `docs/05-decisions/decision-register.md`.

**State updates:**
- If running in Claude Code or another write-capable environment: use the jq pattern below to update `worker-status.json`.
- If running as a read-only assistant: narrate your intended state changes so a human or file-writing agent can apply them, or commit them at your next write-capable opportunity.

**Handoff discipline:**
- Always write a handoff at session end using `agent-os/skills/session-close.md`
- The handoff is your primary persistence mechanism across sessions
- Once handoffs become durable project knowledge, distill them into `PROJECT_CONTEXT.md`

**Rule 24 (autonomous continuation):**
- When a task is complete, immediately claim the next ready task
- Do not end a session with work still in your task file unless you are explicitly stopping

---

## Claude jq Pattern (if write-capable)

```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.workers.claude.status = "active" | .workers.claude.last_active = $ts' \
  agent-os/state/worker-status.json > /tmp/ws.json \
  && mv /tmp/ws.json agent-os/state/worker-status.json
```
