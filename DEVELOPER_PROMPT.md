Developer Implementation Prompt
You are the lead developer tasked with fully building the Migration Forecasting System using the documentation and scaffolding already present in this repository. Follow the plan below precisely. Ask for clarification only if a spec is missing or contradictory.

## Context & Goal

- Build an end-to-end migration forecasting platform:
  - Backend API (FastAPI) with DB (PostgreSQL + PostGIS), Celery workers, Redis
  - Data integration pipelines for 15+ free data sources
  - ML models for spatiotemporal predictions, explainability, and serving
  - Frontend (React + TypeScript) with interactive map, charts, and report builder
  - Render-first deployment without Docker for production; Docker optional for local dev

## Source of Truth (Read Before You Build)

Review these files first, and keep them open during development:
- `README.md` — entry point, quick start, project structure
- `PROJECT_PLAN.md` — phases, sprints, governance
- `PHASE_1_PLAN.md` … `PHASE_5_PLAN.md` — detailed sprint plans and acceptance criteria
- `DEVELOPMENT_READINESS.md` — missing files and priorities, readiness checklists
- `ARCHITECTURE.md` — system design, tech stack, data flows
- `IMPLEMENTATION_GUIDE.md` — step-by-step build instructions across phases
- `DATA_SOURCES.md` — APIs, rate limits, example calls, update frequencies
- `UI_DESIGN.md` — user stories, journeys, design system, wireframes, accessibility
- `DEPLOYMENT_RENDER.md` — Render deployment guide (Docker-free)
- `render.yaml` — Render services blueprint
- `CONTRIBUTING.md` — code style, PR process
- `AGENTS.md` — how to collaborate with the AI assistant on this repo

## Guardrails & Non-Negotiables

- Do not commit secrets. Use environment variables documented in `DEPLOYMENT_RENDER.md`.
- Keep changes atomic and traceable to sprint tasks in `PHASE_*_PLAN.md`.
- Write tests and docs for every substantive change.
- Maintain accessibility (WCAG 2.1 AA) and performance budgets per `UI_DESIGN.md`.
- Render-first deployment; Docker is optional for local dev only.

## Branching, Commits, and PRs

- Branch strategy: `main` (protected), `develop`, `feature/<ticket>`
- Conventional commits (e.g., `feat: add health endpoint`)
- PRs require green CI (lint + tests), 1+ reviewer, and updated docs
- Use the PR template in `AGENTS.md`

## Phase-by-Phase Execution Plan

Implement in order, sprint-by-sprint, using acceptance criteria and demo scripts in each `PHASE_*_PLAN.md`.

- Phase 1 (Sprints 1–3): Backend Core
  - Scaffolding, health/readiness/metrics, logging
  - SQLAlchemy + Alembic setup; base models (users, regions, audit)
  - Celery worker scaffold; CI smoke tests and coverage thresholds
  - References: `PHASE_1_PLAN.md`, `IMPLEMENTATION_GUIDE.md`, `ARCHITECTURE.md`, `DEVELOPMENT_READINESS.md`

- Phase 2 (Sprints 4–6): Data Integration
  - Connectors: UNHCR, World Bank → then ACLED, NASA POWER
  - ETL orchestration with Celery schedules; validation (Pandera/GE)
  - Provenance tracking; curated fact/dim tables; indexes/partitioning
  - References: `PHASE_2_PLAN.md`, `DATA_SOURCES.md`, `ARCHITECTURE.md`

- Phase 3 (Sprints 7–9): ML Models
  - Feature datasets, leakage guards, splits; baselines (classical + LSTM)
  - Serving endpoints: `/predictions`, `/explain`; SHAP and intervals
  - Metrics exposure; artifacts persisted and versioned
  - References: `PHASE_3_PLAN.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_GUIDE.md`

- Phase 4 (Sprints 10–12): Frontend
  - App shell, routing, theme/tokens; map with layers/time slider/hover
  - Charts (time series, bar, heatmap), Data Sources UI, Report Builder MVP
  - Accessibility, performance optimizations
  - References: `PHASE_4_PLAN.md`, `UI_DESIGN.md`

- Phase 5 (Sprints 13–14): Deployment & Advanced
  - Render production infra and monitoring; alerts and runbooks
  - Explainability Hub modal; Insights Panel; scheduled reports
  - Performance tuning to hit P95 < 500ms for key APIs
  - References: `PHASE_5_PLAN.md`, `DEPLOYMENT_RENDER.md`, `render.yaml`

## Immediate Setup Tasks (Day 0)

- Ensure the scaffolding files exist and update as needed:
  - Root: `.gitignore`, `.editorconfig`, `.env.example`, `LICENSE`, `CONTRIBUTING.md`
  - Backend: `backend/requirements.txt`, `backend/.env.example`
  - Frontend: `frontend/package.json`, `frontend/.env.example`
  - Scripts: `scripts/init.sql`
- Prepare Render services (do not deploy failing builds):
  - Managed Postgres (create and enable PostGIS after initial connect)
  - Managed Redis
  - Services from `render.yaml`: `backend-api`, `celery-worker`, `celery-beat` (or Cron), `frontend` (static site)
  - Set env vars: `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `LOG_LEVEL`, `VITE_API_URL`
  - Keep Auto-Deploy off for `backend-api`/`worker` until minimal skeleton compiles

## Sprint 1 Implementation Targets (Minimal, No Business Logic)

- Backend skeleton:
  - `backend/app/main.py` with `/health` responding 200
  - `backend/app/core/config.py` (env-driven settings)
  - `backend/app/core/logging.py` (JSON logging)
  - Prometheus instrumentation scaffold
- CI & Quality:
  - `pytest.ini`, basic test calling `/health`
  - GitHub Actions `test.yml` (lint + unit test)
- Acceptance Tests:
  - `/health` returns 200; logs in JSON; CI green

## Environment & Commands (Examples)

- Python venv (local)
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Frontend (local)
```bash
cd frontend
npm install
npm run dev
```

- Alembic (once models exist)
```bash
cd backend
alembic upgrade head
```

## Data Integration Requirements

- Build connectors strictly per `DATA_SOURCES.md`:
  - Respect rate limits; implement backoff and caching (Redis)
  - Incremental/delta syncs; pagination handling
  - Staging → curated layers; Pandera/GE validations with artifacts saved
  - Provenance: `data_ingest_runs` with source, params, counts, checksum
  - Spatial joins/aggregations using PostGIS

## ML Pipeline Requirements

- Leakage-safe splits; temporal CV
- Baselines: Linear/RandomForest/XGBoost + LSTM; save artifacts and configs
- Serving endpoints with confidence intervals; SHAP explainability
- Monitoring: request counts, latency, model version labels at `/metrics`

## Frontend Requirements

- Implement per `UI_DESIGN.md`:
  - Design tokens, typography, spacing, color palettes
  - Interactive map (layers: heatmap/flows/points/predictions, time slider, hover tooltips, presets)
  - Charts (time series with brush/zoom, regional bars, risk heatmap)
  - Data Source Management (status cards, logs modal, sync actions)
  - Report Builder MVP (drag-and-drop widgets; export to PDF/HTML)
- Accessibility: keyboard nav, ARIA labels, color contrast; provide data tables for charts

## Deployment on Render

- Use `DEPLOYMENT_RENDER.md` and `render.yaml`
- After skeleton compiles and health endpoint is live:
  - Enable Auto-Deploy for `backend-api` and `celery-worker`
  - Run migrations via Render shell/job: `alembic upgrade head`
  - Configure CORS to allow frontend origin
  - Validate health checks and env var wiring
- Post-Deployment:
  - Add Grafana/Prometheus dashboards
  - Create alerting rules (error rate, DB pool, ETL failures)

## Testing & Quality

- Minimum coverage: 80% for touched backend code
- Add integration tests for critical endpoints and ETL flows
- Frontend unit and E2E (Playwright) in Phase 5
- Performance: target P95 < 500ms for prediction/explain APIs

## Documentation Updates

- Update docs whenever behavior changes:
  - `README.md`, `PHASE_*_PLAN.md`, `IMPLEMENTATION_GUIDE.md`
  - Add API examples to `DATA_SOURCES.md` if updated
  - Keep `DEPLOYMENT_RENDER.md` accurate with any service/env changes

## Definition of Done (Per Sprint)

- Tasks implemented and linked to `PHASE_*_PLAN.md`
- Tests and docs updated
- CI green on PR with reviewer approval
- Demo script executed (in phase plan) and recorded in PR notes

## Risks & Mitigation

- API rate limits: caching + scheduling
- Data gaps/latency: validations + provenance logs
- Compute constraints: start small, iterate
- Geospatial complexity: rely on PostGIS; test queries with EXPLAIN ANALYZE

## Handover & Communication

- Track progress in GitHub Issues/Projects
- Daily updates in Slack channel
- Use PR template from `AGENTS.md` for every PR

If a specification is unclear, reference the corresponding `PHASE_*_PLAN.md` and escalate promptly with a proposed resolution for approval.
