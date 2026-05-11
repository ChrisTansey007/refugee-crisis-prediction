# Codex Self-Install

You are OpenAI Codex (codex-1 or similar). You have shell access and file write access inside your sandbox. ROWS startup instructions are loaded via `.codex/README.md`, which Codex reads at session start.

---

## Step 1 — Confirm Startup File Was Loaded

`.codex/README.md` should have been read automatically at session start. Verify you have already processed its contents by checking if you know:

- The project name (from `system-state.json`)
- Your worker ID (should be `codex` in `worker-status.json`)
- The branch you should be working on

If you did not receive `.codex/README.md` at startup, read it now:

```bash
cat .codex/README.md
```

---

## Step 2 — Verify Shell Tools Available

```bash
which git && git --version
which jq && jq --version
gh auth status 2>&1 | head -3
```

If `jq` is missing:
```bash
apt-get install -y jq 2>/dev/null || brew install jq 2>/dev/null
```

---

## Step 3 — Check Your Branch

`.codex/README.md` specifies the branch you should work on. Confirm you are on it:

```bash
git branch --show-current
```

If not, check out the correct branch as specified in `.codex/README.md`.

---

## Step 4 — Load Reading List

Read `agent-os/agents/codex/reading-list.md` and load every **Required** item.

---

## Step 5 — Load Universal Index

Read `agent-os/agents/universal/index.md`. Load all Phase 0, 1, and 2 Required items.

---

## Step 6 — Done

Proceed to `AGENTS.md` → startup sequence (skip clone and branch steps since you are already in the repo).

> **Note:** Codex does not persist files between sessions the same way IDE-based agents do. Each session re-reads `.codex/README.md` as the startup hook. All ROWS skills are loaded from the repo on each session.
