# Prompt: Goal Intake to Tasks

> **Give this prompt to a worker after filling in `PROJECT_GOAL.md`. Recommended workers: Hermes or Claude.**

---

**Before anything else, read `agent-os/BOOTSTRAP.md`.** Bootstrap equips you for ROWS in 2-4 minutes. Do not proceed until bootstrap is complete.

---

Read the following files in order:

1. `AGENTS.md` — the constitution
2. `PROJECT_GOAL.md` — the project definition
3. `agent-os/README.md` — agent OS overview
4. `agent-os/assignment-model.md` — assignment hierarchy
5. `agent-os/execution-modes.md` — execution modes
6. `agent-os/role-capability-matrix.md` — role-to-capability mapping
7. `agent-os/tasks/task-template.md` — task file template

Your job:

1. Analyze the project goal in `PROJECT_GOAL.md`.
2. Decompose it into discrete, claimable tasks.
3. For each task, create a task file using the template at `agent-os/tasks/task-template.md`.
4. Include in each task:
   - Responsible role
   - Required capabilities
   - Preferred workers (recommendations only)
   - Execution mode compatibility
   - Clear acceptance criteria
5. Place task files in `agent-os/tasks/backlog/`.
6. Update the risk register (`agent-os/state/risk-register.json`) if you identify new risks.
7. Update the dependency map if tasks depend on each other.

Do NOT:
- Start implementing any task.
- Place tasks directly in `ready/` — they go to `backlog/` for human review.
- Make assumptions not supported by `PROJECT_GOAL.md`.

After completion:
- Write a handoff using `agent-os/handoffs/handoff-template.md`.
- Place the handoff in `agent-os/handoffs/active/`.
- Summarize what tasks were created and why.
