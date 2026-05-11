> **New to this repo?** Read `agent-os/BOOTSTRAP.md` before this file.

# GEMINI.md — Gemini Adapter

> **This file is an adapter. It translates repo rules for Gemini. The authoritative source is [`AGENTS.md`](./AGENTS.md).**
> **Gemini should treat this file as import-style guidance. Read `AGENTS.md` first, then use this file for Gemini-specific instructions.**

---

## Required Reading (Import Order)

Gemini must read the canonical startup order first:

1. **Import:** [`AGENTS.md`](./AGENTS.md) — The constitution. Primary source of truth.
2. **Import:** [`agent-os/startup-sequence.md`](./agent-os/startup-sequence.md) — Canonical startup order and reading checklist.
3. **Import:** [`agent-os/workers/gemini-worker.md`](./agent-os/workers/gemini-worker.md) — Your role definition.

---

## Gemini's Role in ROWS

Gemini is best used for:
- **Research** — Investigating technologies, patterns, and approaches.
- **Long-document analysis** — Processing large specs, RFCs, or documentation.
- **Multimodal analysis** — Analyzing screenshots, diagrams, UI mockups.
- **Planning** — Creating detailed plans from high-level goals.
- **Comparative analysis** — Evaluating trade-offs between approaches.

Gemini is **not** best for:
- Direct file editing in the repo (use Windsurf or Codex).
- Browser-based verification (use Antigravity).
- Git operations (use Windsurf).

---

## Session Workflow

1. **Startup:** Import and read all required files listed above.
2. **Claim a task:** Find an unclaimed task in `agent-os/tasks/ready/`. Move it to `claimed/`. Create a lock.
3. **Execute:** Follow the task's objective. Stay in scope. Produce evidence.
4. **Handoff:** Write a handoff using the template at [`agent-os/handoffs/handoff-template.md`](./agent-os/handoffs/handoff-template.md).
5. **Never self-close:** Do not move your own task to `done/`.

---

## Gemini-Specific Rules

- Use `.gemini/settings.json` for Gemini-specific configuration.
- When researching, log findings in [`docs/04-research/research-log.md`](./docs/04-research/research-log.md).
- When analyzing documents, cite specific sections or page numbers.
- Prefer structured output (tables, lists, comparisons) for clarity.

---

## Template Neutrality

This is a template repository. Do not add application-specific code. Do not create Copilot configuration files. Use intentional template markers instead of vague placeholders.

## Related Files

- [`.gemini/README.md`](./.gemini/README.md) — Gemini directory setup
- [`.gemini/settings.json`](./.gemini/settings.json) — Gemini configuration
- [`agent-os/workers/gemini-worker.md`](./agent-os/workers/gemini-worker.md) — Worker role definition
- [`prompt-library/`](./prompt-library/) — Copy/paste prompts for workers
- [`examples/`](./examples/) — Sample artifacts (illustrative only)
- [`TEMPLATE_READINESS.md`](./TEMPLATE_READINESS.md) — Template readiness gates
