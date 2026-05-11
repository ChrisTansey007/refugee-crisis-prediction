# Prompt: Reassignment Continuation

> **Give this prompt to a worker taking over a task from another worker.**

---

**Before anything else, read `agent-os/BOOTSTRAP.md`.** Bootstrap equips you for ROWS in 2-4 minutes. Do not proceed until bootstrap is complete.

---

Read the following files in order:

1. `AGENTS.md` — the constitution
2. `agent-os/worker-contract.md` — your obligations
3. `agent-os/worker-switching-protocol.md` — reassignment protocol

Then read the task-specific files:

4. The task file (find it in `agent-os/tasks/` — may be in `in-progress/`, `blocked/`, or `review/`)
5. The PREVIOUS worker's handoff in `agent-os/handoffs/active/`
6. The reassignment record in `agent-os/reassignment/`
7. Any verification evidence in `agent-os/reports/verification/`
8. Any changed files referenced in the handoff

Your job:

You are taking over a task that was previously assigned to another worker. The previous worker has written a handoff. Your job is to continue the work without relying on private chat memory.

Rules you MUST follow:

1. Read ALL materials before taking any action.
2. Create a NEW lock in `agent-os/locks/` — do not reuse the previous worker's lock.
3. Update the task file's `Current claimed worker` field to yourself.
4. Update `agent-os/state/worker-status.json` with your current task.
5. Preserve continuity — reference the previous handoff in your own handoff.
6. Do not rely on private chat memory. Everything you need is in repo files.
7. If the handoff is insufficient, escalate — do not guess.

Start by:
- Inspecting changed files to understand current state.
- Identifying what was completed and what remains.
- Stating your plan before making edits.
