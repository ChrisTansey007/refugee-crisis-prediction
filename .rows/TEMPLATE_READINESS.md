# TEMPLATE_READINESS.md

> **Defines what "ready to publish as a GitHub template" means for ROWS.**

---

## Readiness Gates

### Documentation
- [ ] `README.md` exists and explains fork workflow
- [ ] `AGENTS.md` exists and is clear
- [ ] `PROJECT_GOAL.md` is usable as an intake form
- [ ] `TEMPLATE_USAGE.md` has complete fork instructions
- [ ] `HUMAN_OWNER_GUIDE.md` exists
- [ ] `CONTRIBUTING.md` exists
- [ ] `SECURITY.md` exists
- [ ] `CHANGELOG.md` exists
- [ ] `RELEASE_CHECKLIST.md` exists

### Agent OS
- [ ] `agent-os/README.md` exists
- [ ] Task lifecycle folders exist (backlog, ready, claimed, in-progress, review, blocked, done)
- [ ] Task template exists
- [ ] Handoff template exists
- [ ] Role/capability model exists
- [ ] Worker switching docs exist
- [ ] Assignment model docs exist
- [ ] Execution modes docs exist

### Assignment Model
- [ ] `assignment-state.json` is valid
- [ ] `capability-registry.json` is valid
- [ ] `worker-status.json` is valid
- [ ] Role definition files exist
- [ ] Decision register references all ADRs

### Prompt Library
- [ ] `prompt-library/README.md` exists
- [ ] Goal intake prompt exists
- [ ] Solo worker start prompt exists
- [ ] Multi-worker start prompt exists
- [ ] Hybrid primary worker start prompt exists
- [ ] Support worker start prompt exists
- [ ] Reviewer worker start prompt exists
- [ ] Verification worker start prompt exists
- [ ] Reassignment continuation prompt exists
- [ ] Status report request prompt exists
- [ ] Template publish check prompt exists

### Examples
- [ ] `examples/README.md` exists
- [ ] Sample project goal exists
- [ ] Sample task exists
- [ ] Sample handoff exists
- [ ] Sample verification report exists
- [ ] Sample reassignment record exists
- [ ] Sample status report exists

### Script Validation
- [ ] All JSON files parse without error
- [ ] Task validation passes
- [ ] Handoff validation passes
- [ ] Assignment validation passes
- [ ] Decision/ADR validation passes
- [ ] Link validation passes (no broken local links)
- [ ] Placeholder audit passes (no vague placeholders, only intentional markers)
- [ ] Lock validation passes
- [ ] Template readiness validation passes
- [ ] Definition of done check passes
- [ ] Audit script runs successfully

### GitHub Readiness
- [ ] GitHub Actions workflows are syntactically valid
- [ ] Workflows do not depend on secrets
- [ ] Workflows do not deploy anything
- [ ] Workflows do not push commits automatically (except daily status report)
- [ ] PR template exists
- [ ] Issue templates exist

### Security
- [ ] No secrets, keys, or credentials committed
- [ ] `.gitignore` covers env files
- [ ] `SECURITY.md` explains security expectations

### License
- [ ] `LICENSE` file exists at repository root
- [ ] `README.md` links to `./LICENSE`
- [ ] Copyright holder uses intentional `[OWNER_USERNAME]` placeholder

### Template Neutrality
- [ ] No Copilot-specific files exist
- [ ] No empty files exist
- [ ] No application-specific source code in `src/` or `tests/`
- [ ] Examples are clearly marked as examples
- [ ] Placeholders use intentional template markers (not vague markers)

### Final Review
- [ ] Human owner has reviewed all docs
- [ ] Human owner has run `npm run audit`
- [ ] Human owner has verified no worker can self-close
- [ ] Human owner confirms template is ready to publish
