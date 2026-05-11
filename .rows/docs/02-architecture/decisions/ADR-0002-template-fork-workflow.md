# ADR-0002: Template Fork Workflow

## Status

Accepted

## Date

2026-05-06

## Context

The ROWS system must be reusable across projects. Each project needs its own instance of the agent operating system, with project-specific goals, tasks, and state. We need a distribution and initialization model that is simple, familiar to developers, and preserves the ability to receive upstream improvements.

## Decision

We will distribute ROWS as a GitHub template repository. Users fork the template, rename it for their project, fill in `PROJECT_GOAL.md`, and begin. The template contains all scaffolding (rules, task lifecycle folders, checklists, scripts) but no project-specific code.

Key design choices:
- **GitHub template (not a package or CLI tool):** The repo IS the system. Forking is the installation.
- **`PROJECT_GOAL.md` as intake:** A single guided form bootstraps the entire project.
- **Upstream merge capability:** Forks can pull improvements from the template while maintaining project-specific state.
- **No Copilot:** GitHub Copilot is intentionally excluded. The system uses its own defined worker set.

## Consequences

**Positive:**
- Zero installation — fork and go.
- Familiar GitHub workflow for developers.
- Upstream improvements can be merged into project forks.
- Clear separation between system (template) and project (fork).

**Negative:**
- Template updates require manual merge into existing forks.
- GitHub dependency — the template lives on GitHub.
- Fork visibility settings may expose project plans if set to public.

## Alternatives Considered

1. **npm package / CLI tool:** Rejected because the repo IS the system; a package would separate rules from state.
2. **Docker image:** Rejected because it adds operational complexity without benefit for a file-based system.
3. **Submodule:** Rejected because submodules complicate workflows and confuse AI workers.

## Related Files

- [`TEMPLATE_USAGE.md`](../../../TEMPLATE_USAGE.md) — Fork workflow instructions
- [`PROJECT_GOAL.md`](../../../PROJECT_GOAL.md) — Project intake form
