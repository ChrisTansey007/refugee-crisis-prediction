# Release Process

> **Customize after forking. How to release [PROJECT_NAME].**

## Versioning

We follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

- **MAJOR:** Breaking changes.
- **MINOR:** New features, backward compatible.
- **PATCH:** Bug fixes, backward compatible.

## Release Steps

1. **Create release branch:** `release/vX.Y.Z`
2. **Update version:** Bump version in `package.json` and any other version files.
3. **Update changelog:** Add entries to [`../06-release/changelog.md`](../06-release/changelog.md).
4. **Run full test suite:** `npm test`
5. **Run definition of done check:** `npm run check:dod`
6. **Create PR:** Merge release branch into `main`.
7. **Tag release:** `git tag vX.Y.Z && git push --tags`
8. **Deploy:** Follow deployment instructions for [DEPLOYMENT_TARGET].
9. **Verify:** Run smoke tests against production.

## Hotfix Process

1. Branch from `main`: `hotfix/description`
2. Fix, test, and PR into `main`.
3. Tag as patch version.
4. Deploy immediately.

## Related Files

- [`../06-release/release-plan.md`](../06-release/release-plan.md) — Release plan
- [`../06-release/release-checklist.md`](../06-release/release-checklist.md) — Release checklist
- [`../06-release/changelog.md`](../06-release/changelog.md) — Changelog
