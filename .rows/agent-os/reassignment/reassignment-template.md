# Reassignment Record

> **Use this template when reassigning a task from one worker to another.**

---

# Reassignment: [TASK-ID]

## Metadata

- **Task ID:** [TASK-XXXX]
- **Previous worker:** [worker name]
- **New worker:** [worker name]
- **Requested by:** [worker name | human | coordinator]
- **Date:** [YYYY-MM-DD]

## Reason for Reassignment

[Clear explanation of why the task is being reassigned. Reference specific conditions from the worker-switching-protocol.]

## Current Task Status

- **Status:** [backlog | ready | claimed | in-progress | review | blocked]
- **What has been completed:** [summary]
- **What remains:** [summary]

## Current Lock Status

- **Lock file:** [path or "none"]
- **Lock status:** [active | stale | removed]
- **Lock expiration:** [date or "N/A"]

## Files Already Changed

| File | Action | Status |
|------|--------|--------|
| `path/to/file` | created/modified | committed/uncommitted |

## Handoff Available

- **Handoff file:** [path or "none — reconstructed by human"]
- **Handoff quality:** [complete | partial | reconstructed]

## Verification Available

- **Verification report:** [path or "none"]
- **Test results:** [summary or "none"]
- **Evidence files:** [paths or "none"]

## Known Risks

- [Risk 1]
- [Risk 2]
- [Risks introduced by reassignment itself]

## Required Reading for New Worker

1. [`AGENTS.md`](../../AGENTS.md)
2. [`agent-os/assignment-model.md`](../assignment-model.md)
3. The task file: `agent-os/tasks/[folder]/[TASK-ID].md`
4. The previous handoff: [path]
5. Verification evidence: [paths]
6. Changed files: [list key files to inspect]

## Continuation Instructions

[Specific, actionable instructions for the new worker. What to do first, what to watch out for, what decisions are pending.]

## Approval Status

- **Human approved:** [yes | no | pending]
- **Coordinator proposed:** [yes | no]
- **New worker accepted:** [yes | no | pending]

## Notes

[Any additional context for the new worker or future reference.]
