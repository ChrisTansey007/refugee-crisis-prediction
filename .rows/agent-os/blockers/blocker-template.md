---
id: BLOCKER-[NNNN]
task_id: TASK-[NNNN]
type: dependency | external | human_decision | capability | environment
severity: trivial | low | moderate | high | critical
deadline_minutes: 5 | 15 | 30 | 60 | 1440
filed_at: [ISO-8601 timestamp]
filed_by: [worker name]
status: open
resolve_at: [ISO-8601 timestamp — filed_at + deadline_minutes]
irreversible: false
manual_only: false
---

# BLOCKER-[NNNN] — [Short description]

## What Is Blocking

[Clear, one-paragraph description of what is blocking TASK-[NNNN] and why the
worker cannot proceed without a decision. Reference the specific line of code,
design choice, or external dependency involved.]

## Context

[What has already been tried or considered. Reference PROJECT_GOAL.md, ADR files,
or handoffs that are relevant to this decision.]

## Related ADRs

- [ADR-XXXX] — [Why this ADR matters to the blocker]

## Related Decisions

- [Decision ID] — [Prior decision or blocker outcome this blocker touches]

## Options

### Option A — [Name]

[Description of this option.]

**Consequences if chosen:**
- [consequence 1]
- [consequence 2]

**Reversibility:** [trivial | low | moderate | high | irreversible]

---

### Option B — [Name]

[Description of this option.]

**Consequences if chosen:**
- [consequence 1]
- [consequence 2]

**Reversibility:** [trivial | low | moderate | high | irreversible]

---

## Default Choice

**Option A** — [Reasoning. Must reference an existing document, prior decision,
or stated goal. "I think A is better" is not sufficient. "PROJECT_GOAL.md specifies
X which aligns with Option A because Y" is sufficient.]

## Override Instructions

To choose a different option, create this file **before `resolve_at`**:

`agent-os/blockers/overrides/BLOCKER-[NNNN]-override.md`

Contents:
```
chosen_option: B
reason: [optional — why you prefer B]
```

Commit and push. The system will apply your choice within 5 minutes.

---

## Resolution

> *Filled in automatically by the on-blocker-deadline Action or manually by the
> human owner. Do not edit this section.*

**Resolved at:** —
**Method:** — `auto` | `human` | `override`
**Chosen option:** —
**Decision logged at:** —
