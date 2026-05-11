# Blocker Protocol

> **Before declaring any task blocked, a worker must attempt all tiers in order.**
> Skipping a tier is a rule violation. Most blockers never reach tier 3.

---

## Blocker Types

Every blocker must be classified as one of:

| Type | Meaning |
|---|---|
| `dependency` | Waiting on another ROWS task to complete |
| `external` | Waiting on a service, credential, or resource outside the repo |
| `human_decision` | A decision only the human owner can make |
| `capability` | This worker cannot do it — needs a different worker |
| `environment` | Build broken, service down, infrastructure issue |

---

## The 4-Tier Resolution Protocol

Work through every tier in order. Stop at the first tier that resolves the blocker.

---

### Tier 1 — Resolve from Context

**Before anything else, check existing documentation.**

Read in this order:
1. `PROJECT_GOAL.md` — is the answer implied by the stated goal or tech stack?
2. `docs/02-architecture/decisions/ADR-*.md` — has this already been decided?
3. `docs/05-decisions/decision-register.md` — has a similar decision been logged?
4. Recent handoffs in `agent-os/handoffs/` — did a prior worker address this?

If the answer is implied by any of these, **proceed without escalating**. Log what
you inferred and why in your handoff. No blocker file needed.

**Example:** Task requires choosing a date formatting library. PROJECT_GOAL.md lists
`date-fns` in the tech stack. That is the answer. Proceed.

---

### Tier 2 — Assume and Flag

**If tier 1 finds no answer, evaluate reversibility.**

Ask: *If I make the wrong call here, how hard is it to fix?*

| Reversibility | What to do |
|---|---|
| Trivially reversible (rename, swap library, change a constant) | Proceed with best call. Add `**Assumed:** [what you chose and why]` to your handoff. No blocker file. |
| Moderately reversible (refactor required but no data loss) | Same as above — proceed, flag clearly in handoff. |
| Hard to reverse | Move to Tier 3. |

**Example:** Which icon library to use. Not in any docs. Easily swapped later.
Choose the most popular one, note it in the handoff, move on.

---

### Tier 3 — Propose with Deadline

**For decisions that are hard to reverse, write a blocker record and set a deadline.**

The system will auto-resolve using your proposed default if the human does not
respond before the deadline.

**Steps:**

1. Create a blocker record in `agent-os/blockers/` using `blocker-template.md`.
   Fill every field. Write a clear default choice with reasoning tied to existing docs.

2. Set `severity` and `resolve_at` using the deadline ladder:

   | Severity | Minutes | Use when |
   |---|---|---|
   | `trivial` | 5 | Safe, low-consequence, fully reversible |
   | `low` | 15 | Minor consequence, easily swappable |
   | `moderate` | 30 | Some rework if wrong, no data risk |
   | `high` | 60 | Significant rework or security impact |
   | `critical` | 1440 (24h) | Very rare — external commitment or data risk |

3. Move the task file: `tasks/in-progress/ → tasks/blocked/`

4. Update the task file's `blocker_id` field with the new blocker ID.

5. Write a trigger file: `agent-os/triggers/human-decision-[BLOCKER-ID]-[date].md`
   Follow the trigger format in `agent-os/triggers/README.md`.

6. Commit and push. The `on-blocker-deadline` Action will auto-resolve when the
   deadline passes.

7. Claim the next available task in `tasks/ready/`. Do not wait idle.

**Example:** Task requires choosing between PostgreSQL RLS and application-level
multi-tenancy. Not in the ADR. Hard to change later. Write blocker, set severity
`high` (60 min), propose RLS as default with reasoning, move to blocked, claim
next task.

---

### Tier 4 — Hard Block

**Only for decisions that are irreversible or have consequences outside the codebase.**

Criteria for a hard block (ALL must be true):
- The decision cannot be undone without data loss, financial cost, or external impact
- No reasonable default can be proposed
- Proceeding with a wrong choice would require starting over

If these criteria are met:
1. Write the blocker record with `irreversible: true`.
2. Set severity to `critical`.
3. Do NOT set a `resolve_at` deadline — mark it `manual_only: true`.
4. Write an escalation trigger instead of a human-decision trigger.
5. Move task to `tasks/blocked/`.
6. Claim the next available task. Do not wait idle.

**Examples of genuine tier-4 blockers:**
- Sending a real email to a real client
- Executing a destructive database migration on production data
- Making a financial transaction
- A decision that requires legal or compliance review

**Most things are NOT tier 4.** If you are tempted to use tier 4, re-evaluate
tier 3 first. A bad architecture choice is not tier 4 — it is expensive but
reversible.

---

## After a Blocker is Resolved

When the `on-blocker-deadline` Action auto-resolves a blocker, it:
1. Records the chosen option in `docs/05-decisions/decision-register.md`
2. Moves the task from `tasks/blocked/` back to `tasks/ready/`
3. Opens a GitHub issue summarizing what was decided

When you next pick up that task, run `agent-os/skills/resolve-blocker.md` first
to understand what was decided and why before continuing.

---

## Override Instructions

If you want to override a pending auto-resolution before the deadline, create:

`agent-os/blockers/overrides/[BLOCKER-ID]-override.md`

With content:
```
chosen_option: B
reason: [optional explanation]
```

Commit and push. The Action will detect the override file and use your choice
instead of the proposed default.
