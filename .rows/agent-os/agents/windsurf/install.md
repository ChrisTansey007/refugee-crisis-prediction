# Windsurf Self-Install

You are Windsurf (Cascade AI). You have full file write access and terminal access. ROWS skills are installed as Windsurf Workflow files in `.windsurf/workflows/`.

---

## Step 1 — Check Install Status

```bash
ls .windsurf/workflows/ 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

If `EXISTS` and files are recent: skip to Step 4.
If `MISSING` or empty: continue with Step 2.

---

## Step 2 — Install ROWS Workflows

```bash
mkdir -p .windsurf/workflows
cp agent-os/agents/windsurf/workflows/*.md .windsurf/workflows/
echo "Installed $(ls .windsurf/workflows/ | wc -l) workflow files."
```

These files are now natively accessible to Cascade as workflows. Windsurf will auto-load them.

---

## Step 3 — Verify Installation

```bash
ls -la .windsurf/workflows/
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

Even with workflows installed, you need project context. Read this file now and load every **Required** item:

```
agent-os/agents/windsurf/reading-list.md
```

---

## Step 5 — Load Universal Index

Read `agent-os/agents/universal/index.md` and load all Phase 0, 1, and 2 Required items.

---

## Step 6 — Done

Proceed to `AGENTS.md`.

> **Note:** Workflow files persist between sessions because they are committed to the repo. On your second and subsequent sessions in this repo, Step 2 is a no-op — the files are already there.
