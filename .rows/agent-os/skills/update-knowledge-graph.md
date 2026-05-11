# Skill: Update Knowledge Graph

Use this skill whenever you change task templates, onboarding docs, skills, ADRs, blockers, or other files that affect how the repo references itself.

## Purpose

The knowledge graph is the shared index behind backlinks, repo-map generation, orphan detection, and task context enrichment. Keep it current whenever reference-bearing files change.

## Steps

1. Run the builder:

```bash
npm run graph:build
```

2. Review the generated artifacts:

- `agent-os/state/knowledge-graph.json`
- `docs/04-research/repo-map.md`
- `agent-os/state/dependency-map.json`

3. If orphan warnings increased unexpectedly, inspect whether:

- a new file is missing from onboarding or task references
- a generated file source is wrong
- an old file should be archived or ignored

4. Before finishing, validate:

```bash
npm run validate:graph
```

## When To Run

- After updating `BOOTSTRAP.md`, `AGENTS.md`, reading lists, install docs, or skills
- After changing task fields or dependency conventions
- After adding or changing ADRs, decision-register entries, or blockers
- Before shipping docs work that changes repo navigation
