# TASK-0001: Initialize Project from Goal

## Status

backlog

## Execution Mode Compatibility

- solo
- multi-worker
- hybrid

## Responsible Role

goal-builder

## Supporting Roles

- project-planner
- architect

## Required Capabilities

- goal-decomposition
- task-decomposition
- project-planning
- documentation

## Preferred Workers

- Hermes
- Claude

## Current Claimed Worker

none

## Reassignment Allowed

yes

## Reassignment Conditions

- worker is blocked
- lock is stale
- task scope changed
- human owner requests reassignment
- required capability does not match current worker

## Objective

Read `PROJECT_GOAL.md` and the existing template structure, then generate the initial set of project documentation and task proposals. This is the first task that bootstraps a new project from the template.

Specifically:
1. Read and understand the project goal.
2. Populate the `docs/00-project-brief/` files with project-specific content derived from the goal.
3. Populate the `docs/01-product/` files with initial product requirements.
4. Create an initial system architecture sketch in `docs/02-architecture/system-overview.md`.
5. Decompose the project goal into 5-15 initial task files and place them in `agent-os/tasks/backlog/`.
6. Update `agent-os/state/system-state.json` to reflect the new phase.

## Required Reading

- [ ] [`AGENTS.md`](../../../AGENTS.md)
- [ ] [`PROJECT_GOAL.md`](../../../PROJECT_GOAL.md)
- [ ] [`agent-os/README.md`](../README.md)
- [ ] [`agent-os/worker-contract.md`](../../worker-contract.md)
- [ ] [`agent-os/tasks/task-template.md`](../task-template.md)
- [ ] [`docs/00-project-brief/`](../../../docs/00-project-brief/) (all files)
- [ ] [`docs/01-product/`](../../../docs/01-product/) (all files)

## Files Likely Affected

- `docs/00-project-brief/vision.md` — Populate with project-specific vision
- `docs/00-project-brief/current-scope.md` — Define initial scope
- `docs/00-project-brief/non-goals.md` — Confirm or expand non-goals
- `docs/00-project-brief/glossary.md` — Add project-specific terms
- `docs/01-product/prd.md` — Create initial PRD
- `docs/01-product/user-stories.md` — Create initial user stories
- `docs/01-product/acceptance-criteria.md` — Define acceptance criteria
- `docs/01-product/roadmap.md` — Create initial roadmap
- `docs/02-architecture/system-overview.md` — Create architecture sketch
- `agent-os/tasks/backlog/` — Create TASK-0002 through TASK-XXXX
- `agent-os/state/system-state.json` — Update phase and task count

## Acceptance Criteria

- [ ] All `docs/00-project-brief/` files contain project-specific content (no template placeholders remain).
- [ ] `docs/01-product/prd.md` contains at least 3 core features derived from the goal.
- [ ] `docs/01-product/user-stories.md` contains at least 5 user stories.
- [ ] `docs/02-architecture/system-overview.md` contains a proposed tech stack and component diagram description.
- [ ] At least 5 task files are created in `agent-os/tasks/backlog/`, each using the task template.
- [ ] Each generated task is independently claimable (minimal dependencies).
- [ ] `agent-os/state/system-state.json` is updated with the new phase.
- [ ] A handoff is written summarizing all generated artifacts.

## Verification Required

- [ ] Self-check against acceptance criteria
- [ ] Human reviews all generated docs and tasks
- [ ] Human moves approved tasks from `backlog/` to `ready/`

## Completion Evidence Required

- [ ] List of all files created or modified
- [ ] Summary of generated tasks with their objectives
- [ ] Updated system-state.json

## Handoff Required

- [ ] Handoff written using [`handoffs/handoff-template.md`](../../handoffs/handoff-template.md)
- [ ] Handoff placed in `handoffs/active/`

## Risks

- The project goal may be too vague, leading to incorrect assumptions. Workers should flag ambiguities.
- Generated tasks may be too large or too small. Human review is essential.
- The tech stack in the goal may need refinement after architecture analysis.

## Dependencies

- None — this is the first task.

## Notes

This task is the bootstrap for every new ROWS project. After completion, the human should review all generated content, refine as needed, and move approved tasks to `ready/` to begin the development cycle.

If `PROJECT_GOAL.md` is still full of placeholders (e.g., `[PROJECT_NAME]`), do NOT proceed. Escalate to the human and request that they complete the goal file first.
