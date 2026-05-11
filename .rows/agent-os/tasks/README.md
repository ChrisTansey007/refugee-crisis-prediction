# Tasks — Task Queue

This directory contains the task queue for the ROWS system. Tasks are Markdown files that move through lifecycle folders as they progress.

## Lifecycle Folders

| Folder | Meaning |
|--------|---------|
| [`backlog/`](./backlog/) | Proposed tasks, not yet approved |
| [`ready/`](./ready/) | Approved and claimable by any worker |
| [`claimed/`](./claimed/) | Claimed by a worker, lock created |
| [`in-progress/`](./in-progress/) | Work actively happening |
| [`review/`](./review/) | Awaiting independent verification |
| [`blocked/`](./blocked/) | Cannot proceed due to dependency or issue |
| [`done/`](./done/) | Verified and complete |

## Task Template

Use [`task-template.md`](./task-template.md) to create new tasks.

## Related Files

- [`../task-lifecycle.md`](../task-lifecycle.md) — Full lifecycle documentation
- [`../worker-contract.md`](../worker-contract.md) — Worker claiming rules
