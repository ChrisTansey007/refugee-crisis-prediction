# TASK-0007-implement-lstm-model: Implement LSTM Model for Migration Forecasting

## Status
backlog

## Blocker Fields

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
ml-engineer

## Supporting Roles
- qa-verifier
- documentation-maintainer

## Required Capabilities
- ml-model-development
- feature-engineering
- model-training

## Required Tier
unspecified

## Cost Ceiling
unspecified

## Required MCP Servers
- none

## Preferred Workers
- Hermes
- Claude
- Codex

## Current Claimed Worker
none

## Reassignment Allowed
yes

## Reassignment Conditions
- worker is blocked
- lock is stale
- task scope changed
- tests are failing and review is needed
- human owner requests reassignment
- required capability does not match current worker

## Objective
Implement an LSTM neural network model for predicting migration flows 4-26 weeks ahead, including data preprocessing, training pipeline, and model serving endpoint.

## Related ADRs
- None yet (to be created as needed)

## Related Decisions
- None yet

## Context Snapshot
### Why This Task Exists
[To be filled based on project context]

### Key Decisions
- Using established patterns from existing codebase

### Key Constraints
- Python 3.11+ requirement
- Must follow existing code style
- Must use environment variables for configuration
- Must not commit secrets to repository

### Upstream Facts
- None

### Required Context Links
- [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md) — Understanding current project state
- [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md) — Understanding the goal of world-class migration forecasting

### Snapshot Freshness
- **Generated/updated:** 2026-05-11T22:00:46.240647Z
- **Source versions:** manual
- **Needs refresh if:** project goal or context changes significantly

## Required Reading
- [ ] [`AGENTS.md`](../../AGENTS.md)
- [ ] [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
- [ ] [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md)

## Files Likely Affected
[To be determined during task analysis]

## Acceptance Criteria
[ ] LSTM model architecture defined and implemented
[ ] Model training pipeline works with UNHCR and other ingested data
[ ] Model achieves reasonable baseline performance on validation set
[ ] Model serving endpoint exposed at /predictions/lstm
[ ] Model explains predictions with feature importance
[ ] Model training logs and artifacts saved

## Verification Required
- [ ] Self-check against acceptance criteria
- [ ] Automated tests pass
- [ ] Independent review by different worker or human

## Completion Evidence Required
- [ ] Test results (pass/fail counts)
- [ ] Backend startup logs showing successful initialization (if applicable)
- [ ] Screenshots of interface (if UI changes)
- [ ] Database migration logs (if schema changes)
- [ ] Documentation updated in relevant files

## Handoff Required
- [ ] Handoff written using [`handoffs/handoff-template.md`](../handoffs/handoff-template.md)
- [ ] Handoff placed in `handoffs/active/`

## Risks
- Scope creep without proper verification
- Integration issues with existing components
- Performance regressions

## Dependencies
- TASK-0001-initialize-backend-core.md — Backend core must be functional

## Notes
This task should follow existing patterns in the codebase. Ensure all changes are committed with descriptive messages and proper documentation updates.
