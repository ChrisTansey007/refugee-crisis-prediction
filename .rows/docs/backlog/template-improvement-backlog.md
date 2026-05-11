# Template Improvement Backlog

> **Source:** Audit findings in `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/agent-template-readiness-audit.md` and research in `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/current-ai-agent-workflow-research.md`.
>
> **Format:** Each item has an ID, title, description, rationale, effort (S/M/L), impact (Low/Med/High), and acceptance criteria. Items are grouped by theme and ordered within each theme by ROI.
>
> **Status:** Backlog only. Items here are **not** yet active task files in `agent-os/tasks/backlog/`. Promote items by creating task files using `agent-os/tasks/task-template.md` and placing them in `agent-os/tasks/backlog/` for human approval.

---

## Reading Guide

- **Effort** — S = ≤1 hour, M = 1–4 hours, L = 4+ hours.
- **Impact** — High / Medium / Low based on adoption and credibility gain.
- **Themes:**
  - **C** = Critical fix (broken/missing references) — do first.
  - **M** = Modernize (MCP, worktrees, providers, prompt-injection).
  - **D** = Deduplicate documentation.
  - **T** = Template-quality polish.
  - **V** = Verification & quality gates.
  - **X** = Examples in active state.
  - **O** = Observability & coordination.

---

## Critical Fixes (Theme C)

### C1 — Add `.env.example`

- **Effort:** S
- **Impact:** Medium
- **Why:** `@/Users/theca/CascadeProjects/windsurf-project-7/.gitignore:17` and `@/Users/theca/CascadeProjects/windsurf-project-7/docs/03-development/setup.md:23` reference `.env.example`, which does not exist.
- **What:** Create `.env.example` at repo root with commented placeholders only (no secrets, no project assumptions). Mark intentional placeholders.
- **Acceptance:** File exists, contains only comments + placeholder lines using intentional markers, `validate-placeholders.mjs` passes.

### C2 — Resolve `.claude/rules/` reference

- **Effort:** S
- **Impact:** Medium
- **Why:** `@/Users/theca/CascadeProjects/windsurf-project-7/.claude/README.md:13-19` lists `backend.md`, `frontend.md`, `docs.md`, `testing.md`, `orchestration.md` as if they exist. The directory is empty.
- **What:** Either (a) create the five files as template stubs with explicit placeholder markers, or (b) edit `.claude/README.md` to remove the file list and explain the directory is empty by design and meant to be populated after fork.
- **Acceptance:** No broken file references in `.claude/README.md`. `validate-template-readiness.mjs` continues to pass.

### C3 — Define or remove `npm test` and `npm run lint` references

- **Effort:** S
- **Impact:** High
- **Why:** `@/Users/theca/CascadeProjects/windsurf-project-7/agent-os/definition-of-done.md`, `@/Users/theca/CascadeProjects/windsurf-project-7/agent-os/verification-gates.md`, and the implement-task workflow all reference `npm test` and `npm run lint`. `package.json` defines neither.
- **What:** Add no-op or template-aware scripts to `package.json`:
  - `"test": "node scripts/validate-template-readiness.mjs && echo 'Add real tests after forking.'"`
  - `"lint": "node scripts/validate-placeholders.mjs && echo 'Add real linter after forking.'"`
- **Acceptance:** `npm test` and `npm run lint` exit 0 on a fresh clone. Document in `docs/03-development/commands.md` that they are template-stage no-ops.

### C4 — Add `engines` field to `package.json`

- **Effort:** S
- **Impact:** Low
- **Why:** ESM scripts assume modern Node. No declared minimum.
- **What:** Add `"engines": { "node": ">=20" }` and document in `docs/03-development/setup.md`.
- **Acceptance:** `package.json` updated, README/setup mention Node ≥ 20 once.

### C5 — Fix `examples/sample-verification-report.md` evidence references

- **Effort:** S
- **Impact:** Low
- **Why:** The sample references `reports/verification/TASK-0003-test-output.txt`, `*.png`, `*.mp4` files that do not exist.
- **What:** Either (a) create stub artifacts in `agent-os/reports/verification/` (using clearly-marked example file names) or (b) reword the sample to make clear they are illustrative paths only.
- **Acceptance:** `validate-links.mjs` passes; reader can tell whether referenced files exist or are illustrative.

### C6 — Add `.editorconfig` and `.gitattributes`

- **Effort:** S
- **Impact:** Low
- **Why:** Cross-OS contributors will see whitespace and line-ending diffs without these.
- **What:**
  - `.editorconfig` — UTF-8, LF, 2-space indent for MD/JSON/YAML, final newline.
  - `.gitattributes` — `* text=auto`, `*.md text eol=lf`, etc.
- **Acceptance:** Files exist; `git status` clean on both Windows and macOS after a fresh clone.

---

## Modernize (Theme M)

### M1 — MCP integration starter

- **Effort:** M
- **Impact:** High
- **Why:** Zero MCP references in the repo. MCP is the dominant 2026 standard for tool-extended AI. See research §4.
- **What:**
  1. Create `agent-os/mcp.md` — policy: which capabilities are allowed, security boundaries (read-only by default, scoped roots, version pinning).
  2. Create `.mcp.json` (or `.mcp.example.json`) at repo root with safe-default servers (filesystem read-only on `./`, git read-only).
  3. Add capabilities to `agent-os/state/capability-registry.json`: `mcp-tool-use`, `mcp-resource-read`.
  4. Update `agent-os/tasks/task-template.md` with optional `## Required MCP servers` section.
  5. Add `scripts/validate-mcp.mjs` — checks `.mcp.json` validity if present.
- **Acceptance:** `.mcp.example.json` exists; `agent-os/mcp.md` exists; capability-registry includes new caps; task template has new section.

### M2 — Git worktree workflow

- **Effort:** M
- **Impact:** High
- **Why:** Multi-worker mode without worktrees collides on shared working tree. See research §2.
- **What:**
  1. Create `agent-os/worktree-strategy.md`: when to use worktrees (multi-worker / hybrid mode), naming convention (`<repo>-<worker>`), shared `.git/` model.
  2. Add `scripts/setup-worktree.mjs <worker> <task-id>` that runs `git worktree add` with the right branch name.
  3. Update `agent-os/branch-strategy.md` to recommend worktree per worker for parallel work.
  4. Update `agent-os/execution-modes.md` (multi-worker and hybrid sections) to reference worktrees.
  5. Add a CI check that PR diffs do not include nested worktree directories.
- **Acceptance:** Doc exists; script runs end-to-end on a clean repo; tested for both Windows (PowerShell) and macOS/Linux.

### M3 — Prompt-injection / external-content policy

- **Effort:** M
- **Impact:** High
- **Why:** OWASP LLM Top 10 #1 threat. ROWS does not address it. See research §5.
- **What:**
  1. Create `agent-os/prompt-injection-policy.md`: external-content-as-data rule, quoting requirements, refuse-instructions-from-fetched-data rule, high-risk content sources.
  2. Add a "External content handling" section to `agent-os/worker-contract.md`.
  3. Add a Safety Rule to `AGENTS.md` Section 14 (or a new Section 14.5).
  4. Update `SECURITY.md` to link to the new policy.
  5. Add `scripts/validate-prompt-safety.mjs` that warns when task specs contain "follow the README of repo X" or "read https://..." without a quoting/quarantine note.
- **Acceptance:** Policy exists; worker contract updated; AGENTS.md updated; sample task in `examples/` demonstrates safe vs unsafe phrasing.

### M4 — Provider tier routing

- **Effort:** M
- **Impact:** Medium
- **Why:** Multi-provider routing (frontier / mid / fast / local) is now standard. See research §6.
- **What:**
  1. Create `agent-os/state/provider-tiers.json` — defines tiers and typical capability fit.
  2. Add `Required tier` and `Cost ceiling` fields to `agent-os/tasks/task-template.md` (both default "any" / "unspecified").
  3. Create `agent-os/provider-routing.md` describing fallback chain, local-first for secrets, cost ceilings.
  4. Add tier preferences to each `agent-os/workers/*-worker.md`.
- **Acceptance:** JSON schema valid; task template updated; `validate-tasks.mjs` accepts both old and new tasks (backward compatible).

### M5 — Cursor adapter

- **Effort:** S
- **Impact:** Medium
- **Why:** Cursor is one of the top 3 AI IDEs. ROWS has adapters for Windsurf, Claude, Codex, Gemini, Antigravity, Hermes — but not Cursor.
- **What:**
  1. Create `.cursor/rules/` with starter rules pointing at `AGENTS.md`.
  2. Create root-level `CURSOR.md` adapter.
  3. Create `agent-os/workers/cursor-worker.md` (similar to `windsurf-worker.md`).
  4. Update `worker-status.json` and `assignment-state.json` with Cursor entry.
  5. Update `role-capability-matrix.md` to list Cursor where appropriate.
- **Acceptance:** Cursor user can fork the repo, open in Cursor, and have agent rules auto-discovered.

### M6 — Generalized tool-use boundary policy

- **Effort:** S
- **Impact:** Medium
- **Why:** Only Antigravity has a written terminal/tool policy (`.antigravity/safe-terminal-policy.md`). Other workers operate without one.
- **What:**
  1. Promote `.antigravity/safe-terminal-policy.md` content to `agent-os/tool-boundaries.md` as the canonical policy.
  2. Have each `.{worker}/README.md` reference the canonical policy and add only worker-specific deltas.
- **Acceptance:** One canonical policy; per-worker deltas only; no duplication.

### M7 — Init / scaffolding script

- **Effort:** M
- **Impact:** High
- **Why:** Reducing first-run friction is the single biggest UX gain. Most modern templates ship with one.
- **What:**
  1. Create `scripts/init.mjs` — interactive (or arg-driven) script that:
     - Prompts for project name, owner GitHub username, execution mode, primary worker.
     - Replaces `[PROJECT_NAME]` and `[OWNER_USERNAME]` in known files.
     - Updates `system-state.json`, `assignment-state.json`, `package.json`, `LICENSE`, `.github/CODEOWNERS`.
     - Creates a starter task in `tasks/backlog/`.
  2. Add `npm run init` script to `package.json`.
  3. Document in README and `TEMPLATE_USAGE.md`.
- **Acceptance:** Fresh fork → `npm run init` → all key placeholders replaced; `validate-placeholders.mjs` shows zero `[PROJECT_NAME]` / `[OWNER_USERNAME]` remaining (except in `examples/` and intentional template stubs).

---

## Deduplicate Documentation (Theme D)

### D1 — Canonical worker startup sequence

- **Effort:** M
- **Impact:** High
- **Why:** Startup sequence is duplicated across 7+ files with drift already present. See audit §4.2.
- **What:**
  1. Create `agent-os/startup-sequence.md` — single canonical list (with rationale per step).
  2. Optionally also `agent-os/state/startup-sequence.json` for machine-readable form.
  3. Replace duplicated lists in adapters and worker files with a one-line link to the canonical doc.
  4. Keep `AGENTS.md` Section 6 as a *summary* with "see `agent-os/startup-sequence.md` for details."
  5. Add `scripts/validate-startup-consistency.mjs` to detect drift.
- **Acceptance:** One canonical doc; adapter/worker files link rather than restate; validator passes.

### D2 — Canonical validation command list

- **Effort:** S
- **Impact:** Medium
- **Why:** README, HUMAN_OWNER_GUIDE, agentctl.mjs, RELEASE_CHECKLIST list slightly different command sets.
- **What:**
  1. Make `docs/03-development/commands.md` canonical.
  2. Replace duplicated lists in README, HUMAN_OWNER_GUIDE, RELEASE_CHECKLIST with a link.
  3. Have `agentctl.mjs` read `package.json` scripts dynamically and print whatever exists.
- **Acceptance:** Adding a new `npm run …` script means only updating `package.json` and `commands.md`.

### D3 — Canonical fork workflow

- **Effort:** S
- **Impact:** Medium
- **Why:** Fork workflow is in README, TEMPLATE_USAGE, HUMAN_OWNER_GUIDE.
- **What:** Make `TEMPLATE_USAGE.md` canonical. Reduce README "Quick Start" to a 30-second pitch with a "Full guide → TEMPLATE_USAGE.md" link. Reduce HUMAN_OWNER_GUIDE to owner-cadence content only.
- **Acceptance:** One canonical fork doc; the others link rather than restate.

### D4 — Glossary

- **Effort:** S
- **Impact:** Medium
- **Why:** "Worker," "role," "capability," "execution mode," "lock," "handoff," "DoD," "ROWS," "intentional placeholder" are scattered.
- **What:** Create `agent-os/glossary.md` with concise one-paragraph definitions, each linking to the canonical doc.
- **Acceptance:** Glossary covers ≥20 terms; new contributor can read it in 5 minutes.

---

## Template-quality Polish (Theme T)

### T1 — Add `CODE_OF_CONDUCT.md`

- **Effort:** S
- **Impact:** Low
- **Why:** Standard for public templates.
- **What:** Use Contributor Covenant 2.1.
- **Acceptance:** File exists; linked from `CONTRIBUTING.md`.

### T2 — README badges

- **Effort:** S
- **Impact:** Low
- **Why:** Signals project health.
- **What:** Add badges for CI status (validate-agent-os), license, version, "template-ready."
- **Acceptance:** Badges render correctly on GitHub.

### T3 — `.github/dependabot.yml`

- **Effort:** S
- **Impact:** Low
- **Why:** Even dep-free repos benefit from dependabot for `actions/*` updates.
- **What:** Add a minimal `dependabot.yml` that watches `.github/workflows/`.
- **Acceptance:** File present; valid syntax.

### T4 — Document Repository description and topics

- **Effort:** S
- **Impact:** Low
- **Why:** Helps discoverability when published as a template.
- **What:** In `RELEASE_CHECKLIST.md`, add a step: set GitHub description and topics (`ai-agents`, `template`, `mcp`, `multi-agent`, `agents-md`).
- **Acceptance:** Checklist step exists.

### T5 — Validate paired files (state-consistency)

- **Effort:** M
- **Impact:** Medium
- **Why:** `decision-register.json` mirrors `decision-register.md`; capability-registry mirrors role-capability-matrix. Drift is silent today.
- **What:** Add `scripts/validate-state-consistency.mjs` that cross-checks paired files.
- **Acceptance:** Runs in `npm run audit`; flags drift.

### T6 — Generate decision register from JSON

- **Effort:** M
- **Impact:** Low
- **Why:** Authoring two formats is duplication.
- **What:** Make `decision-register.json` the source; render `docs/05-decisions/decision-register.md` via `scripts/generate-decision-register.mjs`.
- **Acceptance:** Editing JSON regenerates MD; validator passes.

---

## Verification & Quality Gates (Theme V)

### V1 — Secret scan in CI

- **Effort:** S
- **Impact:** High
- **Why:** `SECURITY.md` says "never commit secrets" but no automated check.
- **What:** Add a `gitleaks` or `trufflehog` step to `validate-agent-os.yml`.
- **Acceptance:** CI fails if a known-secret pattern is committed.

### V2 — Markdown lint

- **Effort:** S
- **Impact:** Low
- **Why:** Documentation quality.
- **What:** Add `markdownlint-cli2` (single dep — accept the trade-off) or a Node-only lite linter.
- **Acceptance:** `npm run lint:md` runs; CI step exists.

### V3 — Scope-creep check

- **Effort:** M
- **Impact:** Medium
- **Why:** Workers are told to stay in scope but no automated guard.
- **What:** `scripts/check-scope.mjs` — for a given task ID, compares `git diff` files against the task's `Files Likely Affected` list. Warns on out-of-scope files.
- **Acceptance:** Runs locally; can be wired into pre-commit or PR check.

### V4 — Schema validation for state JSON

- **Effort:** M
- **Impact:** Medium
- **Why:** `validate-json.mjs` parses but does not enforce schema.
- **What:** Add JSON Schemas in `agent-os/schemas/` for `system-state.json`, `assignment-state.json`, `capability-registry.json`, `worker-status.json`, `risk-register.json`, `decision-register.json`, `dependency-map.json`, lock files. Validate against schemas in `validate-json.mjs`.
- **Acceptance:** Schemas exist; validator catches missing fields and wrong types.

### V5 — DoD on diff, not folder

- **Effort:** L
- **Impact:** Medium
- **Why:** `check-definition-of-done.mjs` only fires for tasks already in `review/`. A workflow that checks based on commit/PR labels would fire earlier.
- **What:** Extend `check-definition-of-done.mjs` to optionally accept a task ID and check that task wherever it lives.
- **Acceptance:** Can run `npm run check:dod -- TASK-0003` without moving the task.

---

## Examples in Active State (Theme X)

### X1 — Active handoff demo

- **Effort:** S
- **Impact:** Medium
- **Why:** `agent-os/handoffs/active/` only has README. Readers cannot see what an active handoff looks like in place.
- **What:** Add `agent-os/handoffs/active/EXAMPLE-handoff.md` clearly marked as illustrative; or copy `examples/sample-handoff.md` into active with a note "this is a demo file; remove after fork."
- **Acceptance:** New users can see a handoff in its real folder.

### X2 — Active lock demo

- **Effort:** S
- **Impact:** Low
- **Why:** Same as X1 for locks.
- **What:** Add `agent-os/locks/EXAMPLE-lock.json` clearly marked.
- **Acceptance:** Lock file shape visible in place.

### X3 — Verification artifact stubs

- **Effort:** S
- **Impact:** Low
- **Why:** Sample verification report references files that don't exist (see C5).
- **What:** Add `agent-os/reports/verification/EXAMPLE-test-output.txt`, `EXAMPLE-screenshot.png` (a 1-pixel PNG), `EXAMPLE-recording-note.md` (instead of a real .mp4).
- **Acceptance:** Sample report links resolve.

### X4 — Multi-worker example walkthrough

- **Effort:** M
- **Impact:** Medium
- **Why:** All current examples assume solo mode.
- **What:** Add `examples/sample-multi-worker-walkthrough.md` showing a coordinator decomposing, two builders implementing, a verifier verifying, with cross-references to handoffs and locks.
- **Acceptance:** Example exists; references all relevant artifact types.

### X5 — Failure / recovery example

- **Effort:** S
- **Impact:** Low
- **Why:** Only happy paths are documented.
- **What:** Add `examples/sample-blocked-task-recovery.md` showing a worker hitting a block, escalating, and a different worker resuming.
- **Acceptance:** Example exists; demonstrates `blocked/` folder and reassignment flow.

---

## Observability & Coordination (Theme O)

### O1 — Coordination proposals folder

- **Effort:** S
- **Impact:** Low
- **Why:** Hermes "proposes coordination" but has no structured place to put proposals.
- **What:** Create `agent-os/proposals/` with a template (`proposal-template.md`) and README. Include a sample.
- **Acceptance:** Hermes can write a coordination proposal that lives in version control.

### O2 — Sprint / milestone artifact

- **Effort:** M
- **Impact:** Medium
- **Why:** Tasks float independently. Real projects need grouping.
- **What:** Add `agent-os/milestones/` with a milestone-template.md and a JSON state file mapping milestone → task IDs.
- **Acceptance:** A milestone can be created; its progress visible in `npm run status:generate`.

### O3 — Agent observability hook

- **Effort:** S
- **Impact:** Low
- **Why:** Document where observability tooling plugs in.
- **What:** Create `agent-os/observability.md` explaining ROWS does not mandate observability tools, but tasks and handoffs use task IDs as correlation IDs that can be referenced from external logs (LangSmith, Helicone, etc.).
- **Acceptance:** Doc exists.

### O4 — In-session checkpoint pattern

- **Effort:** M
- **Impact:** Medium
- **Why:** Long tasks benefit from intermediate checkpoints.
- **What:** Document a `agent-os/handoffs/active/checkpoints/` convention; add `handoff-checkpoint-template.md`.
- **Acceptance:** Long-running tasks can checkpoint without writing a full handoff.

### O5 — Status report dashboard

- **Effort:** M
- **Impact:** Medium
- **Why:** `npm run status:generate` produces a Markdown report. A simpler one-screen "current state" card would help humans.
- **What:** Add `STATUS.md` at repo root (auto-generated nightly) with: phase, mode, tasks counts per state, active workers, recent handoffs, blocked tasks. Generated by an existing or new script.
- **Acceptance:** `STATUS.md` exists; daily-status-report workflow updates it.

---

## Priority Matrix (Recommended Order of Execution)

The order below balances impact, effort, and dependency. It assumes the user wants to bring the template to "great" status efficiently.

### Wave 1 — Critical fixes & quick wins (≈ 1 day)

1. **C3** Define `npm test` and `npm run lint` (unblocks DoD enforcement).
2. **C1** Add `.env.example` (removes broken reference).
3. **C2** Resolve `.claude/rules/` reference.
4. **C4** Add `engines` field.
5. **C5** Fix verification example references (or create stubs — also covers X3).
6. **C6** Add `.editorconfig` and `.gitattributes`.

### Wave 2 — Modernize the agent surface (≈ 2–3 days)

7. **M1** MCP integration starter.
8. **M3** Prompt-injection / external-content policy.
9. **M2** Git worktree workflow.
10. **M7** Init / scaffolding script (depends on no others; massive UX win).

### Wave 3 — Reduce documentation drift (≈ 1 day)

11. **D1** Canonical startup sequence.
12. **D2** Canonical validation command list.
13. **D3** Canonical fork workflow.
14. **D4** Glossary.

### Wave 4 — Tighten verification & template quality (≈ 1–2 days)

15. **V1** Secret scan in CI.
16. **V4** Schema validation for state JSON.
17. **T5** Validate paired files.
18. **M6** Generalized tool-use boundary policy.
19. **M5** Cursor adapter (if Cursor users matter to the project).

### Wave 5 — Polish & demonstrate (≈ 1 day)

20. **X4** Multi-worker example walkthrough.
21. **X1** Active handoff demo.
22. **X2** Active lock demo.
23. **X5** Failure / recovery example.
24. **O5** STATUS.md dashboard.
25. **T1** CODE_OF_CONDUCT.md, **T2** badges, **T3** dependabot.

### Wave 6 — Optional / lower priority

- **M4** Provider tier routing.
- **V2** Markdown lint, **V3** Scope-creep check, **V5** DoD on diff.
- **T6** Generate decision register from JSON.
- **O1**–**O4** Coordination proposals, milestones, observability hook, checkpoints.

---

## How to Promote These to Real Tasks

For each backlog item the human owner approves:

1. Open `agent-os/tasks/task-template.md`.
2. Copy to `agent-os/tasks/backlog/TASK-XXXX-<short>.md`.
3. Fill in: Responsible Role, Required Capabilities, Preferred Workers, Execution Mode Compatibility, Objective, Acceptance Criteria (use the criteria from this doc), Files Likely Affected, Verification Required, Completion Evidence Required, Handoff Required, Risks, Dependencies.
4. Set status to `backlog`.
5. Owner reviews and moves to `ready/` when approved.
6. A worker claims following `.windsurf/workflows/claim-task.md`.

This keeps the backlog separate from the active task queue per ROWS rules.

---

## Related Files

- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/agent-template-readiness-audit.md` — Audit findings
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/current-ai-agent-workflow-research.md` — Research basis
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/strategy/repo-positioning-review.md` — Positioning analysis
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/verification/release-readiness-checklist.md` — Release readiness gates
- `@/Users/theca/CascadeProjects/windsurf-project-7/agent-os/tasks/task-template.md` — Task template to use when promoting
