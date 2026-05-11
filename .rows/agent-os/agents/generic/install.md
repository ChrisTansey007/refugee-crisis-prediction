# Generic Self-Install

You are an agent that does not match one of the named ROWS types. This is fine — ROWS is designed to work with any agent. Your install is context-loading only.

---

## Step 1 — Determine Your Capabilities

Answer these questions before proceeding:

1. **Can you write files to this repo?** (yes / no / unsure)
2. **Do you have shell/terminal access?** (yes / no / unsure)
3. **Do you have a native skill-loading mechanism?** (e.g., a folder of rules/workflows your platform reads automatically) (yes / no)

If yes to #3: check if the ROWS skills can be adapted for your platform. Look at `agent-os/agents/windsurf/workflows/` for an example of what platform-adapted skills look like.

---

## Step 2 — If You Can Write Files

If you answered yes to #1, you can attempt to adapt the Windsurf or Cursor install:

```bash
# Check what platform-specific folders exist
ls -la .*/  2>/dev/null | grep "^d"

# If your platform has a skill/rule folder, copy the generic skills:
mkdir -p .[your-platform]/[skills-folder]
cp agent-os/agents/windsurf/workflows/*.md .[your-platform]/[skills-folder]/
```

Then load your reading list (Step 3) as well.

---

## Step 3 — Load Reading List

Read `agent-os/agents/generic/reading-list.md` and load every **Required** item.

---

## Step 4 — Load Universal Index

Read `agent-os/agents/universal/index.md`. Load all Phase 0, 1, and 2 Required items.

---

## Step 5 — Register Yourself in Worker Status

If you can write files, add yourself to `agent-os/state/worker-status.json`:

```bash
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '.workers.generic = {"status": "active", "last_active": $ts, "current_task": null, "notes": "Generic agent"}' \
  agent-os/state/worker-status.json > /tmp/ws.json \
  && mv /tmp/ws.json agent-os/state/worker-status.json
```

Replace `generic` with a more specific identifier if you know your agent name.

---

## Step 6 — Done

Proceed to `AGENTS.md`.

> **Note:** If you are a new agent type that will be used regularly in this repo, consider submitting an addition to `agent-os/agents/registry.md` and creating a dedicated folder for your type.
