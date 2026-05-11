# Task Template

> **Use this template for all task files. Copy it and fill in every section.**

---

# [TASK-ID]: [Task Title]

## Status

backlog | ready | claimed | in-progress | review | blocked | done

## Blocker Fields

> *Leave these as `~` unless the task is currently blocked. Set them using the escalate-blocker skill.*

blocked_by: []
blocker_id: ~
blocker_type: ~
blocker_resolved_at: ~
blocker_resolution: ~

## Execution Mode Compatibility

- solo
- multi-worker
- hybrid

## Responsible Role

[ROLE_NAME]

## Supporting Roles

- [ROLE_NAME]

## Required Capabilities

- [CAPABILITY]

## Required Tier

unspecified | frontier | mid | fast | local

## Cost Ceiling

unspecified | low | moderate | high

## Required MCP Servers

- [SERVER_NAME] — [why this server is needed]
- [SERVER_NAME] — [read/write scope and constraints]

## Preferred Workers

- [WORKER_NAME]

## Current Claimed Worker

none

## Reassignment Allowed

yes | no

## Reassignment Conditions

- worker is blocked
- lock is stale
- task scope changed
- tests are failing and review is needed
- human owner requests reassignment
- required capability does not match current worker

## Objective

[Clear, one-paragraph description of what must be accomplished. Be specific enough that a worker can understand the goal without additional context.]

## Related ADRs

- [ADR-XXXX] — [Why this task is shaped by this ADR]

## Related Decisions

- [Decision ID or blocker record] — [What was decided and the consequence for this task]

## Context Snapshot

> Fill this before moving the task to `ready/`. Keep it short enough for a worker to load quickly.

### Why This Task Exists

[1-3 sentences tying the task to the project goal, project context, an ADR, a decision, or an upstream dependency.]

### Key Decisions

- [ADR-XXXX or decision] — [One sentence consequence for this task]

### Key Constraints

- [Constraint and source link]

### Upstream Facts

- [TASK-XXXX] — [Critical fact inherited from upstream work]

### Required Context Links

- [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md) — [Why it matters]

### Snapshot Freshness

- **Generated/updated:** [ISO-8601 timestamp]
- **Source versions:** [commit SHA or "manual"]
- **Needs refresh if:** [related ADRs, decisions, dependencies, or project context change]

## Required Reading

- [ ] [`AGENTS.md`](../../AGENTS.md)
- [ ] [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
- [ ] [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md)
- [ ] [Other specific files the worker must read]

## Files Likely Affected

- `[path/to/file]` — [What will change]
- `[path/to/file]` — [What will change]

## Acceptance Criteria

- [ ] [Criterion 1 — must be testable and unambiguous]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Verification Required

- [ ] Self-check against acceptance criteria
- [ ] Automated tests pass
- [ ] Independent review by different worker or human

## Completion Evidence Required

- [ ] Test results (pass/fail counts)
- [ ] [Screenshots if UI changes]
- [ ] [Logs/output if backend changes]
- [ ] Documentation updated

## Handoff Required

- [ ] Handoff written using [`handoffs/handoff-template.md`](../handoffs/handoff-template.md)
- [ ] Handoff placed in `handoffs/active/`

## Risks

- [Risk 1 — what could go wrong?]
- [Risk 2]

## Dependencies

- [TASK-XXXX] — [What this task depends on and why]
- [None] — If no dependencies

## Notes

[Any additional context, constraints, or guidance for the worker.]
