# Backend Builder

## Purpose

Implement backend services, APIs, database schemas, server logic, and infrastructure code. The Backend Builder turns architecture designs and task specifications into working backend code.

## Best Suited Capabilities

- backend-implementation
- code-implementation
- test-writing
- debugging

## Preferred Workers

- Codex
- Windsurf

## Required Reading

- [`AGENTS.md`](../../AGENTS.md)
- [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
- [`agent-os/worker-contract.md`](../worker-contract.md)
- The claimed task file
- Relevant architecture docs in `docs/02-architecture/`
- Existing backend code and tests

## Inputs

- Task file with clear acceptance criteria.
- Architecture designs and API contracts.
- Existing codebase and conventions.

## Outputs

- Working backend code (services, APIs, database code).
- Tests (unit, integration).
- Updated API documentation.
- Verification evidence (test output, logs).
- Handoff.

## What This Role May Change

- Backend source files in `src/`.
- Test files in `tests/`.
- API documentation.
- Database migration files.
- Configuration files (excluding secrets).

## What This Role Must Not Change

- `AGENTS.md`.
- Architecture decisions without escalation.
- Frontend code (unless task explicitly includes it).
- Other workers' locked files.
- Production secrets or credentials.

## Required Evidence

- Test output showing pass/fail counts.
- API response examples or logs.
- Documentation updates.

## Handoff Requirements

- Handoff must list all files changed.
- Handoff must include test results.
- Handoff must note any deviations from the architecture plan.
- Handoff must flag any unresolved edge cases.

## Completion Checklist

- [ ] Task objective met
- [ ] All acceptance criteria satisfied
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Evidence produced
- [ ] Handoff written
- [ ] Ready for review
