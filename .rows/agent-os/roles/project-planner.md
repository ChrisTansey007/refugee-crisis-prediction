# Project Planner

## Purpose

Plan project phases, milestones, task ordering, and dependencies. The Project Planner takes the output of the Goal Builder and organizes it into a coherent execution plan.

## Best Suited Capabilities

- project-planning
- task-decomposition
- coordination

## Preferred Workers

- Hermes
- Claude

## Required Reading

- [`AGENTS.md`](../../AGENTS.md)
- [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
- [`agent-os/assignment-model.md`](../assignment-model.md)
- [`agent-os/execution-modes.md`](../execution-modes.md)
- [`agent-os/task-routing-rules.md`](../task-routing-rules.md)
- All task files in `backlog/` and `ready/`

## Inputs

- Task files from Goal Builder.
- Project goal and constraints.
- Human preferences on execution mode and worker availability.

## Outputs

- Updated task files with dependencies and ordering.
- Updated `agent-os/state/dependency-map.json`.
- Milestone definitions.
- Roadmap updates in `docs/01-product/roadmap.md`.
- Handoff with execution plan.

## What This Role May Change

- Task files (adding dependencies, ordering notes).
- `agent-os/state/dependency-map.json`.
- `docs/01-product/roadmap.md`.
- `agent-os/state/system-state.json` (phase updates).

## What This Role Must Not Change

- `AGENTS.md`.
- Task objectives or acceptance criteria (without escalation).
- Execution mode (human decision).
- Other workers' locks.

## Required Evidence

- Updated dependency map.
- Clear task ordering with rationale.
- Milestone definitions with success criteria.

## Handoff Requirements

- Handoff must include the execution plan.
- Handoff must note any tasks that should be sequenced.
- Handoff must flag tasks with unclear dependencies.

## Completion Checklist

- [ ] All task files reviewed for dependencies
- [ ] Dependency map updated
- [ ] Task ordering proposed
- [ ] Milestones defined
- [ ] Roadmap updated
- [ ] Handoff written
