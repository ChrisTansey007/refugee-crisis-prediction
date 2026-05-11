# agent-os/blockers/overrides/

Human override files for pending blocker resolutions.

## How to Override

If a tier-3 blocker is pending auto-resolution and you want a different choice
than the proposed default, create a file here **before the `resolve_at` deadline**:

**Filename:** `[BLOCKER-ID]-override.md`
**Example:** `BLOCKER-0001-override.md`

**Contents:**
```
chosen_option: B
reason: We already have a Firebase account from another project — reuse it
```

Commit and push. The `on-blocker-deadline` Action will detect this file on its
next run (within 5 minutes) and apply your choice instead of the default.

## After Override

The Action will:
1. Record your choice in `docs/05-decisions/decision-register.md`
2. Move the task from `tasks/blocked/` to `tasks/ready/`
3. Mark the blocker record as `overridden`
4. Open a GitHub issue confirming the resolution

You do not need to delete the override file — the Action archives it.

## Rules

- Override files must be created before the `resolve_at` timestamp
- After the deadline, the default is applied automatically — overrides are ignored
- For tier-4 (hard) blockers, there is no deadline — the task stays blocked until
  you manually resolve it and move the task to `tasks/ready/`
