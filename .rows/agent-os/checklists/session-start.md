# Session Start Checklist

> **Complete this checklist at the start of every worker session.**

## Required Reading

- [ ] [`AGENTS.md`](../../AGENTS.md) read in full
- [ ] [`PROJECT_GOAL.md`](../../PROJECT_GOAL.md) read in full
- [ ] [`agent-os/README.md`](../README.md) read
- [ ] [`agent-os/worker-contract.md`](../worker-contract.md) read
- [ ] [`agent-os/state/system-state.json`](../state/system-state.json) read
- [ ] [`agent-os/state/assignment-state.json`](../state/assignment-state.json) read — understand execution mode
- [ ] [`agent-os/state/capability-registry.json`](../state/capability-registry.json) read — understand capabilities
- [ ] [`agent-os/state/worker-status.json`](../state/worker-status.json) read
- [ ] Your worker role file in [`workers/`](../workers/) read
- [ ] The role file for your role in [`roles/`](../roles/) read
- [ ] Your tool adapter file read (e.g., `CLAUDE.md`, `.windsurf/README.md`)

## Task Identification

- [ ] Checked [`tasks/ready/`](../tasks/ready/) for available tasks
- [ ] Identified a task to claim (or confirmed existing claim)
- [ ] Checked [`locks/`](../locks/) for conflicting locks

## Execution Mode

- [ ] Execution mode identified from `assignment-state.json`
- [ ] Confirmed whether acting as: solo worker, primary worker, support worker, verifier, or reviewer
- [ ] Role for this session identified

## Plan Statement

Before making any edits, state:
- [ ] Which task you are working on
- [ ] Your role for this session
- [ ] The execution mode and your place in it
- [ ] Any assumptions you are making
- [ ] Your planned approach

## Related Files

- [`claim-task.md`](./claim-task.md) — Task claiming checklist
- [`before-coding.md`](./before-coding.md) — Pre-coding checklist
