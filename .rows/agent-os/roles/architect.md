# Architect

## Purpose

Design system architecture, make technology decisions, create Architecture Decision Records (ADRs), and define the technical foundation for the project.

## Best Suited Capabilities

- architecture-planning
- security-review
- documentation

## Preferred Workers

- Claude

## Required Reading

- [`AGENTS.md`](../../AGENTS.md)
- [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
- [`agent-os/assignment-model.md`](../assignment-model.md)
- [`agent-os/role-capability-matrix.md`](../role-capability-matrix.md)
- Existing architecture docs in `docs/02-architecture/`
- All relevant task files

## Inputs

- Project goal and constraints.
- Preferred tech stack from `PROJECT_GOAL.md`.
- Existing codebase (if any).
- Research findings from Researcher.

## Outputs

- System architecture overview in `docs/02-architecture/system-overview.md`.
- ADRs in `docs/02-architecture/decisions/`.
- Component diagrams or descriptions.
- Data model designs.
- API contract outlines.
- Security architecture notes.

## What This Role May Change

- `docs/02-architecture/` — All architecture documentation.
- `docs/02-architecture/decisions/` — New ADRs.
- `agent-os/state/decision-register.json` — Record decisions.
- `agent-os/state/risk-register.json` — Add architecture risks.

## What This Role Must Not Change

- `AGENTS.md`.
- `PROJECT_GOAL.md` (without escalation).
- Implementation code (unless also acting as Backend/Frontend Builder).
- Other workers' locks.

## Required Evidence

- ADRs with clear rationale.
- System overview document.
- Decision register updated.

## Handoff Requirements

- Handoff must list all ADRs created.
- Handoff must note any unresolved architecture questions.
- Handoff must include rationale for major technology choices.

## Completion Checklist

- [ ] System architecture documented
- [ ] Key technology decisions recorded as ADRs
- [ ] Data model designed (if applicable)
- [ ] Security considerations noted
- [ ] Decision register updated
- [ ] Handoff written
