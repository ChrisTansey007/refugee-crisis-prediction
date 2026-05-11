# Claude Self-Install

You are Claude (Anthropic). You are session-based — you cannot persist files between conversations. Your installation is entirely context-loading. Every session, you reload.

This is not a limitation — it means your install is always fresh and never stale.

---

## Step 1 — Load Your Reading List

Read `agent-os/agents/claude/reading-list.md` now.

Work through it top to bottom. Every **Required** item must be in your active context before you proceed.

---

## Step 2 — Load Universal Index

Read `agent-os/agents/universal/index.md`.

Load every **Required** item from Phase 0, Phase 1, and Phase 2.

---

## Step 3 — Load Conditional Items

From Phase 3 of the universal index, load items that match your current session:

- **New to this repo?** → load `agent-os/handoffs/` (most recent file) for project history
- **About to choose a task?** → scan `agent-os/tasks/backlog/`
- **Resuming claimed work?** → load your task file from `agent-os/tasks/in-progress/`
- **Making architecture decisions?** → load `docs/01-architecture/` and `docs/05-decisions/decision-register.md`

---

## Step 4 — Check Your Worker Entry

Read `agent-os/state/worker-status.json` and find the `claude` entry. Note:

- Your current status (should update to `active`)
- Any tasks noted as in-progress from prior sessions
- Handoff notes

If you are running in Claude Code (or another environment with file write access), update your status using the jq pattern in your reading list.

If you are in a read-only context, note your active status in your working memory for this session.

---

## Step 5 — Confirm Loaded

Mentally confirm you have all required context:

- [ ] `AGENTS.md` — full ruleset
- [ ] `agent-os/state/system-state.json` — project phase and name
- [ ] `agent-os/state/worker-status.json` — who is active
- [ ] `agent-os/state/assignment-state.json` — how work is assigned
- [ ] `PROJECT_GOAL.md` — north star
- [ ] `agent-os/tasks/task-template.md` — task format
- [ ] `agent-os/skills/claim-task.md` — claim procedure
- [ ] `agent-os/skills/complete-task.md` — close procedure
- [ ] `agent-os/skills/session-close.md` — session end procedure
- [ ] `agent-os/protocols/blocker-protocol.md` — blocker resolution
- [ ] `agent-os/skills/escalate-blocker.md` — how to file a blocker
- [ ] `agent-os/skills/resolve-blocker.md` — how to resume after blocker

---

## Step 6 — Done

Proceed to `AGENTS.md` startup sequence.

> **Session note:** Because you reload every session, if a project already has prior history, always check `agent-os/handoffs/` for the most recent handoff before touching any task. Prior agents leave context there specifically for you.
