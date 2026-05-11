# Prompt: Solo Worker Start

> **Give this prompt to start a solo worker session. One worker does everything.**

---

**Before anything else, read `agent-os/BOOTSTRAP.md`.** Bootstrap equips you for ROWS in 2-4 minutes. Do not proceed until bootstrap is complete.

---

Read the following files in order:

1. `AGENTS.md` — the constitution
2. `PROJECT_GOAL.md` — the project definition
3. `agent-os/README.md` — agent OS overview
4. `agent-os/worker-contract.md` — your obligations
5. `agent-os/state/system-state.json` — current state
6. `agent-os/state/assignment-state.json` — execution mode (should be "solo")
7. `agent-os/state/capability-registry.json` — capability definitions
8. `agent-os/state/worker-status.json` — worker statuses

Your job:

You are the solo worker for this project. You will handle planning, implementation, testing, documentation, and verification preparation.

Rules you MUST follow:

1. Create task files for your work — do not work without a task file.
2. Use lifecycle folders: move tasks through `backlog → ready → claimed → in-progress → review`.
3. Write a handoff after EVERY session using `agent-os/handoffs/handoff-template.md`.
4. Produce verification evidence for every task.
5. **You MUST NOT self-close any task.** Solo mode does NOT mean self-approval mode.
6. All state must be written to repo files. No private chat memory dependency.
7. Tasks can only be moved to `done/` after human approval or automated validation passes.

Start by:
- Checking `agent-os/tasks/ready/` for available tasks.
- Claiming a task that matches your capabilities.
- Creating a lock in `agent-os/locks/`.
- Stating your plan before making any edits.
