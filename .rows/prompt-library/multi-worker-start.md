# Prompt: Multi-Worker Start

> **Give this prompt to start a multi-worker project. Multiple workers divide work.**

---

**Before anything else, read `agent-os/BOOTSTRAP.md`.** Bootstrap equips you for ROWS in 2-4 minutes. Do not proceed until bootstrap is complete.

---

Read the following files in order:

1. `AGENTS.md` — the constitution
2. `PROJECT_GOAL.md` — the project definition
3. `agent-os/README.md` — agent OS overview
4. `agent-os/worker-contract.md` — your obligations
5. `agent-os/state/system-state.json` — current state
6. `agent-os/state/assignment-state.json` — execution mode (should be "multi-worker")
7. `agent-os/state/capability-registry.json` — capability definitions
8. `agent-os/state/worker-status.json` — worker statuses
9. Your worker file in `agent-os/workers/`
10. The role file for your role in `agent-os/roles/`

Your job:

You are one of multiple workers on this project. Tasks are divided by role, capability, or phase.

Rules you MUST follow:

1. Only claim tasks that match your capabilities.
2. Check `agent-os/locks/` before claiming — respect other workers' locks.
3. Create a lock when you claim a task.
4. Write handoffs after every session.
5. Produce verification evidence.
6. **You MUST NOT close your own tasks.** A different worker must review.
7. If you are blocked, write a handoff and escalate.
8. All state must be written to repo files.

Start by:
- Checking `agent-os/tasks/ready/` for tasks matching your capabilities.
- Claiming ONE task at a time.
- Creating a lock.
- Stating your plan before making edits.
