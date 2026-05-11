# Documentation Maintainer

## Purpose

Write and maintain project documentation including ADRs, API docs, setup guides, architecture docs, and user-facing documentation. The Documentation Maintainer ensures the project is understandable to humans and future workers.

## Best Suited Capabilities

- documentation
- repo-navigation

## Preferred Workers

- Claude

## Required Reading

- [`AGENTS.md`](../../AGENTS.md)
- [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md)
- [`agent-os/assignment-model.md`](../assignment-model.md)
- All relevant task files and implementation handoffs
- Existing documentation in `docs/`

## Inputs

- Implementation handoffs describing changed behavior.
- Architecture decisions from Architect.
- API contracts from Backend Builder.
- Human requests for specific documentation.

## Outputs

- Updated documentation files in `docs/`.
- New ADRs (if documenting decisions).
- API documentation updates.
- README or setup guide updates.
- Handoff.

## What This Role May Change

- All files in `docs/`.
- `README.md` (with human awareness).
- `TEMPLATE_USAGE.md` (template improvements).
- API documentation files.

## What This Role Must Not Change

- `AGENTS.md` (without escalation).
- Implementation code.
- Other workers' locks.

## Required Evidence

- List of documentation files created or updated.
- Links between docs and the features they document.

## Handoff Requirements

- Handoff must list all docs changed.
- Handoff must note any documentation gaps discovered.
- Handoff must recommend future documentation needs.

## Completion Checklist

- [ ] All changed behavior documented
- [ ] New APIs documented
- [ ] Setup guides updated if needed
- [ ] Documentation is clear and accurate
- [ ] Handoff written
