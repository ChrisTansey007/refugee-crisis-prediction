# Skill: Resolve Blocker

Use this skill when you pick up a task from `tasks/ready/` that was previously
in `tasks/blocked/`. The blocker was resolved by the auto-deadline system, a
human override, or a human manual resolution. You must understand what was decided
before continuing the task.

---

## Stage 1 — Find the Blocker Record

Read the task file and get the `blocker_id`:

```bash
cat agent-os/tasks/ready/TASK-[NNNN].md | grep blocker_id
# Result: blocker_id: BLOCKER-[NNNN]
```

Read the full blocker record:

```bash
cat agent-os/blockers/BLOCKER-[NNNN]-*.md
```

---

## Stage 2 — Understand the Resolution

Check the Resolution section at the bottom of the blocker record:

| Field | What to look for |
|---|---|
| `Method: auto` | The deadline passed. Default choice was applied. |
| `Method: override` | Human created an override file before the deadline. |
| `Method: human` | Human manually resolved — check trigger archive for notes. |

Read the **Chosen option** and its consequences from the Options section.

---

## Stage 3 — Check the Decision Register

The resolution was logged to `docs/05-decisions/decision-register.md`. Confirm
the entry is there and read the full context:

```bash
grep -A 10 "BLOCKER-[NNNN]" docs/05-decisions/decision-register.md
```

---

## Stage 4 — Load the Decision into Context

Before writing a single line of code, state explicitly:

> "BLOCKER-[NNNN] was resolved via [method]. The chosen option was [X].
> This means I will [specific implementation consequence]."

If anything about the chosen option is unclear, check the trigger archive:

```bash
ls agent-os/triggers/archive/ | grep "BLOCKER-[NNNN]"
cat agent-os/triggers/archive/[trigger-file]
```

---

## Stage 5 — Clear the Blocker Fields and Continue

Update the task file — remove the blocked status:

```yaml
status: in-progress
blocker_id: ~
blocker_type: ~
blocker_resolved_at: [ISO-8601]
blocker_resolution: [one-line summary of what was decided]
```

Proceed with the task using the decided option. Follow the standard task
execution flow from `agent-os/skills/worker-loop.md` Stage 5 onward.
