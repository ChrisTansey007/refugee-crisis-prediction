# Claim Task Checklist

> **Complete this checklist when claiming a task.**

## Pre-Claim

- [ ] Execution mode checked in [`state/assignment-state.json`](../state/assignment-state.json)
- [ ] Task selected from [`tasks/ready/`](../tasks/ready/)
- [ ] Task file read and understood
- [ ] Required capabilities match your strengths
- [ ] Responsible role matches your active role
- [ ] Acceptance criteria are clear and testable
- [ ] No conflicting locks in [`locks/`](../locks/)
- [ ] Task is appropriate for your worker type and capabilities

## Claim Process

- [ ] Task file moved from `ready/` to [`tasks/claimed/`](../tasks/claimed/)
- [ ] Lock file created using [`locks/lock-template.json`](../locks/lock-template.json)
- [ ] Lock file includes: task_id, claimed_by, files_expected, expires_at
- [ ] Lock file saved to [`locks/`](../locks/)
- [ ] Your entry in [`state/worker-status.json`](../state/worker-status.json) updated (include active_roles)
- [ ] Task file's `Current claimed worker` updated
- [ ] [`state/assignment-state.json`](../state/assignment-state.json) updated if needed

## Branch Setup

- [ ] Branch name follows [`branch-strategy.md`](../branch-strategy.md)
- [ ] Branch created from `main`
- [ ] Branch checked out locally

## Begin Work

- [ ] Task moved from `claimed/` to [`tasks/in-progress/`](../tasks/in-progress/)
- [ ] Ready to begin implementation

## Related Files

- [`session-start.md`](./session-start.md) — Session start checklist
- [`before-coding.md`](./before-coding.md) — Pre-coding checklist
