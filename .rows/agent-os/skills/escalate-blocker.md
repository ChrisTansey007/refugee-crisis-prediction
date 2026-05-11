# Skill: Escalate Blocker

Use this skill when a task cannot proceed and tiers 1 and 2 of the blocker
protocol have been exhausted. See `agent-os/protocols/blocker-protocol.md`.

**Do not run this skill until you have confirmed:**
- [ ] Tier 1 checked — PROJECT_GOAL.md, all ADRs, decision-register.md, recent handoffs
- [ ] Tier 2 evaluated — decision is genuinely hard to reverse

---

## Stage 1 — Determine Severity and Deadline

Choose severity based on the nature of the decision:

| Severity | deadline_minutes | Use when |
|---|---|---|
| `trivial` | 5 | Safe, low-consequence, fully reversible in minutes |
| `low` | 15 | Minor consequence, easily swapped in an hour |
| `moderate` | 30 | Some rework if wrong, no data or security risk |
| `high` | 60 | Significant rework, security, or architecture impact |
| `critical` | 1440 | Very rare — external commitment, data risk, major pivot |

Calculate `resolve_at`:
```bash
# For a 'high' severity blocker (60 minutes):
RESOLVE_AT=$(date -u -d "+60 minutes" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u -v+60M +%Y-%m-%dT%H:%M:%SZ)
echo $RESOLVE_AT
```

If `irreversible: true`, set `manual_only: true` and do not set `resolve_at`.
This is a tier-4 hard block — see blocker-protocol.md.

---

## Stage 2 — Get the Next Blocker ID

```bash
# Find the highest existing blocker number
ls agent-os/blockers/BLOCKER-*.md 2>/dev/null \
  | grep -oP 'BLOCKER-\d+' | sort | tail -1 \
  || echo "BLOCKER-0000"
# Increment by 1 for the new ID
```

---

## Stage 3 — Write the Blocker Record

Copy `agent-os/blockers/blocker-template.md` to:
`agent-os/blockers/BLOCKER-[NNNN]-[short-slug].md`

Fill every field. The default choice reasoning must reference an existing document
— not opinion. Leave the Resolution section blank.

---

## Stage 4 — Update the Task File

In the blocked task file, add or update:

```yaml
status: blocked
blocker_id: BLOCKER-[NNNN]
blocker_type: [type]
```

---

## Stage 5 — Move Task to Blocked

```bash
mv agent-os/tasks/in-progress/TASK-[NNNN].md \
   agent-os/tasks/blocked/TASK-[NNNN].md
# Also remove the lock file if present
rm -f agent-os/tasks/in-progress/TASK-[NNNN].lock
```

---

## Stage 6 — Write the Trigger File

For tier-3 (human_decision with deadline):

```bash
cat > agent-os/triggers/human-decision-BLOCKER-[NNNN]-$(date -u +%Y-%m-%d).md << EOF
---
trigger_type: human_decision
blocker_id: BLOCKER-[NNNN]
task_id: TASK-[NNNN]
severity: [severity]
resolve_at: [ISO-8601]
filed_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
filed_by: [worker]
---

## Decision Required: [Short description]

**Task blocked:** TASK-[NNNN]
**Auto-resolves at:** [resolve_at]
**Default choice:** Option [A/B] — [one-line summary]

[2-3 sentence description of the decision needed]

See full blocker record: agent-os/blockers/BLOCKER-[NNNN]-[slug].md

## To Override the Default

Create: agent-os/blockers/overrides/BLOCKER-[NNNN]-override.md
Contents: chosen_option: B
Commit and push before [resolve_at].

## To Accept the Default

Do nothing. Option [A] will be applied automatically at [resolve_at].
EOF
```

For tier-4 (hard block, no deadline):

```bash
cat > agent-os/triggers/escalation-BLOCKER-[NNNN]-$(date -u +%Y-%m-%d).md << EOF
---
trigger_type: escalation
blocker_id: BLOCKER-[NNNN]
task_id: TASK-[NNNN]
severity: critical
manual_only: true
filed_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
filed_by: [worker]
---

## Human Action Required (No Auto-Resolution)

**Task blocked:** TASK-[NNNN]
**This blocker will NOT auto-resolve.**

[Description of what is needed and why it cannot be auto-resolved]

See: agent-os/blockers/BLOCKER-[NNNN]-[slug].md

## To Unblock

1. Resolve the external dependency / make the decision
2. Move the task manually: tasks/blocked/ → tasks/ready/
3. Update the blocker record status to 'human-resolved'
4. Archive this trigger to agent-os/triggers/archive/
5. Commit and push
EOF
```

---

## Stage 7 — Update Worker Status and Commit

```bash
# Update worker-status.json — note you are blocked but continuing
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
   --arg note "Blocked on BLOCKER-[NNNN] — claimed next available task" \
   '.workers.[WORKER].notes = $note | .last_updated = $ts' \
   agent-os/state/worker-status.json > /tmp/ws.json \
   && mv /tmp/ws.json agent-os/state/worker-status.json

git add agent-os/blockers/ agent-os/tasks/ agent-os/triggers/ \
        agent-os/state/worker-status.json
git commit -m "chore(blocker): BLOCKER-[NNNN] filed for TASK-[NNNN] — [short description]"
git push origin [current-branch]
git ls-remote origin [current-branch]
```

---

## Stage 8 — Claim the Next Task (Rule 24)

Do not wait idle. Return to the worker loop immediately:

```bash
cat agent-os/skills/worker-loop.md
# Go to SCAN step — find next ready task
ls agent-os/tasks/ready/
```
