# Repo Positioning Review — ROWS

> **Purpose:** Decide what kind of asset this repository should be, who it should serve, and how it should be positioned in the public template ecosystem.
>
> **Inputs:** Audit findings (`@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/agent-template-readiness-audit.md`) and ecosystem research (`@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/current-ai-agent-workflow-research.md`).
>
> **Audience:** The human owner. This document is decision-support, not a directive.

---

## 1. What the Repo Currently Is

Read literally, ROWS is currently a **GitHub template** that bundles:

- A worker constitution (`AGENTS.md`).
- A four-layer assignment model (capability → role → preferred worker → active worker).
- A folder-based task lifecycle.
- A handoff system.
- Verification gates (no-self-close).
- A risk register and decision register.
- 6 worker adapters and 7 issue/PR templates.
- 10 validation scripts wired into CI.
- 6 worked examples.
- 10 copy-paste prompts.

It is **not** an application, **not** a CLI, **not** a service. It is a **process operating system encoded as files**.

---

## 2. Strongest Identity Options

The audit suggests four plausible identities for ROWS. They are not mutually exclusive, but choosing one as the **primary** identity changes which improvements matter most.

### Option A — "The Constitution Repo" (governance-first)

**Pitch:** "The most rigorous open contract for multi-agent software development. Fork it, fill in your goal, and run any AI tool against it with consistent rules."

**Strengths to lean into:**

- The no-self-close rule.
- The capability → role → preferred worker → active worker model.
- The verification gates.
- The lifecycle folders.
- Worker replaceability.

**Audience:**

- Solo developers who want discipline.
- Agencies and consultancies that need defensible AI-assisted work.
- Teams introducing AI workers and needing guardrails.
- Auditors and compliance-conscious projects.

**Implication:** The brand is *governance*. Improvements that strengthen governance (V1 secret scan, V4 schema validation, T5 paired-file consistency, D-theme deduplication) become highest priority. MCP and worktrees are nice-to-have.

### Option B — "The Modern Agent Workbench" (capability-first)

**Pitch:** "A turn-key environment for running multiple AI agents in parallel — MCP-aware, worktree-isolated, provider-agnostic, prompt-injection-aware."

**Strengths to lean into:**

- Worker replaceability.
- Multi-worker mode.
- Tool adapters for many AI tools.
- Prompt-library starter prompts.

**Audience:**

- Power users running 3+ agents in parallel.
- Indie hackers building shipped projects with AI assistance.
- Teams that want a starting point for serious agent automation.

**Implication:** The brand is *capability*. The Modernize theme (M1 MCP, M2 worktrees, M3 prompt-injection, M4 providers, M5 Cursor, M7 init script) becomes highest priority. Governance is necessary but not the lead.

### Option C — "The Agent-Onboarding Template" (UX-first)

**Pitch:** "Fork. Run `npm run init`. Get a defensible, multi-agent-ready repo in 60 seconds."

**Strengths to lean into:**

- Single command to bootstrap.
- Clear `PROJECT_GOAL.md` intake.
- One worked example.

**Audience:**

- New developers learning to use AI agents.
- Teams piloting AI workflows.
- Educators teaching agent-assisted development.

**Implication:** The brand is *low friction*. M7 init script, D-theme deduplication, X-theme example walkthroughs become highest priority. Heavy governance and parallel-agent depth become potential clutter.

### Option D — "The Reference Implementation of the AGENTS.md Spec"

**Pitch:** "What `AGENTS.md` looks like when you take it seriously — including every adapter, every checklist, every state file, and every gate."

**Strengths to lean into:**

- Adapter coverage (Windsurf, Claude, Codex, Gemini, Antigravity, Hermes; Cursor pending).
- Constitution-grade `AGENTS.md`.
- File-based state.
- Examples.

**Audience:**

- Teams evaluating `AGENTS.md` as a standard.
- Authors of competing templates looking for benchmarks.
- Tool vendors testing their AGENTS.md support.

**Implication:** The brand is *reference quality*. T-theme polish, D-theme deduplication, X-theme examples, M5 Cursor adapter (more vendors), and meticulous validation become highest priority.

---

## 3. Recommendation

**Lead with Option B (Modern Agent Workbench), keep Option A (Governance) as the substrate, borrow from C (UX) for onboarding, and let D (Reference Implementation) emerge naturally.**

### Why B as the lead

- The brief says "real-world work with current AI agents" and "current AI ecosystem." This implies usefulness in 2026 practice, which means MCP, worktrees, prompt-injection, providers — Option B's territory.
- Option A's governance is the substrate that makes Option B trustworthy. Without governance, an "agent workbench" is just a prompt collection.
- Option C's UX is necessary to get adoption; without an init script and clean docs, the workbench is invisible.
- Option D follows for free if A, B, C are done well.

### Tagline candidates

- "ROWS — A repo-orchestrated worker system. Multi-agent ready. Governance built in."
- "ROWS — The repo is the operating system. Workers are replaceable."
- "ROWS — Your agent team's constitution, lifecycle, and continuity. In one fork."
- "ROWS — Where AGENTS.md meets git worktrees, MCP, and verification gates."

The fourth is closest to Option B; the second is closest to Option A.

---

## 4. Who Should Use This Repo

| Persona | Fit | Why |
|---------|-----|-----|
| Solo developer using one AI tool | High | Imposes useful discipline; light overhead. |
| Solo dev orchestrating 2–3 AI tools | Very high | Capability registry + handoffs solve the coordination problem. |
| Small team using AI agents heavily | High | Multi-worker mode, locks, switching protocol. |
| Agency / consultancy doing AI-assisted client work | Very high | Auditable trail, no-self-close, verification gates. |
| Education / training | High | Examples, prompt library, clear governance. |
| Greenfield startup MVP | Medium | Useful but heavyweight for pure speed. |
| Existing large codebase | Low–Medium | Process can layer on, but governance overhead may slow adoption. |
| Hackathons / rapid prototyping | Low | Too much ceremony. |
| Production deployment automation | Low | This is a development-time template, not deploy infra. |

---

## 5. Who Should NOT Use This Repo

- Anyone who wants Copilot-only workflows. ROWS intentionally excludes Copilot configuration.
- Anyone who needs a *runnable application* template. ROWS is governance and process; you bring the code.
- Anyone allergic to file-based ceremony. ROWS produces task files, lock files, handoff files, verification reports. That is by design.
- Teams that already have established multi-agent governance and just need an AGENTS.md. They'll find ROWS heavyweight.

Being honest about non-fit is a positioning advantage.

---

## 6. Why Not Just `AGENTS.md`?

The agents.md community has converged on a single-file convention. ROWS is **multi-file**. Justification:

- One file cannot hold a constitution + lifecycle + state + handoffs + reassignment protocol + 10 worker definitions + capability registry + risk register + ADRs + examples without becoming unreadable.
- Multi-file enables auditing via folder layout (`tasks/in-progress/` is a glanceable state).
- Multi-file enables tooling (`validate-tasks.mjs` reads `tasks/`; `check-dod.mjs` reads `review/`).
- Multi-file enables version control of state (`git log agent-os/state/system-state.json` shows phase changes).

ROWS uses `AGENTS.md` as the **doorway** to the multi-file system. This is consistent with the agents.md spec, which permits and even encourages linking out to richer documentation.

---

## 7. Differentiators vs. Alternative Templates

The audit looked at current-ecosystem templates. ROWS has measurable advantages over generic alternatives:

| Differentiator | ROWS | Most templates |
|---------------|------|----------------|
| Worker replaceability built into protocol | Yes | No |
| No-self-close rule | Yes | No |
| Capability registry separate from worker identity | Yes | No |
| Task lifecycle as folder structure | Yes | Sometimes |
| Mandatory handoffs | Yes | Rare |
| Reassignment record format | Yes | No |
| Validation suite + CI for the template itself | Yes (10 scripts) | Rare |
| Template-neutrality enforcement (placeholder validator) | Yes | No |
| Multiple coexisting tool adapters | Yes (6) | 1–2 |
| Risk register pre-populated with multi-agent-specific risks | Yes (10) | No |
| Decision register (machine + human) | Yes | Sometimes |

These differentiators are valuable and should be **prominent** in any rewritten README and TEMPLATE_USAGE.

---

## 8. Where ROWS Should Concede

Acknowledge what ROWS is **not**:

- Not a Copilot-friendly system. State this once, with rationale, and move on.
- Not zero-config. Some discipline is required.
- Not a runnable app — `src/` and `tests/` are intentionally generic.
- Not the only way. Spec-driven, single-agent, and monolithic-rules approaches all have merit.
- Not a model — it works with whatever model your worker is configured to use.
- Not an MCP server itself — it consumes them.

Being explicit about non-claims protects the brand.

---

## 9. Marketing Surface (if published as a public template)

Recommended assets to add when promoting:

1. A 60-second README hero with one diagram (lifecycle + 4-layer assignment).
2. A "Why ROWS over X?" section comparing to (a) plain `AGENTS.md`, (b) BMAD, (c) GitHub Spec Kit, (d) Augment Intent.
3. A short demo video / GIF showing a fresh fork through `npm run init` and a first task.
4. Status badges (CI, license, version, "AGENTS.md compatible," "MCP-ready").
5. Topics on GitHub: `ai-agents`, `agents-md`, `mcp`, `multi-agent`, `template`, `windsurf`, `claude-code`, `codex`, `git-worktree`.
6. A `STATUS.md` (auto-generated) showing the template's own internal state — meta but compelling.

---

## 10. Distribution Strategy (if applicable)

If the owner wants this to be widely adopted:

- **Channels:** agents.md community, `r/aiagents`, Hacker News, dev.to, the relevant tool Discords (Claude Code, Cursor, Windsurf, Codex CLI, Aider).
- **Cadence:** weekly update post during active development; monthly when stable.
- **Onboarding loop:** README → fork → `npm run init` → first task → handoff → verification → blog/case-study.
- **Feedback loop:** issue templates already provide structured intake; encourage `worker_handoff` issues from real users.
- **Versioning:** semantic; v1.0.0 only after the Wave 4 priorities in the backlog are complete.

---

## 11. Risks of Current Positioning

Three risks to watch:

### Risk 1 — "Heavyweight perception"

The repo has 60+ Markdown files. New users may bounce. **Mitigation:** Init script (M7), trim README, push deep docs behind links.

### Risk 2 — "Stale-by-default appearance"

Without active demonstrations (X1–X5) and a generated STATUS.md (O5), a visitor cannot tell if the system is alive.
**Mitigation:** Add active-state examples and STATUS.md.

### Risk 3 — "Tool-vendor obsolescence"

Adapters reference current 2026 tool names (Claude Code, Codex, Cursor, Windsurf, Antigravity, Hermes, Gemini). New tools emerge constantly. **Mitigation:** Keep adapters minimal (each adapter is a thin file). Anchor on capability registry, not tool names. Document an "adding a new worker" recipe.

---

## 12. Decision Required from the Human Owner

Before significant positioning work, the owner should answer:

1. **Is this for me, or for the world?** Solo internal tool vs public template — different polish bars.
2. **Which lead identity (A / B / C / D)?** Determines which backlog waves to prioritize.
3. **Is Copilot exclusion final?** If yes, document rationale once. If maybe, plan for it.
4. **What's the version 1.0 bar?** Suggest: Waves 1, 2, 3 of the backlog.
5. **Distribution intent?** Public GitHub template repo + announce, or private starting point.

---

## 13. Recommended One-Sentence Positioning

If the owner agrees with Option B as primary:

> **"ROWS is a fork-and-run repository that turns multi-agent AI development into a governed, replayable, audit-able process — with MCP, git worktrees, and verification gates built in."**

If the owner prefers Option A:

> **"ROWS is the constitution and operating system for multi-agent software development — capability-routed, worker-replaceable, no-self-close."**

Either is defensible. Option B aligns better with the brief's "current AI ecosystem" emphasis.

---

## 14. Related Files

- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/agent-template-readiness-audit.md` — Audit findings
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/current-ai-agent-workflow-research.md` — Research basis
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/backlog/template-improvement-backlog.md` — Improvement backlog
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/verification/release-readiness-checklist.md` — Release readiness gates
- `@/Users/theca/CascadeProjects/windsurf-project-7/AGENTS.md` — Constitution
- `@/Users/theca/CascadeProjects/windsurf-project-7/PROJECT_GOAL.md` — Intake form
