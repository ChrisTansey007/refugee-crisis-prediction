> **New to this repo?** Read `agent-os/BOOTSTRAP.md` first.

# Prompt: Status Report Request

> **Give this prompt to ask a worker to summarize current repo state.**

---

Read the following files:

1. `agent-os/state/system-state.json`
2. `agent-os/state/assignment-state.json`
3. `agent-os/state/worker-status.json`
4. `agent-os/state/risk-register.json`
5. `agent-os/state/decision-register.json`

Then scan:

6. `agent-os/tasks/` — count tasks in each lifecycle folder
7. `agent-os/handoffs/active/` — count active handoffs
8. `agent-os/reports/` — note recent reports

Your job:

Generate a summary of the current repo state from files only. Do not rely on memory.

Include:
- Execution mode
- Active workers and their statuses
- Task counts by state (backlog, ready, claimed, in-progress, review, blocked, done)
- Active assignments
- Recent handoffs
- Open risks
- Recent decisions

Output the summary as Markdown. You may also run `npm run status:generate` to produce the standard status report.
