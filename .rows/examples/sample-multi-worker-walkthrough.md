# Example: Multi-Worker Walkthrough

> **This is a fictional example for "TaskFlow Lite." It shows how multiple workers can coordinate through repo files. This is NOT active repo state.**

---

# Walkthrough: Multi-Worker Delivery on TASK-0007

## Scenario

TaskFlow Lite needs a small improvement: users want to reorder cards in the board sidebar and have the change reflected in the activity feed.

The human owner has already completed `PROJECT_GOAL.md`, approved an initial task set, and moved a few tasks into `agent-os/tasks/ready/`.

## Worker Split

| Worker | Role | Job |
|--------|------|-----|
| Hermes | coordinator | Break the work into claimable tasks and recommend sequencing. |
| Windsurf | backend-builder / repo editor | Implement the state update and file changes. |
| Codex | test-writer | Add focused tests for the reorder logic. |
| Antigravity | qa-verifier | Verify the UI behavior and capture screenshots. |
| Claude | reviewer | Review the design, documentation, and evidence before closeout. |

## Step 1: Hermes decomposes the work

Hermes reads `AGENTS.md`, `PROJECT_GOAL.md`, and the existing backlog, then creates a short coordination note that recommends three claimable tasks:

1. Update the board data model.
2. Add tests for the reorder flow.
3. Verify the visual behavior in the browser.

Hermes writes the decomposition into a handoff and leaves the task files in `agent-os/tasks/backlog/` for human approval.

## Step 2: The human approves and moves tasks to ready

The human reviews the task files, confirms that the scope is clear, and moves them into `agent-os/tasks/ready/`.

At this point the repo becomes the source of truth:
- the task files are ready to claim,
- the assignment state reflects the chosen execution mode,
- and the backlog remains readable by the next worker.

## Step 3: Windsurf claims the implementation task

Windsurf claims the main implementation task, creates a task-scoped worktree, and records the lock file.

Typical evidence trail:
- branch: `agent/windsurf/TASK-0007-worktree`
- worktree path: `../rows-template-windsurf`
- lock file: `agent-os/locks/TASK-0007.json`
- handoff: `agent-os/handoffs/active/TASK-0007-handoff.md`

Windsurf updates the board state, keeps the change scoped, and leaves implementation notes in the handoff.

## Step 4: Codex adds tests

Codex works from the same task split but in a separate checkout. It focuses on the reorder logic tests and keeps the changes narrow:

- one test file for the reorder reducer,
- one test file for the activity feed update,
- and a short note about assumptions and edge cases.

Codex does not try to own the entire feature; it only owns the testing slice.

## Step 5: Antigravity verifies the result

Antigravity opens the UI, exercises the reorder flow, and captures evidence:

- desktop screenshot showing the reordered sidebar,
- recording note documenting the interaction,
- verification report mapping each acceptance criterion to evidence.

If the UI fails to match the expected behavior, Antigravity records the failure instead of forcing a pass.

## Step 6: Claude reviews the closeout package

Claude reads the handoff, checks the tests, and reviews the evidence trail. The review focuses on:

- whether the acceptance criteria are actually met,
- whether the handoff is complete,
- whether the evidence supports the claim,
- whether any follow-up work should be split into a new task.

Claude does not re-implement the feature. It reviews and recommends.

## What Makes This a Good Multi-Worker Flow

- Each worker has a clear lane.
- The repo files show the state transitions.
- Handoffs make the work continuable.
- Verification is separate from implementation.
- No worker marks its own task done.

## Example Artifact Trail

| Artifact | Example Path |
|----------|--------------|
| Task file | `agent-os/tasks/backlog/TASK-0007-reorder-sidebar.md` |
| Handoff | `agent-os/handoffs/active/TASK-0007-handoff.md` |
| Lock | `agent-os/locks/TASK-0007.json` |
| Verification report | `agent-os/reports/verification/TASK-0007-verification.md` |
| Screenshot | `agent-os/reports/verification/TASK-0007-desktop.png` |
| Recording note | `agent-os/reports/verification/TASK-0007-recording-note.md` |

## Reminder

This walkthrough is illustrative only. It shows the *shape* of a healthy multi-worker process, not active state in this repository.
