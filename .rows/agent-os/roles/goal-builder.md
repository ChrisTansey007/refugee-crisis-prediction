# Goal Builder

## Purpose

Decompose the project goal from `PROJECT_GOAL.md` into actionable, claimable task files. The Goal Builder is typically the first role activated in a new project.

## Best Suited Capabilities

- goal-decomposition
- task-decomposition
- project-planning

## Preferred Workers

- Hermes
- Claude

## Required Reading

- [`AGENTS.md`](../../AGENTS.md)
- [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
- [`agent-os/assignment-model.md`](../assignment-model.md)
- [`agent-os/task-routing-rules.md`](../task-routing-rules.md)
- [`agent-os/tasks/task-template.md`](../tasks/task-template.md)
- [`agent-os/role-capability-matrix.md`](../role-capability-matrix.md)

## Inputs

- Completed `PROJECT_GOAL.md` (no placeholders remaining).
- Existing repo structure and template files.
- Any additional human guidance.

## Outputs

- Task files in `agent-os/tasks/backlog/` (5-15 tasks typical).
- Updated `agent-os/state/system-state.json` (phase, task count).
- Handoff summarizing all generated tasks and their relationships.

## What This Role May Change

- `agent-os/tasks/backlog/` — Create new task files.
- `agent-os/state/system-state.json` — Update phase and task count.
- `agent-os/state/dependency-map.json` — Record task dependencies.
- `docs/00-project-brief/` — Populate with project-specific content.
- `docs/01-product/` — Populate with initial product requirements.

## What This Role Must Not Change

- `AGENTS.md` — The constitution.
- `agent-os/worker-contract.md` — Worker obligations.
- `agent-os/definition-of-done.md` — Completion criteria.
- Any lock files belonging to other workers.
- The execution mode in `assignment-state.json` (human decision).

## Required Evidence

- List of all task files created with their objectives.
- Updated system-state.json.
- Handoff summarizing the decomposition.

## Handoff Requirements

- Handoff must list every task created with a one-line summary.
- Handoff must note any ambiguities in the project goal.
- Handoff must recommend task ordering and dependencies.
- Handoff must specify which worker types are recommended for each task.

## Completion Checklist

- [ ] `PROJECT_GOAL.md` read and understood
- [ ] Goal decomposed into discrete, claimable tasks
- [ ] Each task uses the standard task template
- [ ] Each task includes required capabilities and preferred workers
- [ ] Tasks placed in `backlog/` (not `ready/` unless approved)
- [ ] System state updated
- [ ] Handoff written
- [ ] Human notified for review
