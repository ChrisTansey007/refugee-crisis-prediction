# Autonomous Continuation Protocol

> This document describes the full system design for keeping ROWS agents
> running without human intervention. It covers the three-layer architecture:
> in-session loops, inter-session triggers, and scheduled sweeps.

---

## The problem this solves

Without autonomous continuation, ROWS agents work in isolated bursts:
1. Human starts a session.
2. Agent does work.
3. Session ends.
4. All work stops until the human starts a new session.

This means the repo is only as productive as the human's availability.
The goal is a system where work continues automatically between human sessions.

---

## Three-layer architecture

```
Layer 1: In-session loop (worker-loop skill)
  └─ Agent keeps working until no tasks remain or context runs out

Layer 2: Inter-session triggers (triggers/ directory + GitHub Actions)
  └─ When a session ends, it leaves a trigger that wakes the next session

Layer 3: Scheduled sweeps (GitHub Actions cron + Cowork scheduled tasks)
  └─ Daily/hourly jobs that triage backlog, promote tasks, and notify
```

---

## Layer 1: In-session loop

Defined in `agent-os/skills/worker-loop.md`. The key principle:

> After every task closes, the agent immediately looks for the next task.
> It never exits unless explicitly told to (idle trigger or stop trigger).

**Human action required:** Start the first session. After that, the agent
loops autonomously until it idles.

---

## Layer 2: Inter-session triggers

When a session ends with no more work (or abruptly), it writes a trigger file
to `agent-os/triggers/`. The trigger file is a signal to the next session.

### Trigger types

| File | Meaning |
|---|---|
| `idle-<worker>-<date>.md` | No tasks remain; describe what unblocks next |
| `escalation-<task>-<date>.md` | Task blocked; human decision needed |
| `handoff-ready-<task>-<date>.md` | Task paused mid-flight; ready for pickup |
| `stop-<worker>.md` | Human-written; tells the named worker to idle |
| `wake-<worker>-<date>.md` | Written by another agent to request a worker |

### How GitHub Actions uses triggers

`.github/workflows/on-trigger.yml` fires on any push that adds a file to
`agent-os/triggers/`. It can:
- Post a GitHub issue comment summarizing the trigger.
- Send a notification (email, Slack, webhook) to the human owner.
- *(Future)* Call an API to automatically spin up a new agent session.

The human sees the notification, opens Claude/Cowork, and the trigger file
tells the new session exactly what to do first.

---

## Layer 3: Scheduled sweeps

### GitHub Actions cron (`daily-triage.yml`)

Runs daily at 09:00 UTC. Does not execute work — it is a triage and
notification job only:
1. Reads `tasks/backlog/` — lists tasks whose blockers are now resolved.
2. Reads `tasks/in-progress/` — flags tasks with no push in >48 hours (stale).
3. Reads `agent-os/triggers/` — summarizes open triggers.
4. Opens a GitHub Issue titled "Daily ROWS Triage — <date>" with the summary.

The human owner reads the issue and decides whether to start an agent session.

### Cowork scheduled tasks

Using the Cowork `scheduled-tasks` MCP, a recurring task can be configured
to run a ROWS triage prompt on a schedule (e.g., every weekday morning).
This gives the human a ready-to-go session with full context each morning.

---

## Adding autonomous spin-up (future)

For full autonomy (no human needed between sessions), the system needs an
external trigger that can start a Claude session. Options:
- **GitHub Actions + Anthropic API:** When a `wake-*` trigger is pushed,
  a GitHub Action calls the Anthropic API to start a new agent session with
  the worker-loop skill pre-loaded.
- **Webhook + n8n/Zapier:** Push triggers a workflow that opens a Cowork
  session with a pre-written prompt.
- **Scheduled Cowork session:** A Cowork scheduled task runs `worker-loop`
  every N hours.

This layer is intentionally left for the human owner to configure, as it
requires API keys and external service setup beyond the repo itself.

---

## Summary: what runs automatically vs. what requires a human

| Action | Automatic | Requires human |
|---|---|---|
| Continue working after a task closes | Yes (worker-loop) | No |
| Promote backlog tasks | Yes (auto-promote) | No |
| Write idle/escalation triggers | Yes (worker-loop exit) | No |
| Notify human of triggers | Yes (GitHub Actions) | No |
| Start a new session after idle | No | Yes (for now) |
| Spin up agent via API | Optional (future) | Setup only |

---

## Related files

- [skills/worker-loop.md](../skills/worker-loop.md)
- [skills/auto-promote.md](../skills/auto-promote.md)
- [skills/session-close.md](../skills/session-close.md)
- [triggers/README.md](../triggers/README.md)
- [../../.github/workflows/](../../.github/workflows/)
- [../../AGENTS.md](../../AGENTS.md) Rules 23–24
