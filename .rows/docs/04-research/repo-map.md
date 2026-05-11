# ROWS Repo Map

> Generated from [agent-os/state/knowledge-graph.json](../../agent-os/state/knowledge-graph.json) by `npm run graph:build`.

## Generated Metadata

- Generated at: 2026-05-09T15:31:26.850Z
- Nodes: 330
- Edges: 714
- Orphans flagged: 128

## Executive Summary

- Tasks mapped: 17
- ADRs mapped: 3
- Active handoffs mapped: 4
- Skills mapped: 11

## Task Dependency Graph

| Task | Status | Depends on | Blocks |
|---|---|---|---|
| [TASK-0001](../../agent-os/tasks/backlog/TASK-0001-initialize-project-from-goal.md) | backlog | none | none |

## ADR and Decision Coverage

| ADR | Referenced by |
|---|---|
| [ADR-0001](../../docs/02-architecture/decisions/ADR-0001-repo-orchestrated-worker-system.md) | decision-register.json, Decision Register |
| [ADR-0002](../../docs/02-architecture/decisions/ADR-0002-template-fork-workflow.md) | decision-register.json, Decision Register |
| [ADR-0003](../../docs/02-architecture/decisions/ADR-0003-flexible-worker-assignment.md) | decision-register.json, Decision Register |

## Handoff Context Flow

| Handoff | Task | Distilled? |
|---|---|---|
| [handoff-checkpoint-template.md](../../agent-os/handoffs/active/checkpoints/handoff-checkpoint-template.md) | none | no |
| [README.md](../../agent-os/handoffs/active/checkpoints/README.md) | none | no |
| [EXAMPLE-handoff.md](../../agent-os/handoffs/active/EXAMPLE-handoff.md) | none | no |
| [README.md](../../agent-os/handoffs/active/README.md) | none | no |

## Onboarding and Skill Entry Points

| Source | Target | Type |
|---|---|---|
| [agent-os/BOOTSTRAP.md](../../agent-os/BOOTSTRAP.md) | [agent-os/knowledge-model.md](../../agent-os/knowledge-model.md) | onboards_to |
| [agent-os/skills/auto-promote.md](../../agent-os/skills/auto-promote.md) | [agent-os/reports/promotion-log.md](../../agent-os/reports/promotion-log.md) | links_to |
| [agent-os/skills/auto-promote.md](../../agent-os/skills/auto-promote.md) | [agent-os/skills/worker-loop.md](../../agent-os/skills/worker-loop.md) | links_to |
| [agent-os/skills/auto-promote.md](../../agent-os/skills/auto-promote.md) | [agent-os/task-lifecycle.md](../../agent-os/task-lifecycle.md) | links_to |
| [agent-os/skills/claim-task.md](../../agent-os/skills/claim-task.md) | [agent-os/locks/lock-template.json](../../agent-os/locks/lock-template.json) | links_to |
| [agent-os/skills/claim-task.md](../../agent-os/skills/claim-task.md) | [agent-os/skills/enrich-task.md](../../agent-os/skills/enrich-task.md) | links_to |
| [agent-os/skills/claim-task.md](../../agent-os/skills/claim-task.md) | [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | links_to |
| [agent-os/skills/claim-task.md](../../agent-os/skills/claim-task.md) | [agent-os/tasks/task-template.md](../../agent-os/tasks/task-template.md) | links_to |
| [agent-os/skills/complete-task.md](../../agent-os/skills/complete-task.md) | [agent-os/definition-of-done.md](../../agent-os/definition-of-done.md) | links_to |
| [agent-os/skills/complete-task.md](../../agent-os/skills/complete-task.md) | [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | links_to |
| [agent-os/skills/complete-task.md](../../agent-os/skills/complete-task.md) | [agent-os/verification-gates.md](../../agent-os/verification-gates.md) | links_to |
| [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | [agent-os/checklists/before-commit.md](../../agent-os/checklists/before-commit.md) | links_to |
| [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | [agent-os/checklists/task-closeout.md](../../agent-os/checklists/task-closeout.md) | links_to |
| [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | [agent-os/handoffs/handoff-template.md](../../agent-os/handoffs/handoff-template.md) | links_to |
| [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | [agent-os/task-lifecycle.md](../../agent-os/task-lifecycle.md) | links_to |
| [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | [AGENTS.md](../../AGENTS.md) | links_to |
| [agent-os/skills/worker-loop.md](../../agent-os/skills/worker-loop.md) | [agent-os/protocols/autonomous-continuation.md](../../agent-os/protocols/autonomous-continuation.md) | links_to |
| [agent-os/skills/worker-loop.md](../../agent-os/skills/worker-loop.md) | [agent-os/skills/auto-promote.md](../../agent-os/skills/auto-promote.md) | links_to |
| [agent-os/skills/worker-loop.md](../../agent-os/skills/worker-loop.md) | [agent-os/skills/enrich-task.md](../../agent-os/skills/enrich-task.md) | links_to |
| [agent-os/skills/worker-loop.md](../../agent-os/skills/worker-loop.md) | [agent-os/skills/session-close.md](../../agent-os/skills/session-close.md) | links_to |
| [agent-os/skills/worker-loop.md](../../agent-os/skills/worker-loop.md) | [agent-os/triggers/README.md](../../agent-os/triggers/README.md) | links_to |
| [agent-os/skills/worker-loop.md](../../agent-os/skills/worker-loop.md) | [AGENTS.md](../../AGENTS.md) | links_to |

## Skills and Protocol Usage

| Skill/Protocol | Referenced by |
|---|---|
| [autonomous-continuation.md](../../agent-os/protocols/autonomous-continuation.md) | agent-os/skills/worker-loop.md, AGENTS.md, docs/04-research/repo-map.md |
| [blocker-protocol.md](../../agent-os/protocols/blocker-protocol.md) | docs/04-research/repo-map.md |
| [auto-promote.md](../../agent-os/skills/auto-promote.md) | agent-os/protocols/autonomous-continuation.md, agent-os/skills/worker-loop.md, docs/04-research/repo-map.md |
| [claim-task.md](../../agent-os/skills/claim-task.md) | docs/04-research/repo-map.md |
| [complete-task.md](../../agent-os/skills/complete-task.md) | docs/04-research/repo-map.md |
| [distill-handoffs.md](../../agent-os/skills/distill-handoffs.md) | docs/04-research/repo-map.md |
| [enrich-task.md](../../agent-os/skills/enrich-task.md) | agent-os/skills/claim-task.md, agent-os/skills/worker-loop.md, docs/04-research/repo-map.md |
| [escalate-blocker.md](../../agent-os/skills/escalate-blocker.md) | docs/04-research/repo-map.md |
| [resolve-blocker.md](../../agent-os/skills/resolve-blocker.md) | docs/04-research/repo-map.md |
| [self-install.md](../../agent-os/skills/self-install.md) | docs/04-research/repo-map.md |
| [session-close.md](../../agent-os/skills/session-close.md) | agent-os/protocols/autonomous-continuation.md, agent-os/skills/claim-task.md, agent-os/skills/complete-task.md, agent-os/skills/worker-loop.md, AGENTS.md, docs/04-research/repo-map.md |
| [update-knowledge-graph.md](../../agent-os/skills/update-knowledge-graph.md) | docs/04-research/repo-map.md |
| [worker-loop.md](../../agent-os/skills/worker-loop.md) | agent-os/protocols/autonomous-continuation.md, agent-os/skills/auto-promote.md, AGENTS.md, docs/04-research/repo-map.md |

## Orphans and Warnings

- ADRs with no meaningful references: none
- Skills with no meaningful references: none
- Active handoffs with no task edge: agent-os/handoffs/active/checkpoints/handoff-checkpoint-template.md, agent-os/handoffs/active/checkpoints/README.md, agent-os/handoffs/active/EXAMPLE-handoff.md, agent-os/handoffs/active/README.md
- All other orphan candidates: .claude/rules/backend.md, .claude/rules/docs.md, .claude/rules/frontend.md, .claude/rules/orchestration.md, .cursor/rules/backend.md, .cursor/rules/docs.md, .cursor/rules/frontend.md, .cursor/rules/orchestration.md, .cursor/rules/testing.md, .editorconfig, .env.example, .gitattributes, .github/CODEOWNERS, .github/dependabot.yml, .github/ISSUE_TEMPLATE/agent-task.yml, .github/ISSUE_TEMPLATE/architecture-decision.yml, .github/ISSUE_TEMPLATE/bug-report.yml, .github/ISSUE_TEMPLATE/research-task.yml, .github/ISSUE_TEMPLATE/verification-report.yml, .github/ISSUE_TEMPLATE/worker-handoff.yml, .github/workflows/daily-status-report.yml, .github/workflows/daily-triage.yml, .github/workflows/definition-of-done-check.yml, .github/workflows/distill-handoffs.yml, .github/workflows/on-blocker-deadline.yml, .github/workflows/on-task-done.yml, .github/workflows/on-trigger.yml, .github/workflows/stale-task-audit.yml, .github/workflows/template-readiness.yml, .github/workflows/validate-agent-os.yml, .gitignore, .windsurf/workflows/implement-task.md, agent-os/agents/claude/install.md, agent-os/agents/claude/reading-list.md, agent-os/agents/codex/install.md, agent-os/agents/codex/reading-list.md, agent-os/agents/cursor/install.md, agent-os/agents/cursor/reading-list.md, agent-os/agents/cursor/rules/rows-claim-task.md, agent-os/agents/cursor/rules/rows-complete-task.md, agent-os/agents/cursor/rules/rows-escalate-blocker.md, agent-os/agents/cursor/rules/rows-resolve-blocker.md, agent-os/agents/cursor/rules/rows-session-close.md, agent-os/agents/generic/install.md, agent-os/agents/generic/reading-list.md, agent-os/agents/registry.md, agent-os/agents/universal/index.md, agent-os/agents/windsurf/install.md, agent-os/agents/windsurf/reading-list.md, agent-os/agents/windsurf/workflows/rows-claim-task.md, agent-os/agents/windsurf/workflows/rows-complete-task.md, agent-os/agents/windsurf/workflows/rows-escalate-blocker.md, agent-os/agents/windsurf/workflows/rows-resolve-blocker.md, agent-os/agents/windsurf/workflows/rows-session-close.md, agent-os/blockers/blocker-template.md, agent-os/milestones/milestone-template.md, agent-os/observability.md, agent-os/proposals/proposal-template.md, agent-os/schemas/assignment-state.schema.json, agent-os/schemas/capability-registry.schema.json, agent-os/schemas/decision-register.schema.json, agent-os/schemas/dependency-map.schema.json, agent-os/schemas/knowledge-graph.schema.json, agent-os/schemas/milestones.schema.json, agent-os/schemas/provider-tiers.schema.json, agent-os/schemas/risk-register.schema.json, agent-os/schemas/system-state.schema.json, agent-os/schemas/worker-status.schema.json, agent-os/state/milestones.json, agent-os/triggers/archive/.gitkeep, CHANGELOG.md, CODE_OF_CONDUCT.md, docs/04-research/karpathy-knowledge-layer-plan.md, docs/audits/agent-template-readiness-audit.md, docs/audits/current-ai-agent-workflow-research.md, docs/backlog/template-improvement-backlog.md, docs/strategy/repo-positioning-review.md, docs/verification/release-readiness-checklist.md, examples/sample-handoff.md, examples/sample-multi-worker-walkthrough.md, examples/sample-project-goal.md, examples/sample-reassignment-record.md, examples/sample-status-report.md, prompt-library/goal-intake-to-tasks.md, prompt-library/hybrid-primary-worker-start.md, prompt-library/multi-worker-start.md, prompt-library/reassignment-continuation.md, prompt-library/reviewer-worker-start.md, prompt-library/solo-worker-start.md, prompt-library/status-report-request.md, prompt-library/support-worker-start.md, prompt-library/template-publish-check.md, prompt-library/verification-worker-start.md, scripts/agentctl.mjs, scripts/audit-agent-os.mjs, scripts/build-knowledge-graph.mjs, scripts/check-definition-of-done.mjs, scripts/check-scope.mjs, scripts/claim-task.mjs, scripts/distill-handoffs.mjs, scripts/enrich-task.mjs, scripts/generate-assignment-report.mjs, scripts/generate-decision-register.mjs, scripts/generate-status-report.mjs, scripts/init.mjs, scripts/lint-markdown.mjs, scripts/list-capabilities.mjs, scripts/list-modes.mjs, scripts/list-tasks.mjs, scripts/list-workers.mjs, scripts/move-task.mjs, scripts/setup-worktree.mjs, scripts/validate-assignments.mjs, scripts/validate-decisions.mjs, scripts/validate-handoff.mjs, scripts/validate-json.mjs, scripts/validate-knowledge-graph.mjs, scripts/validate-links.mjs, scripts/validate-locks.mjs, scripts/validate-mcp.mjs, scripts/validate-placeholders.mjs, scripts/validate-provider-tiers.mjs, scripts/validate-secrets.mjs, scripts/validate-startup-consistency.mjs, scripts/validate-state-consistency.mjs, scripts/validate-task.mjs, scripts/validate-template-readiness.mjs, STATUS.md

## How to Refresh

```bash
npm run graph:build
npm run validate:graph
```

