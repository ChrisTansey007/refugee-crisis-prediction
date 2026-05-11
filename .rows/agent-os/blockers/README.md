# agent-os/blockers/

Structured records for every tier-3 and tier-4 blocker in the project.

## Directory Structure

```
agent-os/blockers/
  README.md                        — this file
  blocker-template.md              — copy this to create a new blocker record
  BLOCKER-0001-[slug].md           — individual blocker records
  overrides/
    README.md                      — override instructions
    BLOCKER-0001-override.md       — human override files (created manually)
```

## Lifecycle

```
Worker hits blocker
  → Attempts Tier 1 (context) and Tier 2 (assume + flag)
  → If still blocked: writes BLOCKER-NNNN.md here (Tier 3 or 4)
  → Moves task to tasks/blocked/
  → Writes trigger file in agent-os/triggers/
  → Pushes and claims next task

on-blocker-deadline Action fires (every 5 min)
  → Checks resolve_at on all open blockers
  → If deadline passed and no override: applies default, marks auto-resolved
  → If override file exists: applies override choice, marks overridden
  → Moves task back to tasks/ready/
  → Logs decision to docs/05-decisions/decision-register.md
  → Opens GitHub issue summarizing resolution
```

## Naming Convention

`BLOCKER-[NNNN]-[short-slug].md`

Example: `BLOCKER-0001-auth-provider-choice.md`

## Status Values

| Status | Meaning |
|---|---|
| `open` | Awaiting resolution |
| `auto-resolved` | Deadline passed, default choice applied |
| `human-resolved` | Human responded before deadline |
| `overridden` | Human created an override file |

## Rules

- Never delete a blocker record — mark it resolved instead
- Blocker IDs are sequential and never reused
- Every task in `tasks/blocked/` must have a corresponding blocker record here
- See `agent-os/protocols/blocker-protocol.md` for the full resolution protocol
