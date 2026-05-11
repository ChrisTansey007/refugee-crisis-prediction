# Roles

> **Roles are jobs. Workers are tools. This directory defines the jobs that workers perform.**

---

## What Are Roles?

A **role** describes the type of work being performed. A **worker** describes the AI tool or human executing the work.

A single worker may perform multiple roles. A single role may be performed by different workers over time. The repo must preserve continuity through durable files, not private chat memory.

---

## Role List

| Role | File | Purpose |
|------|------|---------|
| Goal Builder | [`goal-builder.md`](./goal-builder.md) | Decompose project goals into task files |
| Project Planner | [`project-planner.md`](./project-planner.md) | Plan phases, milestones, and task ordering |
| Architect | [`architect.md`](./architect.md) | Design system architecture and make tech decisions |
| Researcher | [`researcher.md`](./researcher.md) | Research technologies, patterns, and approaches |
| Backend Builder | [`backend-builder.md`](./backend-builder.md) | Implement backend services and APIs |
| Frontend Builder | [`frontend-builder.md`](./frontend-builder.md) | Implement frontend UI and components |
| QA Verifier | [`qa-verifier.md`](./qa-verifier.md) | Verify implementations and write tests |
| Documentation Maintainer | [`documentation-maintainer.md`](./documentation-maintainer.md) | Write and maintain documentation |
| Release Reviewer | [`release-reviewer.md`](./release-reviewer.md) | Review work before release |
| Coordinator | [`coordinator.md`](./coordinator.md) | Coordinate multi-worker efforts |

---

## How Roles Are Assigned

Role assignment is recorded in:
- Task files (`## Responsible role`, `## Supporting roles`)
- `agent-os/state/assignment-state.json`
- `agent-os/state/worker-status.json` (each worker's `active_roles`)

A worker performing a role must:
1. Read the role file for requirements.
2. Confirm capability fit against `capability-registry.json`.
3. Record the role in their worker status entry.
4. Follow the role's completion checklist.

---

## Related Files

- [`../role-capability-matrix.md`](../role-capability-matrix.md) — Full role-to-capability mapping
- [`../assignment-model.md`](../assignment-model.md) — Assignment hierarchy
- [`../workers/`](../workers/) — Worker definitions
- [`../state/capability-registry.json`](../state/capability-registry.json) — Machine-readable capabilities
