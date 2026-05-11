# Triggers Directory

Trigger files are drop-and-forget signals between agent sessions. A session
that ends writes a trigger file here; the next session reads it to know
exactly what to do first.

**This directory is watched by GitHub Actions.** Any push that adds a file
here fires `.github/workflows/on-trigger.yml`, which notifies the human owner.
Human-decision triggers additionally fire `on-blocker-deadline.yml` every 5 minutes
until the deadline passes or an override is created.

---

## File Naming Convention

```
<type>-<identifier>-<YYYY-MM-DD>.md
```

| Type | Written by | Meaning |
|---|---|---|
| `idle` | Worker (end of session) | No tasks remain; describes blockers |
| `escalation` | Worker (tier-4 hard block) | Human action required — no auto-resolve |
| `human-decision` | Worker (tier-3 blocker) | Decision needed — auto-resolves at deadline |
| `handoff-ready` | Worker (mid-task) | Task paused, ready for pickup |
| `wake` | Any agent | Requesting another worker spin up |
| `stop` | Human owner | Tells a named worker to idle |

---

## General Trigger Format

```markdown
# <Type> Trigger — <identifier>

**Written by:** <worker-name>
**Timestamp:** <ISO-8601>
**Related task:** <TASK-ID> (or "none")

## Summary
<One paragraph explaining the situation>

## What the next agent should do first
<Numbered list — specific enough to execute without reading this whole conversation>

## Files to read
<List of files the next agent needs to load for context>
```

---

## Human-Decision Trigger Format

Used for tier-3 blockers. The `on-blocker-deadline` Action reads `resolve_at`
and `blocker_id` from this format to auto-resolve when the deadline passes.

```markdown
---
trigger_type: human_decision
blocker_id: BLOCKER-[NNNN]
task_id: TASK-[NNNN]
severity: trivial | low | moderate | high | critical
resolve_at: [ISO-8601 — when the default will be applied]
filed_at: [ISO-8601]
filed_by: [worker name]
---

## Decision Required: [Short description]

**Task blocked:** TASK-[NNNN]
**Auto-resolves at:** [resolve_at]
**Default choice:** Option [A/B] — [one-line summary]

[2-3 sentence description of the decision needed and why the worker cannot proceed]

See full blocker record: agent-os/blockers/BLOCKER-[NNNN]-[slug].md

## To Override the Default

Create: agent-os/blockers/overrides/BLOCKER-[NNNN]-override.md
Contents:
  chosen_option: B
  reason: [optional]
Commit and push before [resolve_at].

## To Accept the Default

Do nothing. Option [A] will be applied automatically at [resolve_at].
```

### Deadline Ladder

| Severity | Minutes | Use when |
|---|---|---|
| `trivial` | 5 | Safe, low-consequence, fully reversible |
| `low` | 15 | Minor consequence, easily swappable |
| `moderate` | 30 | Some rework if wrong, no data/security risk |
| `high` | 60 | Significant rework, security, or architecture impact |
| `critical` | 1440 (24h) | Very rare — external commitment or data risk |

---

## Escalation Trigger Format

Used for tier-4 hard blocks. No deadline — requires human action to unblock.

```markdown
---
trigger_type: escalation
blocker_id: BLOCKER-[NNNN]
task_id: TASK-[NNNN]
severity: critical
manual_only: true
filed_at: [ISO-8601]
filed_by: [worker name]
---

## Human Action Required

**Task blocked:** TASK-[NNNN]
**This blocker will NOT auto-resolve.**

[Description of what is needed and why it cannot be auto-resolved]

See: agent-os/blockers/BLOCKER-[NNNN]-[slug].md

## To Unblock

1. Resolve the external dependency / make the decision
2. Move the task: tasks/blocked/ → tasks/ready/
3. Update the blocker record status to 'human-resolved'
4. Archive this trigger to agent-os/triggers/archive/
5. Commit and push
```

---

## Lifecycle

1. Worker writes trigger file to this directory.
2. Worker commits and pushes (Rule 23).
3. GitHub Actions fires `on-trigger.yml` → human notified via GitHub Issue.
4. For `human-decision` triggers: `on-blocker-deadline` checks every 5 minutes.
5. At deadline (or when override detected): task auto-promoted to `tasks/ready/`.
6. After work is complete: trigger archived to `triggers/archive/`.

---

## Archive

Processed trigger files move to `triggers/archive/` to keep the active
directory clean. Only unprocessed triggers should exist here.
