# Skill: Self-Install

**When to use:** At the start of any session in a ROWS repo, immediately after reading `BOOTSTRAP.md`.

This skill installs ROWS operational knowledge into you — either by copying files to platform-native locations (if you can write files) or by loading a structured reading list into your context (if you are session-based or read-only).

---

## Stage 1 — Confirm Your Agent Type

You should already know your type from `BOOTSTRAP.md`. Confirm it here by checking `agent-os/agents/registry.md` if needed.

Proceed to the branch that matches your type.

---

## Branch A — File-Writing Agents (Windsurf, Cursor, Codex)

These agents have a native skill-loading mechanism. The goal is to get ROWS skill files into the locations your platform reads automatically.

### A1 — Check What Is Already Installed

```bash
# Windsurf
ls .windsurf/workflows/ 2>/dev/null || echo "Not yet installed"

# Cursor
ls .cursor/rules/ 2>/dev/null || echo "Not yet installed"

# Codex
ls .codex/ 2>/dev/null || echo "Not yet installed"
```

If ROWS files are already present (e.g., from a prior session), skip to A3.

### A2 — Copy Platform Skills Into Place

Run the install script for your agent type:

**Windsurf:**
```bash
mkdir -p .windsurf/workflows
cp agent-os/agents/windsurf/workflows/*.md .windsurf/workflows/
echo "Windsurf ROWS workflows installed."
```

**Cursor:**
```bash
mkdir -p .cursor/rules
cp agent-os/agents/cursor/rules/*.md .cursor/rules/
echo "Cursor ROWS rules installed."
```

**Codex:**
```bash
# Codex reads .codex/README.md at startup — it is already in the repo.
# No copy needed. Verify it exists:
cat .codex/README.md | head -5
echo "Codex startup file confirmed."
```

### A3 — Load Your Reading List Into Context

Even file-writing agents need context. Read your agent-specific reading list now:

```
agent-os/agents/[your-type]/reading-list.md
```

Load every **Required** item into your active context.

### A4 — Load Universal Index

Read `agent-os/agents/universal/index.md` and load all **Required** items from Phase 0, 1, and 2.

### A5 — Confirm and Proceed

Log completion to your session notes or handoff:

```
Self-install complete: [agent-type], [timestamp]
Platform skills: installed to [location]
Universal required skills: loaded
```

Proceed to `AGENTS.md`.

---

## Branch B — Session-Based / Read-Only Agents (Claude, generic)

These agents cannot persist files between sessions. Knowledge injection happens entirely through reading.

### B1 — Load Your Reading List

Read your agent-specific reading list:

```
agent-os/agents/[your-type]/reading-list.md
```

This list is ordered. Work through it top to bottom. Do not skip **Required** items.

### B2 — Load Universal Index (Phase 0, 1, 2)

Read `agent-os/agents/universal/index.md`.

Load every **Required** item from Phase 0, Phase 1, and Phase 2 into your context now. This is not optional — these files contain the rules and protocols you will need for every action you take in this repo.

### B3 — Load Conditional Items Based on Work Ahead

Scan Phase 3 of the universal index. Load any Conditional items that match your current situation:

- About to pick a task? → load `agent-os/tasks/backlog/`
- Resuming mid-project? → load `agent-os/handoffs/` (most recent file)
- Making architectural choices? → load `docs/01-architecture/` and `docs/05-decisions/decision-register.md`

### B4 — Confirm and Proceed

Mentally confirm you have loaded:
- [ ] `AGENTS.md`
- [ ] `agent-os/state/system-state.json`
- [ ] `agent-os/state/worker-status.json`
- [ ] `agent-os/state/assignment-state.json`
- [ ] `PROJECT_GOAL.md`
- [ ] `agent-os/tasks/task-template.md`
- [ ] `agent-os/skills/claim-task.md`
- [ ] `agent-os/skills/complete-task.md`
- [ ] `agent-os/skills/session-close.md`
- [ ] `agent-os/protocols/blocker-protocol.md`
- [ ] `agent-os/skills/escalate-blocker.md`
- [ ] `agent-os/skills/resolve-blocker.md`

If any item is missing, load it now before proceeding.

Proceed to AGENTS.md → startup sequence.

---

## What Self-Install Does Not Do

- It does not claim a task (that happens after AGENTS.md startup sequence)
- It does not modify any state files
- It does not create branches or commits
- It does not replace re-reading AGENTS.md — you still read AGENTS.md after this

Self-install is knowledge injection only. Work starts after.
