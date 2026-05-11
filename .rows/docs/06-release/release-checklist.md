# Release Checklist

> **Complete this checklist before every release.**

## Pre-Release

- [ ] All tasks for this release are in `done/`.
- [ ] Full test suite passes (`npm test`).
- [ ] Linting passes (`npm run lint`).
- [ ] Definition of done check passes (`npm run check:dod`).
- [ ] All handoffs for release tasks are archived.
- [ ] Changelog updated with all changes.
- [ ] Version bumped in `package.json`.
- [ ] Documentation reviewed and up to date.
- [ ] No known critical bugs.

## During Release

- [ ] Release branch created and PR approved.
- [ ] PR merged to `main`.
- [ ] Git tag created (`vX.Y.Z`).
- [ ] Tag pushed to remote.

## Post-Release

- [ ] Deployment successful.
- [ ] Smoke tests pass in production.
- [ ] Monitoring confirms no errors.
- [ ] Release announced (if applicable).

## Related Files

- [`release-plan.md`](./release-plan.md) — Release plan
- [`changelog.md`](./changelog.md) — Changelog
- [`../03-development/release-process.md`](../03-development/release-process.md) — Release process
