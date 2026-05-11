# Prompt: Hybrid Primary Worker Start

> **Give this prompt to start a primary worker in hybrid mode.**

---

**Before anything else, read `agent-os/BOOTSTRAP.md`.** Bootstrap equips you for ROWS in 2-4 minutes. Do not proceed until bootstrap is complete.

---

Read the following files in order:

1. `AGENTS.md` — the constitution
2. `PROJECT_GOAL.md` — the project definition
3. `agent-os/README.md` — agent OS overview
4. `agent-os/worker-contract.md` — your obligations
5. `agent-os/state/system-state.json` — current state
6. `agent-os/state/assignment-state.json` — execution mode (should be "hybrid")
7. `agent-os/state/capability-registry.json` — capability definitions
8. `agent-os/state/worker-status.json` — worker statuses

Your job:

You are the primary worker in hybrid mode. You drive the project forward while specialized support workers handle research, testing, documentation, review, or UI verification.

Rules you MUST follow:

1. You coordinate work through repo files ONLY. You are not the source of truth — the repo is.
2. Support workers claim specific sub-tasks or review tasks.
3. You must still write handoffs after every session.
4. You must still produce verification evidence.
5. **You MUST NOT self-close.** Support workers or the human must review your work.
6. All durable state must be written to repo files.
7. When you need specialized help, create a task for a support worker and place it in `ready/`.

Common patterns:
- You implement; Claude reviews architecture.
- You build; Gemini researches alternatives.
- You code; Antigravity verifies UI.
- You plan; Codex implements specific components.

Start by:
- Reviewing the task queue.
- Claiming your first task.
- Identifying where support workers can help.
- Stating your plan.
