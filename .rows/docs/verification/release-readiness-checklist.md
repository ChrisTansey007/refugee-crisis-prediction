# Release Readiness Checklist — ROWS

> **Purpose:** Independent verification checklist to determine when this repository is ready to be published as a polished public template.
>
> **Scope:** Beyond the existing `@/Users/theca/CascadeProjects/windsurf-project-7/RELEASE_CHECKLIST.md` (which covers structural completeness), this file adds gates for **modern agent compatibility**, **documentation cohesion**, **safety posture**, and **practical first-run experience**.
>
> **How to use:** Each gate is binary (PASS / FAIL). The repo is release-ready only when **all** mandatory gates pass and **most** recommended gates pass.
>
> **Companion files:**
> - `@/Users/theca/CascadeProjects/windsurf-project-7/RELEASE_CHECKLIST.md` (existing structural release checklist)
> - `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/agent-template-readiness-audit.md` (audit findings)
> - `@/Users/theca/CascadeProjects/windsurf-project-7/docs/backlog/template-improvement-backlog.md` (gap-closing tasks)

---

## 1. Status Snapshot Template

When running this checklist, paste this snapshot at the top of a copy and fill in:

```
Run date:           YYYY-MM-DD
Run by:             [worker / human]
Repo commit:        <short SHA>
npm run audit:      PASS / FAIL (current: PASS as of 2026-05-06)
Release verdict:    READY / NOT READY
Blocker count:      N
Recommended gaps:   N
```

---

## 2. Mandatory Gates (Must Pass)

These gates must be PASS before publishing as a template. Any FAIL is a blocker.

### 2.1 Structural Integrity

| Gate | Check | Pass criterion | Tool |
|------|-------|----------------|------|
| S1 | All files referenced in adapter and worker docs exist | No broken file references | `npm run validate:links` |
| S2 | All paired JSON ↔ MD files agree | Decision register, capability registry consistent | `npm run validate:agent-os` (extend to cover this) |
| S3 | All required template files exist | `validate-template-readiness.mjs` passes | `npm run validate:template` |
| S4 | No vague placeholders | Zero matches for tokens in the script's `VAGUE` array outside `reports/` | `npm run validate:placeholders` |
| S5 | No Copilot files | `.copilot`, `.copilot-instructions.md`, `.github/copilot-instructions.md` absent | `npm run validate:template` |
| S6 | All JSON parses | All `.json` valid | `npm run validate:json` |
| S7 | All locks valid | `validate-locks.mjs` passes | `npm run validate:locks` |
| S8 | Definition of done passes for review tasks | `check-definition-of-done.mjs` passes | `npm run check:dod` |
| S9 | All ADRs are valid | `validate-decisions.mjs` passes | `npm run validate:decisions` |
| S10 | `npm run audit` passes end-to-end | All scripts return exit 0 | `npm run audit` |

### 2.2 Reference Integrity

| Gate | Check | Pass criterion |
|------|-------|----------------|
| R1 | `.env.example` exists | File present at repo root |
| R2 | `.claude/rules/` either populated or its README updated | No file references `.claude/rules/*.md` if those files don't exist |
| R3 | `package.json` defines `test` and `lint` scripts | Both scripts exist, exit 0 on a fresh clone |
| R4 | `package.json` declares `engines.node` | `>=20` recommended |
| R5 | Sample verification report references resolve | Either files exist in `agent-os/reports/verification/` or the report explicitly marks paths as illustrative |
| R6 | `.gitignore` references real files only | `.env*` patterns harmless even without `.env.example`; references in setup docs match reality |
| R7 | `LICENSE` `[OWNER_USERNAME]` is intentional placeholder | Listed in `validate-placeholders.mjs` INTENTIONAL array |
| R8 | `.github/CODEOWNERS` `@OWNER_USERNAME` is intentional placeholder | Listed in INTENTIONAL array (or alternative comment-only placeholder) |

### 2.3 Process Integrity

| Gate | Check | Pass criterion |
|------|-------|----------------|
| P1 | No-self-close rule documented in ≥3 places consistently | `AGENTS.md`, `worker-contract.md`, `definition-of-done.md` agree |
| P2 | Lifecycle is exhaustive | `backlog/`, `ready/`, `claimed/`, `in-progress/`, `review/`, `blocked/`, `done/` all exist with READMEs |
| P3 | Handoff template covers required sections | Task ID, summary, files changed, evidence, known issues, risks, next steps |
| P4 | Reassignment template exists and references switching protocol | Both files present and cross-linked |
| P5 | Capability registry has ≥20 capabilities | Currently 21. Each has `preferred_workers`, `common_roles`, `evidence_expected` |
| P6 | Each worker file has Solo / Multi / Hybrid sections | All 6 worker files |
| P7 | Risk register has ≥10 entries | Currently 10. Each has likelihood, impact, mitigation, status |
| P8 | Verification gates document multi-layer verification | Self-check + automated + independent + human |

### 2.4 Documentation Cohesion

| Gate | Check | Pass criterion |
|------|-------|----------------|
| D1 | Worker startup sequence has one canonical home | Adapter and worker files link rather than restate (or, transitionally, all match `AGENTS.md` Section 6 exactly) |
| D2 | Validation command list has one canonical home | `docs/03-development/commands.md` (or equivalent) is canonical |
| D3 | Fork workflow has one canonical home | `TEMPLATE_USAGE.md` is canonical |
| D4 | Glossary exists | `agent-os/glossary.md` defines ≥20 system-specific terms |
| D5 | README hero shows lifecycle + 4-layer assignment in one screen | Single diagram or two short ASCII blocks |
| D6 | Each `agent-os/*/README.md` exists and explains the directory | All directories with README files |

### 2.5 Safety Posture

| Gate | Check | Pass criterion |
|------|-------|----------------|
| Sa1 | `SECURITY.md` covers secrets, destructive commands, deployment | Existing file covers all three |
| Sa2 | `agent-os/prompt-injection-policy.md` exists | New policy covers external content as data, quoting, refusing instructions in fetched data |
| Sa3 | Tool boundaries documented per worker (or canonical + deltas) | Either each worker has a tool policy or one canonical policy with worker-specific deltas |
| Sa4 | `AGENTS.md` Section 14 (Safety Rules) lists ≥6 rules | Currently 6 |
| Sa5 | Secret-scan step in CI | `validate-agent-os.yml` runs `gitleaks` or `trufflehog` |
| Sa6 | No real secrets committed | Manual scan + secret-scan tool clean |

### 2.6 GitHub Readiness

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | `LICENSE` exists at root | Present, with intentional `[OWNER_USERNAME]` |
| G2 | `CONTRIBUTING.md` exists | Present, references task IDs and DoD |
| G3 | `SECURITY.md` exists | Present |
| G4 | `CODE_OF_CONDUCT.md` exists | Present (Contributor Covenant 2.1 recommended) |
| G5 | `.github/PULL_REQUEST_TEMPLATE.md` exists | Present, references task ID, evidence, handoff, reassignment |
| G6 | `.github/ISSUE_TEMPLATE/` has ≥4 templates | Currently 6 |
| G7 | `.github/CODEOWNERS` exists | Present |
| G8 | Workflows are syntactically valid | `actionlint` passes (or visual check) |
| G9 | Workflows do not depend on missing secrets | Workflows tolerate missing secrets gracefully |
| G10 | `.github/dependabot.yml` exists | Watches `actions/*` for updates |

---

## 3. Recommended Gates (Should Pass)

These gates strengthen the release but are not strict blockers. Each FAIL should be acknowledged in the release notes.

### 3.1 Modern Agent Compatibility

| Gate | Check | Pass criterion |
|------|-------|----------------|
| Mo1 | MCP integration starter | `agent-os/mcp.md` + `.mcp.example.json` exist; capability registry includes MCP capabilities |
| Mo2 | Git worktree workflow | `agent-os/worktree-strategy.md` exists; `scripts/setup-worktree.mjs` works on Windows and POSIX |
| Mo3 | Provider tier routing starter | `agent-os/state/provider-tiers.json` and `agent-os/provider-routing.md` exist; task template has `Required tier` field |
| Mo4 | Cursor adapter | `.cursor/rules/`, `CURSOR.md`, `agent-os/workers/cursor-worker.md` exist (only mandatory if Cursor users are a target) |
| Mo5 | Init / scaffolding script | `npm run init` works on a fresh clone |
| Mo6 | Browser-agent safety beyond Antigravity | Generalized policy or per-worker browser policy covered |

### 3.2 Examples in Active State

| Gate | Check | Pass criterion |
|------|-------|----------------|
| Ex1 | Active handoff demo present | `agent-os/handoffs/active/EXAMPLE-*.md` clearly marked illustrative |
| Ex2 | Active lock demo present | `agent-os/locks/EXAMPLE-*.json` clearly marked illustrative |
| Ex3 | Verification artifacts present | `agent-os/reports/verification/EXAMPLE-*` files exist OR sample report marks paths as illustrative |
| Ex4 | Multi-worker example walkthrough | `examples/sample-multi-worker-walkthrough.md` exists |
| Ex5 | Failure / recovery example | `examples/sample-blocked-task-recovery.md` exists |
| Ex6 | All 6 existing examples link consistently | Examples reference each other's TaskFlow Lite story without contradiction |

### 3.3 Quality Tooling

| Gate | Check | Pass criterion |
|------|-------|----------------|
| Qa1 | JSON schema validation for state files | Schemas in `agent-os/schemas/` cover all state JSON; `validate-json.mjs` enforces them |
| Qa2 | Markdown lint runs in CI | `validate-agent-os.yml` includes a markdown-lint step |
| Qa3 | State consistency validator | `validate-state-consistency.mjs` checks paired files |
| Qa4 | Startup sequence consistency validator | `validate-startup-consistency.mjs` flags drift |
| Qa5 | Scope-creep checker | `scripts/check-scope.mjs` exists and runs against an open task |
| Qa6 | DoD on diff (not folder) | `check-definition-of-done.mjs` accepts a task ID argument |

### 3.4 Operational Polish

| Gate | Check | Pass criterion |
|------|-------|----------------|
| Op1 | `STATUS.md` auto-generated and current | Daily-status-report workflow updates `STATUS.md` |
| Op2 | README badges present | CI status, license, version, "AGENTS.md compatible" |
| Op3 | Repository description and topics documented for the human owner | Step in `RELEASE_CHECKLIST.md` describing GitHub-side metadata |
| Op4 | First-run walkthrough | A `docs/03-development/first-run.md` describes the 60-second flow |
| Op5 | "Why ROWS over X?" comparison page | Brief comparison vs plain `AGENTS.md`, BMAD, Spec Kit, Augment Intent |
| Op6 | `.editorconfig` and `.gitattributes` exist | Cross-OS contributors get clean diffs |

### 3.5 Documentation Polish

| Gate | Check | Pass criterion |
|------|-------|----------------|
| Dp1 | Glossary covers ≥20 terms | `agent-os/glossary.md` |
| Dp2 | Mermaid or ASCII map of `agent-os/` | One diagram showing folder relationships |
| Dp3 | Every worker file references the same canonical startup sequence | One source of truth |
| Dp4 | Validation command list exists in exactly one canonical doc | Others link to it |
| Dp5 | Fork workflow exists in exactly one canonical doc | Others link to it |
| Dp6 | Every doc has a "Related Files" section linking back to the index | Cross-references navigable |

---

## 4. Verification Workflow

To run this checklist:

1. **Snapshot:** Note commit SHA, date, runner.
2. **Automated checks:** Run `npm run audit`. Record pass/fail.
3. **Tool extension:** Run any new validators (`validate-state-consistency`, `validate-startup-consistency`, `validate-mcp` if added).
4. **Manual passes:** Walk through each Mandatory and Recommended gate. Mark PASS / FAIL / N/A.
5. **Blocker tally:** Count Mandatory FAILs.
6. **Risk tally:** Count Recommended FAILs.
7. **Verdict:**
   - 0 Mandatory FAIL + ≤3 Recommended FAIL → **READY**.
   - 0 Mandatory FAIL + 4–8 Recommended FAIL → **READY with notes** (document gaps in CHANGELOG).
   - ≥1 Mandatory FAIL → **NOT READY**. Address blockers; re-run.

This checklist is itself a process artifact and should be referenced from any "publish" PR.

---

## 5. First-Run Smoke Test (Manual)

Independent verification means **trying the repo as a new user**. Do this on a fresh clone (different machine or fresh worktree):

| Step | Expected | Actual | PASS? |
|------|----------|--------|-------|
| 1. Clone the repo | Succeeds | | |
| 2. Read `README.md` for ≤2 minutes | Understand the pitch | | |
| 3. Run `npm run audit` | All checks PASS | | |
| 4. Open `AGENTS.md` | Constitution is clear in ≤5 minutes | | |
| 5. Open `PROJECT_GOAL.md` | Intake form is fillable in ≤10 minutes | | |
| 6. Run `npm run init` (when M7 done) | Placeholders replaced; first task created | | |
| 7. Open the generated first task | Task is claimable, well-formed | | |
| 8. Read `examples/sample-handoff.md` | Understand what a great handoff looks like | | |
| 9. Run `npm run list:tasks` | Shows tasks by state | | |
| 10. Run `node scripts/agentctl.mjs` | System info + commands listed | | |
| 11. Open `prompt-library/solo-worker-start.md` | Ready to paste into your AI tool | | |
| 12. Find the no-self-close rule | Found in `AGENTS.md` Section 12 (or equivalent) | | |

If 10 of 12 PASS on a fresh clone, the first-run experience is acceptable.

---

## 6. Independent Reviewer Sign-Off

Per ROWS, no worker may close its own work. The release decision must be **independently verified** by a different worker or a human:

```
Independent reviewer:    [name / worker]
Date of review:          YYYY-MM-DD
Mandatory gates:         _ / _ PASS
Recommended gates:       _ / _ PASS
First-run smoke test:    _ / 12 PASS

Decision:                READY / READY-WITH-NOTES / NOT-READY
Signature / approval:    _____________________
Notes:                   _____________________________________________
```

Save the completed sign-off in `agent-os/reports/verification/release-readiness-YYYY-MM-DD.md`.

---

## 7. Failure Modes & Recovery

If verification fails:

| Failure | Recovery |
|---------|----------|
| Single Mandatory FAIL | Promote the matching backlog item (Wave 1 most likely); re-run that gate after fix |
| Multiple structural FAILs | Halt release; re-audit using `agent-template-readiness-audit.md`; promote a batch of backlog items |
| All Mandatory PASS, many Recommended FAIL | Release as **0.x** with documented gaps; target 1.0 after Recommended gates pass |
| `npm run audit` regression | Bisect with git; do not release until cause identified |
| First-run smoke test < 8/12 | Address Wave 1 + 3 backlog items; UX is the lead bar for adoption |

---

## 8. Versioning Guidance

This is a process recommendation only:

- **0.x.y** — While Mandatory gates pass but Modernize-theme features (MCP, worktrees, init script) are missing.
- **1.0.0** — When Mandatory + most Recommended gates pass.
- **1.x.y** — Iterate on examples, polish, and adapter coverage.
- **2.0.0** — Reserved for breaking changes to the assignment model or AGENTS.md structure.

`CHANGELOG.md` already follows Keep a Changelog. Continue that.

---

## 9. Continuous Verification

Once published, re-run this checklist:

- Before each minor release.
- After any change to `AGENTS.md`, `agent-os/state/*`, or `package.json`.
- Quarterly even without changes (ecosystem drifts; check that AGENTS.md spec, MCP spec, and prompt-injection guidance are still aligned).

Schedule the quarterly review in `@/Users/theca/CascadeProjects/windsurf-project-7/agent-os/schedules/audits.md`.

---

## 10. Related Files

- `@/Users/theca/CascadeProjects/windsurf-project-7/RELEASE_CHECKLIST.md` — Existing structural release checklist
- `@/Users/theca/CascadeProjects/windsurf-project-7/TEMPLATE_READINESS.md` — Existing readiness gates
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/agent-template-readiness-audit.md` — Audit findings
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/current-ai-agent-workflow-research.md` — Research basis
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/backlog/template-improvement-backlog.md` — Improvement backlog
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/strategy/repo-positioning-review.md` — Positioning analysis
- `@/Users/theca/CascadeProjects/windsurf-project-7/agent-os/verification-gates.md` — Repo's verification gates
- `@/Users/theca/CascadeProjects/windsurf-project-7/agent-os/definition-of-done.md` — Repo's definition of done
