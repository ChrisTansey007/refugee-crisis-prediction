# Cursor Self-Install

You are Cursor AI. You have full file write access and terminal access. ROWS skills are installed as Cursor Rule files in `.cursor/rules/`.

---

## Step 1 — Check Install Status

```bash
ls .cursor/rules/ 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

If `EXISTS` and files are recent: skip to Step 4.
If `MISSING` or empty: continue with Step 2.

---

## Step 2 — Install ROWS Rules

```bash
mkdir -p .cursor/rules
cp agent-os/agents/cursor/rules/*.md .cursor/rules/
echo "Installed $(ls .cursor/rules/ | wc -l) rule files."
```

These files are now natively accessible to Cursor as rules. Cursor will auto-load them.

---

## Step 3 — Verify Installation

```bash
ls -la .cursor/rules/
```

Confirm these files are present:
- `rows-claim-task.md`
- `rows-complete-task.md`
- `rows-session-close.md`
- `rows-escalate-blocker.md`
- `rows-resolve-blocker.md`

If any are missing, re-run Step 2.

---

## Step 4 — Load Reading List Into Context

Read `agent-os/agents/cursor/reading-list.md` and load every **Required** item.

---

## Step 5 — Load Universal Index

Read `agent-os/agents/universal/index.md`. Load all Phase 0, 1, and 2 Required items.

---

## Step 6 — Done

Proceed to `AGENTS.md`.

> **Note:** Like Windsurf, your rule files persist between sessions because they are committed to the repo. On your second and subsequent sessions, Step 2 is a no-op.
