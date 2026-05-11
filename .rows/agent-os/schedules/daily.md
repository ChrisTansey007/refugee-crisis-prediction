# Daily Schedule

> **Daily cadence for the ROWS system.**

## Morning (Start of Day)

- [ ] Review new handoffs in [`handoffs/active/`](../handoffs/active/)
- [ ] Check [`state/worker-status.json`](../state/worker-status.json) for active workers
- [ ] Review any tasks moved to [`tasks/review/`](../tasks/review/) overnight
- [ ] Check for stale locks in [`locks/`](../locks/) (expired > 24 hours)

## During Day

- [ ] Workers claim and execute tasks from [`tasks/ready/`](../tasks/ready/)
- [ ] Workers write handoffs at end of each session
- [ ] Human reviews completed work as it arrives in `review/`

## End of Day

- [ ] All active workers have written handoffs
- [ ] No tasks stuck in `claimed/` without progress
- [ ] Quick scan of [`tasks/blocked/`](../tasks/blocked/) for new blockers
- [ ] Run `npm run status:generate` for daily summary

## Related Files

- [`weekly.md`](./weekly.md) — Weekly schedule
- [`audits.md`](./audits.md) — Audit schedule
