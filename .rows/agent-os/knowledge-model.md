# ROWS Knowledge Model

> This file defines the two-layer model for ROWS: knowledge tells you what is true and why; work tells you what is happening now.

## The Two Layers

### Knowledge Layer

Knowledge is evergreen or slow-moving. It grows, refines, and may be superseded, but it is not treated like disposable session state.

Examples:

- `PROJECT_GOAL.md`
- `PROJECT_CONTEXT.md`
- `AGENTS.md`
- `agent-os/BOOTSTRAP.md`
- `agent-os/agents/`
- `agent-os/skills/`
- `agent-os/protocols/`
- `agent-os/schemas/`
- `agent-os/state/decision-register.json`
- `agent-os/state/dependency-map.json`
- `agent-os/state/knowledge-graph.json`
- `docs/00-project-brief/` through `docs/05-decisions/`
- generated knowledge views such as `docs/04-research/repo-map.md`

### Work Layer

Work is current execution state. It moves through a lifecycle, archives when finished, and may become irrelevant once the underlying work is complete.

Examples:

- `agent-os/tasks/`
- `agent-os/handoffs/`
- `agent-os/blockers/`
- `agent-os/locks/`
- `agent-os/triggers/`
- `agent-os/reassignment/`
- `agent-os/reports/verification/`
- operational reports and time-stamped audits
- `NEXT_TASK.md`

## Reading Order

When starting a session:

1. Read operating knowledge first.
2. Read project knowledge second.
3. Read work-state files third.

In practice, that means:

1. `agent-os/BOOTSTRAP.md`
2. `AGENTS.md`
3. `PROJECT_GOAL.md`
4. `PROJECT_CONTEXT.md`
5. task, blocker, handoff, and lock files relevant to the current work

## Write-Back Rule

Write durable discoveries back to the knowledge layer. Write session continuity and transient progress back to the work layer.

Examples:

- An architecture decision belongs in an ADR and the decision register.
- A reusable operating lesson belongs in `PROJECT_CONTEXT.md`.
- A per-session partial status update belongs in a handoff.
- A blocked execution path belongs in `agent-os/blockers/` and the task file.

## Generated Artifacts

Some knowledge files are generated from machine-readable sources or scans:

- `docs/05-decisions/decision-register.md` is generated from `agent-os/state/decision-register.json`.
- `docs/04-research/repo-map.md` is generated from `agent-os/state/knowledge-graph.json`.

When generated artifacts drift, fix the source or generator rather than hand-editing the generated file unless the template explicitly says otherwise.
