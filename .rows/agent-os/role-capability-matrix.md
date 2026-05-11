# Role-Capability Matrix

> **Maps roles to capabilities and preferred workers. Use this to route tasks to the right worker.**

---

## Roles

Roles are jobs. Workers are tools. A role describes the type of work being performed. A worker describes the AI tool or human executing the work.

A single worker may perform multiple roles. A single role may be performed by different workers over time.

---

## Role Definitions

### Goal Builder

**Purpose:** Decompose the project goal from `PROJECT_GOAL.md` into actionable task files.

**Required capabilities:**
- goal-decomposition
- task-decomposition
- project-planning

**Preferred workers:** Hermes, Claude

**May also be performed by:** Gemini, Windsurf

---

### Project Planner

**Purpose:** Plan project phases, milestones, task ordering, and dependencies.

**Required capabilities:**
- project-planning
- task-decomposition
- coordination

**Preferred workers:** Hermes, Claude

**May also be performed by:** Gemini

---

### Architect

**Purpose:** Design system architecture, make technology decisions, create ADRs.

**Required capabilities:**
- architecture-planning
- security-review
- documentation

**Preferred workers:** Claude

**May also be performed by:** Gemini, Windsurf

---

### Researcher

**Purpose:** Research technologies, patterns, approaches, and external information.

**Required capabilities:**
- research
- documentation

**Preferred workers:** Gemini

**May also be performed by:** Claude, Hermes

---

### Backend Builder

**Purpose:** Implement backend services, APIs, database schemas, and server logic.

**Required capabilities:**
- backend-implementation
- code-implementation
- test-writing
- debugging

**Preferred workers:** Codex, Windsurf

**May also be performed by:** Claude, Antigravity

---

### Frontend Builder

**Purpose:** Implement frontend UI, components, styles, and client-side logic.

**Required capabilities:**
- frontend-implementation
- code-implementation
- test-writing

**Preferred workers:** Windsurf, Codex

**May also be performed by:** Claude, Antigravity

---

### QA Verifier

**Purpose:** Verify that implementations meet acceptance criteria, write and run tests.

**Required capabilities:**
- verification
- test-writing
- ui-browser-verification
- debugging

**Preferred workers:** Antigravity, Codex

**May also be performed by:** Windsurf, Claude

---

### Documentation Maintainer

**Purpose:** Write and maintain project documentation, ADRs, API docs, and guides.

**Required capabilities:**
- documentation
- repo-navigation

**Preferred workers:** Claude

**May also be performed by:** Gemini, Windsurf, Hermes

---

### Release Reviewer

**Purpose:** Review completed work before release, check security, verify DoD.

**Required capabilities:**
- release-review
- security-review
- verification

**Preferred workers:** Claude

**May also be performed by:** Hermes, Antigravity

---

### Coordinator

**Purpose:** Coordinate multi-worker efforts, review task queues, generate status reports.

**Required capabilities:**
- coordination
- task-decomposition
- handoff-writing

**Preferred workers:** Hermes

**May also be performed by:** Claude, Windsurf

---

## Capability Definitions

| Capability | Description | Preferred Workers | Common Roles |
|-----------|-------------|-------------------|--------------|
| goal-decomposition | Break a project goal into discrete tasks | Hermes, Claude | Goal Builder |
| project-planning | Plan phases, milestones, and task ordering | Hermes, Claude | Project Planner, Architect |
| architecture-planning | Design system architecture and make tech decisions | Claude | Architect |
| research | Research technologies, patterns, and external info | Gemini | Researcher |
| code-implementation | Write production code | Codex, Windsurf | Backend Builder, Frontend Builder |
| frontend-implementation | Build UI components and client logic | Windsurf, Codex | Frontend Builder |
| backend-implementation | Build APIs, services, and server logic | Codex, Windsurf | Backend Builder |
| test-writing | Write unit, integration, and e2e tests | Codex, Antigravity | QA Verifier, Backend Builder, Frontend Builder |
| ui-browser-verification | Verify UI behavior in a browser | Antigravity | QA Verifier |
| documentation | Write and maintain documentation | Claude | Documentation Maintainer, Architect |
| mcp-tool-use | Use MCP servers safely for scoped tool access and resource reads | Claude, Hermes | Architect, Coordinator, Documentation Maintainer |
| mcp-resource-read | Read MCP resources without granting write access | Claude, Hermes | Researcher, Documentation Maintainer |
| prompt-safety | Evaluate external content and fetched instructions for prompt-injection risk | Claude, Hermes | Architect, QA Verifier, Coordinator |
| worktree-management | Set up and maintain git worktrees for parallel execution | Hermes, Windsurf | Coordinator, Backend Builder, Frontend Builder |
| scaffolding | Initialize or scaffold a fork from template inputs | Hermes, Claude | Goal Builder, Project Planner, Coordinator |
| coordination | Coordinate multi-worker efforts | Hermes | Coordinator |
| release-review | Review work before release | Claude | Release Reviewer |
| security-review | Review code and architecture for security issues | Claude | Release Reviewer, Architect |
| refactoring | Improve code structure without changing behavior | Codex, Windsurf | Backend Builder, Frontend Builder |
| debugging | Find and fix bugs | Codex, Windsurf | Backend Builder, Frontend Builder, QA Verifier |
| task-decomposition | Break work into claimable task files | Hermes, Claude | Goal Builder, Project Planner, Coordinator |
| verification | Verify work against acceptance criteria | Antigravity, Codex | QA Verifier, Release Reviewer |
| repo-navigation | Navigate and understand repository structure | Windsurf, Claude | All roles |
| file-editing | Create, modify, and delete files in the repo | Windsurf, Codex | Backend Builder, Frontend Builder |
| handoff-writing | Write clear, actionable handoff files | All workers | All roles |
| evidence-production | Produce verifiable evidence of completion | All workers | All roles |

---

## Worker-to-Capability Quick Reference

| Worker | Primary Capabilities |
|--------|---------------------|
| **Codex** | code-implementation, refactoring, test-writing, debugging |
| **Claude** | architecture-planning, documentation, security-review, release-review, large-context reasoning |
| **Gemini** | research, long-document analysis, project-planning |
| **Windsurf** | file-editing, code-implementation, repo-navigation, scaffolding |
| **Cursor** | file-editing, repo-navigation, scaffolding, lightweight orchestration |
| **Antigravity** | ui-browser-verification, test-writing, evidence-production |
| **Hermes** | task-decomposition, coordination, goal-decomposition, project-planning |

---

## Related Files

- [`assignment-model.md`](./assignment-model.md) — Full assignment hierarchy
- [`execution-modes.md`](./execution-modes.md) — Solo, multi-worker, and hybrid modes
- [`workers/`](./workers/) — Individual worker definitions
- [`roles/`](./roles/) — Individual role definitions
- [`state/capability-registry.json`](./state/capability-registry.json) — Machine-readable capability registry
