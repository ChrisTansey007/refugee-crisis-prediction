# AGENTS Playbook — AI Coding Assistant for Migration Forecasting System

Last Updated: 2025-10-13
Primary Audience: Project Maintainers, Junior Developers, AI Assistants

---

## Purpose
Define how an AI coding assistant should operate on this repository to maximize quality, speed, and safety. This playbook provides roles, workflows, prompt templates, guardrails, and references for each phase of the project.

---

## Operating Principles

- **Single Source of Truth**: Treat repository docs as authoritative. Always reference:
  - `README.md`, `PROJECT_PLAN.md`, `PHASE_*_PLAN.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_GUIDE.md`, `DATA_SOURCES.md`, `DEPLOYMENT_RENDER.md`, `UI_DESIGN.md`.
- **Read Before Write**: Open and read target files or directories before proposing changes. Cite exact paths (e.g., `backend/app/main.py`).
- **No Surprise Actions**: Propose changes first. Do not auto-run commands or generate app code unless explicitly requested.
- **Small, Atomic Changes**: Prefer scoped, incremental patches with clear rationale and acceptance criteria.
- **Traceability**: Link changes to user stories, sprint tasks, or phase plans.
- **Security**: Never commit secrets or tokens. Use environment variables. Follow `DEPLOYMENT_RENDER.md` guidance.
- **Render-First**: Prefer Render deployment over Docker for production. Keep Docker only for optional local dev.
- **Windows-Friendly**: When proposing commands, avoid `cd` inlined. Specify working directory and use PowerShell-compatible syntax.
- **Accessibility & UX**: Adhere to `UI_DESIGN.md` accessibility and performance standards for frontend work.

---

## Agent Roles

- **Coding Assistant (Primary)**
  - Plans tasks, reads docs, drafts patches, writes tests, updates docs.
  - Keeps `todo_list` (project tracker) up to date and marks completion.
- **Data Source Research Agent**
  - Validates API endpoints, rate limits, and examples against `DATA_SOURCES.md`.
  - Proposes schema updates and ETL cadence.
- **ETL Orchestration Agent**
  - Designs `extract → transform → load` flows and validation rules.
  - Ensures provenance tracking and materialized views per `PHASE_2_PLAN.md`.
- **ML Engineer Agent**
  - Creates feature pipelines, trains baselines, saves artifacts, exposes serving endpoints per `PHASE_3_PLAN.md`.
- **Frontend/UI Agent**
  - Implements map/charts per `UI_DESIGN.md`, ensures accessibility and performance.
- **DevOps/Render Agent**
  - Maintains `render.yaml`, environment variables, and deployment docs (`DEPLOYMENT_RENDER.md`).
- **Reporting Agent**
  - Implements report builder widgets, export flows, and schedules.

---

## Phase & Sprint Workflows (Agent Checklists)

### Phase 1 (Backend Core) — `PHASE_1_PLAN.md`
1. Read: `DEVELOPMENT_READINESS.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_GUIDE.md`.
2. Propose scaffolding (no business logic) and confirm with maintainer.
3. Add health/readiness/metrics endpoints plan and tests scaffolding.
4. Set up Alembic and base models plan (users, regions, audit).
5. Ensure logging, config, CI smoke tests are documented.

### Phase 2 (Data Integration) — `PHASE_2_PLAN.md`
1. Confirm source specs in `DATA_SOURCES.md`.
2. Implement UNHCR/World Bank connectors; then ACLED/NASA POWER.
3. Add Pandera/Great Expectations validations; provenance tables.
4. Aggregate to curated facts/dims; add partitions and indexes.

### Phase 3 (ML Models) — `PHASE_3_PLAN.md`
1. Build reproducible datasets with temporal splits and leakage guards.
2. Train classical baselines + LSTM; log metrics, save artifacts.
3. Expose `/predictions` and `/explain` endpoints (FastAPI).
4. Add Prometheus metrics; set up basic drift monitoring workflow.

### Phase 4 (Frontend) — `PHASE_4_PLAN.md`
1. Create app shell with theme/tokens; route stubs per `UI_DESIGN.md`.
2. Build interactive map (layers, hover, time slider) and charts.
3. Implement Data Sources and Report Builder UIs.
4. Ensure accessibility (WCAG 2.1 AA) and performance budgets.

### Phase 5 (Deployment & Advanced) — `PHASE_5_PLAN.md`
1. Use Render blueprint (`render.yaml`) and `DEPLOYMENT_RENDER.md`.
2. Add monitoring dashboards and alerts; finalize runbooks.
3. Optimize DB queries and caching; finalize Explainability Hub & Insights.

---

## Guardrails & Safety

- **No Secrets**: Never hardcode credentials. Use `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY` in service settings.
- **Approval Before Execution**: Propose commands; require maintainer approval before running anything destructive.
- **Patch Hygiene**: Keep patches minimal with surrounding context, referencing exact lines.
- **Licensing/Attribution**: Ensure data/API usage complies with provider terms.
- **Token Limits**: Split large edits across multiple patches/files if needed.

---

## Prompt Templates (Copy/Paste)

- **Read & Locate**
  - "Open `path/to/file` and show entire contents."  
  - "Search for `functionName` across `backend/`."

- **Propose Patch**
  - "I will add X to `file`. Summary: <one-line>. Acceptance: <criteria>."  
  - Then produce a minimal patch with 3 lines of context around the change.

- **Write Tests**
  - "Generate unit tests for `module.Function`, focusing on edge cases: <list>."

- **Migration**
  - "Create Alembic migration for new table `table_name` with indexes on `<cols>`."  
  - Include rollback and data backfill notes.

- **Render Deployment Update**
  - "Update `render.yaml` to add env var `<KEY>`, and add notes in `DEPLOYMENT_RENDER.md` under Post-Deployment."

- **ETL Validation**
  - "Add Pandera schema for `stg_source_table` with constraints `<list>`."

- **Frontend UI**
  - "Design hover tooltip content for map layer `<layer>` consistent with `UI_DESIGN.md` and add aria-labels."

---

## PR Description Template

```
Title: feat(scope): short summary

Context
- Links: user story / phase plan / issue
- Files/areas touched

Changes
- [ ] Change 1
- [ ] Change 2

Testing
- Steps to verify
- Screenshots (if UI)

Risks
- Potential side effects
- Rollback plan

Docs
- [ ] Updated relevant .md files
```

---

## Metrics (Assistant Performance)
- **Cycle Time**: time from task creation to merged PR
- **Review Iterations**: number of review cycles per PR
- **Test Coverage**: % coverage for touched files
- **Defect Rate**: issues created per merged PR
- **Docs Freshness**: docs updated per substantive change

---

## Render Deployment (Assistant Checklist)
1. Confirm services and env vars with maintainer.
2. Update `render.yaml` with service changes.
3. Update `DEPLOYMENT_RENDER.md` with step-by-step instructions.
4. Validate health checks and CORS.
5. Never paste secrets into repo or logs.

---

## Security & Compliance
- Use managed secrets; never commit `.env` (template only: `.env.example`).
- Keep PII out of logs and reports; aggregate/anonymize where needed.
- Respect data provider licenses and rate limits; cache responses.

---

## Useful References
- `README.md` — project entry point
- `PROJECT_PLAN.md` — phases, sprints, governance
- `PHASE_1_PLAN.md` … `PHASE_5_PLAN.md` — detailed execution plans
- `DEVELOPMENT_READINESS.md` — environment and missing files
- `ARCHITECTURE.md` — system design & stacks
- `DATA_SOURCES.md` — APIs, rate limits, examples
- `IMPLEMENTATION_GUIDE.md` — step-by-step build guide
- `UI_DESIGN.md` — UX specs, accessibility, performance
- `DEPLOYMENT_RENDER.md` — Render deployment guide
- `render.yaml` — Render blueprint

---

## When to Escalate to a Human
- Requirements ambiguity or conflicting specs
- Security-sensitive changes (auth, secrets, RBAC)
- Cost-impacting infra decisions
- Persistent failures after two fix attempts

---

This playbook equips AI assistants and junior developers to collaborate effectively, safely, and consistently across all phases of the Migration Forecasting System.
