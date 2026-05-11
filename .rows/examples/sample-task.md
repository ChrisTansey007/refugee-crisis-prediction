# Example: Task File

> **This is a fictional example for "TaskFlow Lite." It shows proper use of the role/capability assignment model. This is NOT an active task.**

---

# TASK-0003: Implement Drag-and-Drop Task Board

## Status

ready

## Execution Mode Compatibility

- solo
- multi-worker
- hybrid

## Responsible Role

frontend-builder

## Supporting Roles

- qa-verifier

## Required Capabilities

- frontend-implementation
- test-writing

## Preferred Workers

- windsurf
- codex

## Current Claimed Worker

none

## Reassignment Allowed

yes

## Reassignment Conditions

- worker is blocked
- lock is stale
- human owner requests reassignment

## Objective

Implement a three-column Kanban-style task board (To Do, In Progress, Done) with drag-and-drop functionality. Tasks should be movable between columns using HTML5 drag-and-drop API. Column state must persist to localStorage. The board should be responsive and work on mobile viewports.

## Required Reading

- [ ] [`AGENTS.md`](../AGENTS.md)
- [ ] [`PROJECT_GOAL.md`](../PROJECT_GOAL.md)
- [ ] [`docs/02-architecture/data-model.md`](../docs/02-architecture/data-model.md)

## Files Likely Affected

- `src/components/TaskBoard.tsx` — New: main board component
- `src/components/TaskColumn.tsx` — New: individual column component
- `src/components/TaskCard.tsx` — New: draggable task card
- `src/hooks/useTaskBoard.ts` — New: board state management hook
- `src/types/task.ts` — Modify: add board-related types
- `tests/components/TaskBoard.test.tsx` — New: board tests

## Acceptance Criteria

- [ ] Three columns render: To Do, In Progress, Done
- [ ] Tasks can be dragged between any two columns
- [ ] Column order persists after page refresh
- [ ] Board is responsive (single column on mobile, three columns on desktop)
- [ ] Drag-and-drop works with keyboard (accessibility)
- [ ] Empty columns show a placeholder message

## Verification Required

- [ ] Self-check against acceptance criteria
- [ ] Automated tests pass
- [ ] Independent review by different worker or human

## Completion Evidence Required

- [ ] Test results (pass/fail counts)
- [ ] Screenshots of board on desktop and mobile
- [ ] Screen recording of drag-and-drop interaction
- [ ] Documentation updated

## Handoff Required

- [ ] Handoff written using [`handoffs/handoff-template.md`](../agent-os/handoffs/handoff-template.md)
- [ ] Handoff placed in `handoffs/active/`

## Risks

- Drag-and-drop API may behave differently across browsers.
- Mobile drag-and-drop may require touch event handling.
- localStorage size limits may be reached with many tasks.

## Dependencies

- TASK-0001 — Project setup and scaffolding must be complete.
- TASK-0002 — Task data model and types must be defined.

## Notes

Use @dnd-kit/core library for drag-and-drop if HTML5 API proves insufficient. Prioritize keyboard accessibility — all drag operations must have keyboard equivalents.
