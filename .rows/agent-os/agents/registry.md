# Agent Registry

This file maps agent types to their capabilities, resource paths, and identification signals.

If you are unsure which type you are, use the signals table to self-identify.

---

## Agent Types

### `windsurf`
- **Platform:** Windsurf IDE (Cascade AI)
- **Can write files:** Yes
- **Native skill location:** `.windsurf/workflows/`
- **Resources:** `agent-os/agents/windsurf/`
- **Identification signals:** You have access to Cascade tools, you can run terminal commands and write files, you see `.windsurf/` in the repo root

### `codex`
- **Platform:** OpenAI Codex (codex-1 or similar)
- **Can write files:** Yes (via shell/container)
- **Native skill location:** `.codex/` (startup instructions)
- **Resources:** `agent-os/agents/codex/`
- **Identification signals:** You are running inside a Codex sandbox, you have shell access, your startup file is `.codex/README.md`

### `claude`
- **Platform:** Anthropic Claude (any version)
- **Can write files:** Session-dependent (Claude Code: yes; Claude.ai chat: no)
- **Native skill location:** N/A — context-loaded
- **Resources:** `agent-os/agents/claude/`
- **Identification signals:** You are Claude, you received this repo via a prompt or attachment

### `cursor`
- **Platform:** Cursor IDE
- **Can write files:** Yes
- **Native skill location:** `.cursor/rules/`
- **Resources:** `agent-os/agents/cursor/`
- **Identification signals:** You are running in Cursor, you see `.cursor/` in the repo root

### `generic`
- **Platform:** Any unrecognized agent
- **Can write files:** Unknown — check your own capabilities
- **Native skill location:** N/A
- **Resources:** `agent-os/agents/generic/`
- **Identification signals:** You do not match any of the above

---

## Capability Flags

| Agent | can_write_files | has_shell | has_native_skill_loader | session_based |
|---|---|---|---|---|
| windsurf | ✅ | ✅ | ✅ (.windsurf/workflows) | ❌ |
| codex | ✅ | ✅ | ✅ (.codex/README.md) | ❌ |
| claude | ⚠️ varies | ⚠️ varies | ❌ | ✅ |
| cursor | ✅ | ✅ | ✅ (.cursor/rules) | ❌ |
| generic | ❓ | ❓ | ❓ | ❓ |

---

## Resource Path Map

| Agent | Install Guide | Reading List | Platform Skills |
|---|---|---|---|
| windsurf | `agent-os/agents/windsurf/install.md` | `agent-os/agents/windsurf/reading-list.md` | `agent-os/agents/windsurf/workflows/` |
| codex | `agent-os/agents/codex/install.md` | `agent-os/agents/codex/reading-list.md` | `agent-os/agents/codex/startup/` |
| claude | `agent-os/agents/claude/install.md` | `agent-os/agents/claude/reading-list.md` | N/A |
| cursor | `agent-os/agents/cursor/install.md` | `agent-os/agents/cursor/reading-list.md` | `agent-os/agents/cursor/rules/` |
| generic | `agent-os/agents/generic/install.md` | `agent-os/agents/generic/reading-list.md` | N/A |

---

## Universal Resources (all agents)

| Resource | Path | Purpose |
|---|---|---|
| Skills index | `agent-os/agents/universal/index.md` | All ROWS skills, required vs optional |
| ROWS ruleset | `AGENTS.md` | Complete rules, read after bootstrap |
| Blocker protocol | `agent-os/protocols/blocker-protocol.md` | How to handle blockers |
| Task template | `agent-os/tasks/task-template.md` | Task file format |
| Session close | `agent-os/skills/session-close.md` | How to close a work session cleanly |
