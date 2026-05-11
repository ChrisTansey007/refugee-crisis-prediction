# Execution Modes

> **The ROWS system supports three execution modes: Solo Worker, Multi-Worker, and Hybrid. The active mode is recorded in `agent-os/state/assignment-state.json`.**

---

## Solo Worker Mode

One worker takes the project from goal intake through planning, task creation, implementation, documentation, and verification preparation.

### Rules

- The worker must still create task files.
- The worker must still use lifecycle folders (`backlog/`, `ready/`, `claimed/`, `in-progress/`, `review/`, `done/`).
- The worker must still create handoffs for every session.
- The worker must still produce verification evidence.
- The worker must not self-close final completion without independent review, automated validation, or human approval.
- The worker must make all state durable in repo files.
- The worker must not rely on private chat memory as durable project memory.

### Best For

- Small projects (single feature, prototype, MVP).
- First project setup and initial scaffolding.
- Documentation-heavy builds.
- Early planning and architecture.
- Solo developers using AI assistance.
- Learning the ROWS system.

### Limitations

- No independent worker review (must use automated validation or human review).
- Single point of failure if the worker becomes unavailable.
- Risk of blind spots without a second perspective.
- Reassignment requires reconstructing context from handoffs.

### Activation

Set in `agent-os/state/assignment-state.json`:

```json
{
  "mode": "solo"
}
```

---

## Multi-Worker Mode

Multiple workers divide work by task, role, capability, or phase.

### Rules

- Each worker claims one task at a time unless explicitly approved.
- Workers must respect locks.
- Workers must update handoffs.
- Workers must avoid file collisions (see [`file-ownership.md`](./file-ownership.md)).
- Workers must record verification evidence.
- Review should be performed by a different worker when possible.
- No worker may close its own task without independent verification.
- All continuation context must be written into repo files.
- When two or more workers are active, use separate git worktrees to prevent file collisions.

### Best For

- Larger applications with multiple components.
- Parallel frontend/backend work.
- Research plus implementation happening concurrently.
- Testing and documentation in parallel with development.
- Review-heavy projects requiring independent verification.
- Teams using multiple AI tools.

### Coordination

- Hermes may propose task decomposition and worker assignments (but does not command).
- The human owner reviews and approves task routing.
- Locks prevent file collisions.
- Handoffs enable cross-worker continuity.
- Status reports (`npm run status:generate`) provide visibility.

### Activation

Set in `agent-os/state/assignment-state.json`:

```json
{
  "mode": "multi-worker"
}
```

---

## Hybrid Mode

One primary worker drives the project while other workers perform specialized support.

### Common Patterns

| Primary Worker | Support Workers | Pattern |
|---------------|-----------------|---------|
| Windsurf | Claude, Gemini, Antigravity | Windsurf implements repo changes; Claude reviews architecture and docs; Gemini performs research; Antigravity verifies UI |
| Codex | Claude, Hermes | Codex writes code; Claude reviews; Hermes decomposes tasks |
| Claude | Codex, Windsurf, Antigravity | Claude plans architecture; Codex and Windsurf implement; Antigravity verifies |

### Rules

- The primary worker is responsible for overall progress.
- Support workers claim specific sub-tasks or review tasks.
- The primary worker must still write handoffs.
- Support workers must write handoffs for their contributions.
- The primary worker must not self-close without independent review.
- Support workers may act as independent reviewers for the primary worker.

### Best For

- Projects where one tool has the best repo access but needs specialized help.
- Complex projects requiring diverse capabilities.
- Projects where the human wants one primary driver with specialized support.
- Iterative development with periodic review checkpoints.

### Activation

Set in `agent-os/state/assignment-state.json`:

```json
{
  "mode": "hybrid",
  "active_workers": ["windsurf"],
  "notes": ["Windsurf is primary. Claude for architecture review. Antigravity for UI verification."]
}
```

---

## Mode Comparison

| Aspect | Solo | Multi-Worker | Hybrid |
|--------|------|-------------|--------|
| Worker count | 1 | 2+ | 1 primary + N support |
| Independent review | Automated or human | Different worker | Support worker or human |
| Coordination overhead | Minimal | Moderate | Low-moderate |
| Continuity risk | Medium (handoffs required) | Low (multiple workers) | Low-medium |
| Best project size | Small | Large | Medium-large |
| Setup complexity | Low | Medium | Low-medium |

---

## Switching Modes

You can switch modes at any time by updating `assignment-state.json`. Considerations:

### Solo → Multi-Worker

- Ensure all handoffs are up to date.
- Create task files for remaining work.
- Move tasks to `ready/` for other workers to claim.
- Update `assignment-state.json`.

### Multi-Worker → Solo

- Ensure all active workers write handoffs.
- Close or reassign other workers' locks.
- The solo worker reads all handoffs before continuing.
- Update `assignment-state.json`.

### Hybrid → Solo or Multi-Worker

- Support workers write final handoffs.
- Primary worker reads all support handoffs.
- Update `assignment-state.json` to the new mode.

---

## Related Files

- [`assignment-model.md`](./assignment-model.md) — Full assignment hierarchy
- [`worker-switching-protocol.md`](./worker-switching-protocol.md) — Reassignment protocol
- [`task-routing-rules.md`](./task-routing-rules.md) — Task flow through the system
- [`worktree-strategy.md`](./worktree-strategy.md) — Worktree rules for parallel execution
- [`state/assignment-state.json`](./state/assignment-state.json) — Current mode and assignments
