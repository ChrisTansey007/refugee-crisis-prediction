# Audit Schedule

> **Regular audits to maintain system health.**

## Daily (Automated)
- [ ] CI runs `validate-agent-os.yml`
- [ ] CI checks for stale tasks

## Weekly
- [ ] Review all locks — remove stale ones
- [ ] Check `blocked/` tasks — any stuck > 7 days?
- [ ] Review `claimed/` tasks — any stuck > 48 hours?
- [ ] Verify `worker-status.json` matches actual state

## Per Sprint
- [ ] Full task queue audit — are tasks well-formed?
- [ ] Handoff quality audit — are handoffs complete?
- [ ] Risk register review — new risks? resolved risks?
- [ ] Decision register review — new ADRs? superseded ADRs?

## Ad-Hoc
- [ ] After any merge conflict
- [ ] After any worker non-compliance incident
- [ ] Before major releases

## Related Files
- [`daily.md`](./daily.md), [`weekly.md`](./weekly.md), [`sprint.md`](./sprint.md)
