# Universal Skills Index

Load these files in order. **Required** items must be in your active context before you claim any task. **Conditional** items depend on the work ahead. **Optional** items are reference — load if relevant.

---

## Phase 0 — System Understanding (load first, always)

| Priority | File | What It Gives You |
|---|---|---|
| **Required** | `AGENTS.md` | Full ruleset, all 26+ rules, the law of this repo |
| **Required** | `agent-os/knowledge-model.md` | Knowledge layer vs work layer — how to read the repo in the right order |
| **Required** | `agent-os/state/system-state.json` | Current phase, project name, active goals |
| **Required** | `agent-os/state/worker-status.json` | Who else is active, what they are working on |
| **Required** | `agent-os/state/assignment-state.json` | How work is assigned (solo/hybrid/multi) |
| **Required** | `PROJECT_GOAL.md` | The project's purpose — your north star for all decisions |
| **Required** | `PROJECT_CONTEXT.md` | Distilled durable project context — read this before raw handoff history |

---

## Phase 1 — Task Lifecycle (load before claiming any task)

| Priority | File | What It Gives You |
|---|---|---|
| **Required** | `agent-os/tasks/task-template.md` | Task file format, every field explained |
| **Required** | `agent-os/skills/claim-task.md` | How to claim a task correctly |
| **Required** | `agent-os/skills/complete-task.md` | How to close a task, push gate (Rule 23) |
| **Required** | `agent-os/skills/enrich-task.md` | How to keep tasks atomic with a current context snapshot |
| **Required** | `agent-os/skills/session-close.md` | How to end a session cleanly |

---

## Phase 2 — Blocker Handling (load before starting first task)

| Priority | File | What It Gives You |
|---|---|---|
| **Required** | `agent-os/protocols/blocker-protocol.md` | 4-tier resolution protocol, decision flowchart |
| **Required** | `agent-os/skills/escalate-blocker.md` | How to file and escalate a blocker |
| **Required** | `agent-os/skills/resolve-blocker.md` | How to pick up a task after a blocker clears |
| **Required** | `agent-os/blockers/README.md` | Blocker directory structure and lifecycle |

---

## Phase 3 — Orientation (load after system understanding)

| Priority | File | What It Gives You |
|---|---|---|
| **Conditional** | `docs/05-decisions/decision-register.md` | Past decisions — load if you are about to make an architectural choice |
| **Conditional** | `docs/04-research/repo-map.md` | The connection graph — load if you need dependency or orphan visibility |
| **Conditional** | `agent-os/tasks/backlog/` | Full task queue — load if you need to choose what to work on |
| **Conditional** | `agent-os/tasks/in-progress/` | Active work — load if you are resuming after a gap |
| **Conditional** | `agent-os/handoffs/` | Read task-specific handoffs when resuming unfinished work or if PROJECT_CONTEXT is missing detail |
| **Conditional** | `docs/01-architecture/` | Architecture docs — load if you will be making structural decisions |

---

## Phase 4 — Reference (load on demand)

| Priority | File | What It Gives You |
|---|---|---|
| Optional | `agent-os/skills/create-task.md` | How to write a new task file |
| Optional | `agent-os/skills/distill-handoffs.md` | How to promote durable handoff context into PROJECT_CONTEXT.md |
| Optional | `agent-os/skills/update-knowledge-graph.md` | How to refresh backlinks, repo-map, and orphan visibility |
| Optional | `agent-os/skills/update-state.md` | How to update system-state and worker-status |
| Optional | `agent-os/triggers/README.md` | Trigger file formats, when to write them |
| Optional | `agent-os/blockers/blocker-template.md` | Blocker file format reference |
| Optional | `docs/04-adr/` | Architecture Decision Records |

---

## Loading Order for a Fresh Session

If this is your first session in this repo, load in this order:

1. Everything in Phase 0 (understand the system and project)
2. Everything in Phase 1 (understand the task lifecycle)
3. Everything in Phase 2 (understand how to handle blockers)
4. `PROJECT_CONTEXT.md` — use distilled knowledge before raw history
5. `agent-os/handoffs/` — read the most relevant active handoff if one exists for your task
6. `agent-os/tasks/backlog/` — scan what is ready
7. Your agent-specific `reading-list.md` for any additions

If you are resuming mid-session, load Phase 0 + Phase 2 + `agent-os/tasks/in-progress/` for your claimed tasks.
