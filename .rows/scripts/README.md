# Scripts

Lightweight Node.js ESM validation and automation scripts for the ROWS system. All scripts use only built-in Node.js modules — no external dependencies required.

## Available Scripts

| Script | Purpose | npm run |
|--------|---------|---------|
| `agentctl.mjs` | Print available commands and system info | — |
| `claim-task.mjs` | Validate and assist with task claiming | — |
| `move-task.mjs` | Move tasks between lifecycle folders | — |
| `validate-json.mjs` | Recursively validate all JSON files | `validate:json` |
| `validate-task.mjs` | Validate task file structure | `validate:tasks` |
| `validate-handoff.mjs` | Validate handoff file structure | `validate:handoffs` |
| `validate-assignments.mjs` | Validate assignment state consistency | `validate:assignments` |
| `validate-decisions.mjs` | Validate ADR/decision file consistency | `validate:decisions` |
| `validate-links.mjs` | Scan Markdown files for broken relative links | `validate:links` |
| `validate-placeholders.mjs` | Audit for vague placeholders | `validate:placeholders` |
| `validate-locks.mjs` | Validate lock JSON files | `validate:locks` |
| `validate-template-readiness.mjs` | Check template readiness gates | `validate:template` |
| `generate-status-report.mjs` | Generate a Markdown status report | `status:generate` |
| `generate-assignment-report.mjs` | Generate assignment summary report | `assignments:report` |
| `check-definition-of-done.mjs` | Check DoD for tasks in review | `check:dod` |
| `list-tasks.mjs` | List task files by lifecycle state | `list:tasks` |
| `list-workers.mjs` | List worker statuses | `list:workers` |
| `list-capabilities.mjs` | List all capabilities from registry | `list:capabilities` |
| `list-modes.mjs` | Show current execution mode | `list:modes` |
| `audit-agent-os.mjs` | Run comprehensive audit of all checks | `audit` |

## Usage

All scripts are ESM (`.mjs`) and use only `fs`, `path`, and other built-in Node.js modules. Run directly:

```bash
node scripts/validate-task.mjs
```

Or via npm:

```bash
npm run validate:tasks
```

## Related Files

- [`../package.json`](../package.json) — npm scripts configuration
- [`../agent-os/`](../agent-os/) — The agent operating system
