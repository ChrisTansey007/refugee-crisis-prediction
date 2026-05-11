# Handoff Template

> **Every worker session must produce a handoff using this template. Fill in ALL sections.**

---

# Handoff: [TASK-ID]

## Metadata

- **Task ID:** [TASK-XXXX]
- **Worker:** [codex | claude | gemini | windsurf | antigravity | hermes]
- **Role Performed:** [ROLE_NAME]
- **Capabilities Used:** [list capabilities]
- **Date/Time:** [YYYY-MM-DD HH:MM]
- **Session Status:** [complete | in-progress | blocked]

## Summary of Work

[2-4 sentences describing what was accomplished in this session.]

## Related ADRs

- [ADR-XXXX] — [If this session materially depended on or changed the interpretation of an ADR]

## Related Decisions

- [Decision ID or blocker record] — [If this session carried or resolved a durable decision]

## Files Changed

| File | Action | Description |
|------|--------|-------------|
| `path/to/file` | created/modified/deleted | What changed and why |

## Commands Run

```
$ command1
$ command2
```

## Tests Run

- [ ] Unit tests: [pass/fail count]
- [ ] Integration tests: [pass/fail count]
- [ ] Linting: [pass/fail]

## Evidence Produced

- [Test output saved to `reports/verification/...`]
- [Screenshots saved to `reports/verification/...`]
- [Other evidence]

## What Changed

[Detailed description of what was implemented or modified.]

## What Did Not Change

[Things that were intentionally left unchanged, or that were planned but not completed.]

## Known Issues

- [Issue 1 — description and impact]
- [Issue 2]

## Risks

- [Risk 1 — likelihood and impact]
- [Risk 2]

## Next Recommended Worker

[Which worker type should pick up this task next, if applicable. Include recommended role.]

## Reassignment Notes

[If this task is being reassigned, note the reason, what the new worker should read first, and any risks specific to the handoff.]

## Next Steps

1. [Step 1 — actionable and specific]
2. [Step 2]
3. [Step 3]

## Verification Notes

- [ ] Self-check completed
- [ ] Acceptance criteria reviewed
- [ ] Ready for independent review: [YES/NO]

## Continuity Notes

[Anything the next worker needs to know to continue without relying on private chat memory. Include enough context for a different worker to pick up seamlessly.]

## Additional Notes

[Anything else the next worker or human should know.]
