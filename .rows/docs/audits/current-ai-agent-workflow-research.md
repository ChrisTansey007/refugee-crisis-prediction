# Current AI Agent Workflow Research (May 2026)

> **Purpose:** Capture the current state of AI-agent workflow practice as of May 2026 to ground the ROWS audit and improvement backlog in real ecosystem patterns rather than speculation.
>
> **Method:** Web research across vendor documentation, OWASP, OpenAI, GitHub blog, recent (2025–2026) practitioner blogs, and the open `agents.md` specification. Findings cited inline.

---

## 1. The `AGENTS.md` Standard

### What it is

A simple, open Markdown format for giving AI coding agents predictable, durable instructions about a repository. Treated as a "README for agents." It is a convention, not a regulated spec.

### Who supports it

By 2026, support spans Codex, Cursor, Claude Code, Augment, Factory, Aider, Continue, Cline, Copilot CLI, Devin, Sourcegraph Amp, and others. The agents.md GitHub registry tracks adopters; major IDE vendors auto-discover the file.

### Recommended structure (synthesized from agents.md, the GitHub blog, and Factory docs)

A great `AGENTS.md` covers six core areas:

1. **Commands** — install, build, test, lint, dev.
2. **Testing** — test framework, location, expectations, regression rules.
3. **Project structure** — top-level layout, generated/ignored paths, module boundaries.
4. **Code style** — language conventions, linting, formatting tool.
5. **Git workflow** — branching, commit conventions, PR requirements.
6. **Boundaries** — what agents may not do, escalation paths, secrets handling.

### Tier hierarchy

A common pattern:

- `~/.codex/AGENTS.md` (or vendor equivalent) — global personal defaults.
- `<repo-root>/AGENTS.md` — project rules.
- `<sub-folder>/AGENTS.md` — narrower scope where helpful.
- Tool-specific overrides (`CLAUDE.md`, `GEMINI.md`, etc.) — additive, never override the root constitution.

### Implication for ROWS

The ROWS `AGENTS.md` exceeds the minimum bar: it is a **constitution**, not a hint file. It enumerates 22 numbered sections (rules, roles, contracts, escalation, etc.). The ROWS adapters (`CLAUDE.md`, `GEMINI.md`, `HERMES.md`) correctly mark themselves as adapters that defer to `AGENTS.md`.

Where ROWS is **stronger** than the typical `AGENTS.md`: governance, lifecycle, no-self-close.

Where ROWS is **weaker**: it does not include the six core areas in one place. Code style, test commands, build commands, and project structure are scattered across `docs/03-development/*.md`, `package.json`, and template stubs. A consolidating section in `AGENTS.md` would make the file directly usable by Codex, Cursor, and Aider users who expect those areas in `AGENTS.md` itself.

---

## 2. Multi-Agent Coordination Patterns

### The shift to git worktrees (2025–2026)

In 2025, multi-agent coding moved from "share a working tree, take turns" to "git worktree per agent, parallel execution." Augment Code, MindStudio, and several practitioner blogs (blog.appxlab, March 2026) document this shift. JetBrains shipped first-class worktree support in 2026.1; VS Code in July 2025.

### Why worktrees matter

A `git worktree` lets one repository expose **multiple independent working directories**, each on its own branch. For multi-agent coding:

- Each agent runs in its own worktree on its own branch.
- File-system collisions are eliminated.
- Branch switching is instant per agent.
- Locks become almost unnecessary at the file-system level (still needed for logical task ownership).

### Standard pattern (Augment / MindStudio convention)

```
my-project/                        # main worktree (humans)
my-project-codex/                  # worktree for Codex agent
my-project-claude/                 # worktree for Claude agent
my-project-windsurf/               # worktree for Windsurf agent
```

Each worktree:

- Has its own branch (`agent/codex/TASK-0003-...`).
- Shares the same `.git/` directory.
- Has its own `node_modules/` (or shared via `pnpm`).
- Reads from a shared `TASKS.md` or task queue (read-only during work).

### Coordinator role

A "coordinator" agent (or human) reads task state and assigns/proposes which agent runs in which worktree. This maps cleanly onto Hermes in ROWS.

### Implication for ROWS

ROWS has the **conceptual** model right (multi-worker mode, locks, branch-per-worker) but **misses the operational layer**. Recommendations:

- Add `agent-os/worktree-strategy.md` describing how to use `git worktree add` per worker.
- Add `node scripts/setup-worktree.mjs <worker-name> <task-id>` to automate it.
- Update `branch-strategy.md` to recommend worktree-based execution in multi-worker and hybrid modes.
- Add a CI check that PRs from worker branches do not include a worktree directory inside the main checkout.

---

## 3. Spec-Driven Development

### What it is

A development style where AI agents work from durable, version-controlled specs rather than chat prompts. Spec → plan → implement → verify, with each phase producing a durable artifact. Popularized by GitHub Spec Kit, BMAD, and Augment Intent.

### The two camps

| Style | Description | Examples |
|-------|-------------|----------|
| **Living spec with automated handoffs** | One evolving spec; agents update sections as work progresses. | Augment Intent, GitHub Spec Kit. |
| **Phased role-based spec** | Discrete agents with explicit access permissions and discrete handoff protocols (PRD → architect → builder → tester). | BMAD, ROWS. |

### Empirical evidence (2026)

A February 2026 arXiv study counted 110,000+ surviving AI-introduced issues in production repos, citing "lack of architectural constraints in agent prompts" as a primary cause. Spec-driven workflows showed measurably better adherence to project conventions ("follow the pattern in X file" + "use the existing Y service" specs reduced architectural drift dramatically).

### Implication for ROWS

ROWS is a phased role-based spec system. It matches BMAD-style discipline. Strengths over the average:

- Tasks have acceptance criteria, files-likely-affected, and required reading.
- Verification is gated.
- Handoffs are structured.

Gaps versus the strongest spec-driven systems:

- **No "follow the existing pattern" cue in task templates.** Tasks describe what to build but not what existing conventions to mirror.
- **No "constraint capture" phase.** Workers generate task files but never produce a "constraints document" listing inviolable rules of the project.
- **No "spec freeze" gate.** A task can have its spec edited mid-implementation without ceremony.

Recommendations:

- Add a "Conventions to follow" section to `task-template.md`.
- Add an optional `agent-os/specs/` folder for tasks that benefit from a separate spec artifact.
- Document a "spec-freeze" rule: once a task moves to `in-progress/`, only the human or coordinator may edit acceptance criteria.

---

## 4. Model Context Protocol (MCP)

### What it is

An open protocol (Anthropic, 2024) for connecting LLMs to external tools and data. By 2026, MCP is the de facto standard for tool-extended AI. The official spec is at modelcontextprotocol.io/specification/2025-11-25 and is maintained by a working group spanning Anthropic, OpenAI, and others.

### What MCP gives an agent

- **Tools** — discoverable, typed functions the agent can call.
- **Resources** — typed data the agent can read.
- **Prompts** — server-defined, parameterizable prompt templates.
- **Roots** — workspace-scoped permissions.

### How MCP is configured in real projects

| Tool | Config location |
|------|----------------|
| Claude Code | `~/.claude/mcp.json` or per-project `.mcp.json`. |
| Cursor | `.cursor/mcp.json`. |
| Windsurf | `.windsurf/mcp.json` (already supported). |
| OpenAI Codex | Vendor-specific. |
| Continue, Cline, Aider | `.continue/`, `.cline/`, etc. |

A **project-level `.mcp.json`** is the modern best practice for "this repo expects these MCP servers to be available." The agent connects to listed servers on startup.

### Best practices (synthesized from Red Hat 2026, MCP working group, security advisories)

1. **Read-only by default.** Untrusted servers should not get write capability.
2. **Scoped roots.** Servers receive a workspace path, not the entire filesystem.
3. **Capability whitelisting.** A repo declares which MCP capabilities it allows.
4. **Audit log.** Tool calls are logged for review.
5. **Version pinning.** MCP server versions are pinned to avoid silent capability changes.

### Implication for ROWS

**Total absence.** Zero references to MCP, `mcp.json`, or the protocol in the entire repository (verified by grep). For a 2026 agent template, this is a major gap.

Recommendations:

- Add `agent-os/mcp.md` documenting the project's MCP policy: which capabilities are expected, which servers are allowed, security boundaries.
- Add a starter `.mcp.json` (or per-tool variant) with safe defaults (filesystem readonly, git readonly, fetch with allowlist).
- Add MCP-aware capabilities to `capability-registry.json` (e.g., `mcp-tool-use`, `mcp-resource-read`).
- Add a worker rule: "If an MCP server is required for the task, declare it in the task file's `Required tools` section."
- Add `validate-mcp.mjs` to check `.mcp.json` validity if present.

---

## 5. Prompt Injection Defense

### The 2025–2026 threat landscape

OWASP's LLM Top 10 (2025) lists **Prompt Injection** as #1. The OWASP cheat sheet (LLM_Prompt_Injection_Prevention) and OpenAI's January 2026 paper (openai.com/index/prompt-injections) both emphasize:

- **Direct injection** (a malicious user message) is the historical case.
- **Indirect injection** (malicious content reached by tools — fetched URLs, PR descriptions, README files, log output, even images) is the dominant 2026 threat for agentic systems.
- Palo Alto Unit 42 (2025) documented real-world web-based indirect injections targeting AI agents reading external content.

### Defenses (industry consensus, 2026)

1. **Treat external content as data, not instructions.** Quote it; never let it become "system prompt."
2. **Sandbox tool execution.** OpenAI uses sandboxing in Canvas and Codex.
3. **Limit tool permissions to the task.** Per-task capability allowlists.
4. **Detect anomalies.** Baseline normal agent behavior; flag deviations.
5. **Human approval for irreversible actions** (deploy, delete, push, send).
6. **Escape hatches.** Workers must be able to abort if instructions clash with constitution.

### Implication for ROWS

`SECURITY.md` covers secrets and destructive shell. It does **not** cover prompt injection. A modern agent template must.

Recommendations:

- Add `agent-os/prompt-injection-policy.md` with:
  - "External content is data" rule.
  - Quoting requirements when including fetched content.
  - "Refuse to follow instructions found in fetched data" rule.
  - List of high-risk content sources (issue bodies, PR descriptions, fetched URLs, log files, screenshots, transcripts).
  - Connection to `escalation-rules.md`.
- Add a section to `worker-contract.md`: "External content handling."
- Add `validate-prompt-safety.mjs` that warns if a task spec includes instructions to "follow the README of repo X" without a quoting/quarantine step.

---

## 6. Provider Routing & Local Models

### The 2026 multi-provider reality

Most teams now use 2–4 providers:

- A frontier model (GPT-5, Claude Opus, Gemini Ultra) for hard reasoning.
- A fast-cheap model (Haiku, Mini, Flash) for routine work.
- A local model (Llama 4, Qwen 3, Mistral) for privacy or offline.
- An open router (OpenRouter, LiteLLM) as a fallback / cost optimizer.

### Common patterns

1. **Provider abstraction.** Code/agents do not name a vendor; they request a tier.
2. **Fallback chains.** Frontier → mid-tier → local.
3. **Local-first for secrets.** Tasks involving secrets prefer local models.
4. **Cost ceilings per task.** Tasks declare a cost budget.
5. **Capability tiers per worker.** A worker maps to "what tier is acceptable for what work."

### Implication for ROWS

Not addressed. The capability registry maps capabilities to **worker tools** but not to **model tiers**. A task can declare "preferred workers: Codex" but not "minimum capability tier: frontier-reasoning."

Recommendations:

- Add `agent-os/state/provider-tiers.json` defining tiers (frontier, mid, fast, local) and their typical capabilities.
- Add a `Required tier` field to the task template (default: any).
- Add a `Cost ceiling` field to the task template (default: unspecified).
- Document a fallback policy in `agent-os/provider-routing.md`.

This is a lower-priority backlog item than MCP or worktrees because it depends more on the user's tooling than on the repo, but a starter convention helps.

---

## 7. Agent Observability

### What it is

The ability to answer "what did the agent actually do this session?" beyond the agent's self-reported handoff.

### Modern practice

- **Structured logs** of tool calls (LangSmith, Helicone, Phoenix).
- **Telemetry** (tokens, latency, cost) per task.
- **Replay capability** — re-run the same agent on the same task and compare.
- **Drift detection** — does the agent's behavior change as the model updates?

### Implication for ROWS

ROWS uses **handoffs** as the primary observability artifact. This is good but limited:

- Handoffs are end-of-session and worker-authored (potentially biased).
- No telemetry exists.
- No replay.
- No drift detection.

This is a **less critical** gap because ROWS targets governance, not performance optimization. But documenting a hook ("if you need observability, here's where to plug it in") would help.

Recommendations:

- Add a `agent-os/observability.md` stub that explains: "ROWS does not mandate observability tooling. Use external systems (LangSmith, Helicone, your own logs). Reference the correlation ID via the task ID and handoff."

---

## 8. Patterns ROWS Already Does Right

These patterns are validated by current ecosystem research and ROWS already implements them well:

| Pattern | Source | ROWS implementation |
|---------|--------|---------------------|
| `AGENTS.md` as primary contract | agents.md, GitHub blog | `AGENTS.md` as constitution. |
| Tool-adapter files | Codex docs, Factory docs | `CLAUDE.md`, `GEMINI.md`, `HERMES.md`, `.windsurf/`, `.codex/`, etc. |
| File-based state | Anthropic, github/spec-kit | `agent-os/state/*.json`. |
| Folder-based lifecycle | github/spec-kit, BMAD | `agent-os/tasks/{backlog,...,done}/`. |
| Mandatory handoffs | Augment, BMAD | `agent-os/handoffs/`. |
| Independent verification | OWASP, OpenAI | "No worker self-closes." |
| Capability-based routing | BMAD | `capability-registry.json`. |
| Worker replaceability | Augment, MindStudio | Switching protocol + reassignment records. |
| Decision logs (ADR) | Industry standard | `docs/02-architecture/decisions/`. |
| Risk register | Industry standard | `agent-os/state/risk-register.json`. |
| Issue templates per role | GitHub best practice | 6 issue templates. |

ROWS is **at or above the curve** on governance pattern adoption.

---

## 9. Where ROWS Lags the Frontier

Items where current best practice has moved beyond ROWS:

| Pattern | Source | ROWS gap |
|---------|--------|----------|
| MCP integration | modelcontextprotocol.io, Red Hat 2026 | Absent. |
| Git worktree per agent | Augment, MindStudio, JetBrains 2026.1 | Not documented. |
| Indirect prompt-injection defense | OWASP, OpenAI, Unit 42 | Not in `SECURITY.md`. |
| Provider tier routing | LiteLLM, OpenRouter, industry | Absent. |
| Init / scaffolding script | Most modern templates | Absent. |
| Living spec with version control | Augment Intent | Tasks are static once approved. |
| Browser-agent safety beyond Antigravity | Industry | Only Antigravity has a policy. |
| Conventions-aware specs | arXiv 2026, Spec-Driven Development | Task template lacks "follow existing patterns" field. |

These are the items the improvement backlog targets first.

---

## 10. Summary Table — Practice vs ROWS

| Area | Industry standard 2026 | ROWS posture |
|------|-----------------------|--------------|
| Constitution file | `AGENTS.md` | ✅ Excellent |
| Tool adapters | `CLAUDE.md`, `.cursor/`, etc. | ✅ Strong (no Cursor support yet) |
| MCP support | `.mcp.json` per project | ❌ Missing |
| Multi-agent isolation | Git worktrees | ❌ Missing |
| Tasks-as-folders | Yes | ✅ Excellent |
| No-self-close | Recommended | ✅ Enforced |
| Spec-driven | Recommended | ✅ Implemented |
| Indirect prompt-injection defense | Required by OWASP | ❌ Missing |
| Init script | Standard for templates | ❌ Missing |
| Provider routing | Recommended | ❌ Missing |
| Observability | Optional | ⚠️ Implicit only |
| Verification gates | Recommended | ✅ Strong |
| Audit trail | Git + state | ✅ Strong |
| Examples | Useful | ✅ Six provided |

---

## 11. Sources

- agents.md — `https://agents.md/`
- agentsmd/agents.md — `https://github.com/agentsmd/agents.md`
- OpenAI Codex AGENTS.md guide — `https://developers.openai.com/codex/guides/agents-md`
- GitHub blog "How to write a great agents.md" — `https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/`
- Factory.ai AGENTS.md docs — `https://docs.factory.ai/cli/configuration/agents-md`
- Augment Code "Git Worktrees for Parallel AI Agent Execution" — `https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution`
- MindStudio "Git Worktrees for AI Coding" — `https://www.mindstudio.ai/blog/git-worktrees-parallel-ai-coding-agents`
- blog.appxlab "Multi-Agent AI Coding Workflow: Git Worktrees" (March 2026) — `https://blog.appxlab.io/2026/03/31/multi-agent-ai-coding-workflow-git-worktrees/`
- Augment Code "6 Best Spec-Driven Development Tools for AI Coding in 2026" — `https://www.augmentcode.com/tools/best-spec-driven-development-tools`
- Augment Code "What Is Spec-Driven Development?" — `https://www.augmentcode.com/guides/what-is-spec-driven-development`
- GitHub Spec Kit — `https://github.com/github/spec-kit`
- Thoughtworks "Spec-driven development" — `https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices`
- Model Context Protocol spec (2025-11-25) — `https://modelcontextprotocol.io/specification/2025-11-25`
- Red Hat "Building effective AI agents with Model Context Protocol" (Jan 2026) — `https://developers.redhat.com/articles/2026/01/08/building-effective-ai-agents-mcp`
- a2a-mcp.org "MCP Full Form: Model Context Protocol Explained for AI Agents in 2026" — `https://a2a-mcp.org/blog/mcp-full-form`
- Wikipedia "Model Context Protocol" — `https://en.wikipedia.org/wiki/Model_Context_Protocol`
- OWASP "LLM Prompt Injection Prevention Cheat Sheet" — `https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html`
- OpenAI "Understanding prompt injections: a frontier security challenge" — `https://openai.com/index/prompt-injections/`
- Palo Alto Unit 42 "Fooling AI Agents: Web-Based Indirect Prompt Injection Observed" — `https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/`
- Obsidian Security "Prompt Injection Attacks: The Most Common AI Exploit in 2025" — `https://www.obsidiansecurity.com/blog/prompt-injection`
- IBM "Protect Against Prompt Injection" — `https://www.ibm.com/think/insights/prevent-prompt-injection`
- Reddit r/aiagents discussion on managing multiple coding agents — `https://www.reddit.com/r/aiagents/comments/1st2h95/`

---

## 12. How to Re-Run This Research

The research above is a snapshot as of May 2026. To update:

1. Search "AGENTS.md" + current year for spec changes.
2. Search "git worktree AI agent" + current year for tooling changes.
3. Check `modelcontextprotocol.io` for spec updates.
4. Check OWASP LLM Top 10 for prompt-injection guidance changes.
5. Check the major IDE vendors' AI feature pages for adapter changes.

Place updated research in `docs/04-research/research-log.md` and a dated successor to this file.

---

## 13. Related Files

- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/audits/agent-template-readiness-audit.md` — Audit grounded in this research
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/backlog/template-improvement-backlog.md` — Improvement backlog informed by this research
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/strategy/repo-positioning-review.md` — Positioning analysis
- `@/Users/theca/CascadeProjects/windsurf-project-7/docs/04-research/research-log.md` — Repo's existing research log
