# Phase 1 Plan — Backend Core Infrastructure (Sprints 1–3)

Last Updated: 2025-10-13
Owner: Tech Lead
Cross-Refs: ARCHITECTURE.md, IMPLEMENTATION_GUIDE.md, DEPLOYMENT.md, DEVELOPMENT_READINESS.md

## Required Reference Docs

- [README.md](./README.md)
- [PROJECT_PLAN.md](./PROJECT_PLAN.md)
- [DEVELOPMENT_READINESS.md](./DEVELOPMENT_READINESS.md)
- [AGENTS.md](./AGENTS.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [DATA_SOURCES.md](./DATA_SOURCES.md)
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
- [UI_DESIGN.md](./UI_DESIGN.md)
- [DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)
- [render.yaml](./render.yaml)
- [DEPLOYMENT.md](./DEPLOYMENT.md) (optional)

---

## Phase Goals
- Establish repo structure, quality gates, and development workflows
- Stand up Dockerized Postgres + PostGIS + Redis and working FastAPI skeleton
- Implement core configuration, logging, health checks, and CI smoke tests

## Non-Goals
- No ML model training (Phase 3)
- No full frontend (Phase 4)

---

## Sprint 1 (Week 1–2): Project Foundation & API Skeleton

### Objectives
- Create scaffolding, environment templates, and base Docker setup
- Spin up a minimal FastAPI app with health endpoint plan
- Add linting, formatting, and testing baselines

### Tasks (Step-by-Step for Junior Dev)
- Repo & Config
  - Create root `.gitignore` (Python, Node, Docker), `LICENSE` (MIT), `CONTRIBUTING.md`
  - Add `.editorconfig` for consistent whitespace
  - Create `.env.example` (root) with placeholders; copy to backend/frontend later
- Docker (dev focus)
  - Draft `docker-compose.yml` with `db` (PostGIS), `redis`, `api` service placeholders
  - Verify volumes and named networks
  - Add `scripts/init.sql` placeholder for DB init
- Backend Skeleton (no business logic yet)
  - Create `backend/app/` directories per `IMPLEMENTATION_GUIDE.md`
  - Plan the following files: `app/main.py` (FastAPI), `app/core/config.py` (settings), `app/core/logging.py` (JSON logs)
  - Prepare health endpoints plan: `/health`, `/readiness`, `/metrics` (exposed later)
- Quality Gates
  - Add `backend/requirements.txt` outline (FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2, asyncpg)
  - Add tooling files: `pyproject.toml` (black/isort/ruff), `pytest.ini` (min config)
  - Set up GitHub Actions `test.yml` (lint + unit test placeholders)

### Acceptance Criteria
- `docker-compose up` runs DB + Redis containers successfully
- Minimal API container starts and responds on `/health` (200 OK) plan finalized
- Lint and tests run successfully in CI (placeholder tests allowed)
- `.env.example` exists and is referenced in docs

### Deliverables
- `docker-compose.yml` (dev)
- Backend folder structure and placeholder files
- CI workflow with lint/test jobs
- Documentation updates in `DEVELOPMENT_READINESS.md`

### Risks & Mitigation
- Docker networking issues → use explicit networks and healthcheck commands
- Dependency conflicts → pin versions in `requirements.txt`

---

## Sprint 2 (Week 3–4): Database & Auth Foundations

### Objectives
- Install and configure SQLAlchemy + Alembic for migrations
- Create base schema: `users`, `regions`, `audit_logs`
- Prepare JWT auth plan and config, but defer full endpoints until Phase 1 end

### Tasks
- Database
  - Configure DSN: `DATABASE_URL` via env
  - Initialize Alembic, create migration scripts folder
  - Create base models plan: `User`, `Region`, `AuditLog`
  - Add indexing strategy (by `region_code`, `created_at`)
- Auth & Security (scaffold)
  - Define JWT settings in `config.py` (keys, expiry, algorithm)
  - Outline endpoints: `/auth/login`, `/auth/refresh`, `/auth/me` (implement minimal in Sprint 3)
  - Add password hashing policy (argon2/bcrypt)
- Observability (start)
  - Introduce JSON logging format and correlation IDs
  - Plan Prometheus metrics via `prometheus_fastapi_instrumentator`

### Acceptance Criteria
- Alembic migrations apply cleanly to Postgres
- Tables visible and accessible; `regions` preloaded via `scripts/init.sql` (admin areas only)
- Configurable JWT settings and key rotation strategy documented
- Logging emits structured JSON to stdout

### Deliverables
- Alembic config + first migration
- Model definitions plan with constraints and indexes
- Logging config and guidelines

### Risks & Mitigation
- PostGIS extensions not available → ensure image tag includes PostGIS and run `CREATE EXTENSION postgis;`
- JWT key management → note Secret Manager plan (see `DEPLOYMENT.md`)

---

## Sprint 3 (Week 5–6): Services, Workers, Health & CI Hardening

### Objectives
- Add Celery worker scaffolding with Redis broker
- Implement basic background jobs (placeholders) for data refresh cadence
- Finalize health/readiness endpoints and metrics exposure
- Harden CI (test matrix, coverage) and error handling

### Tasks
- Services
  - Celery app plan in `app/workers/celery_app.py` with retry/backoff policy
  - Placeholder periodic tasks: `refresh_all_data`, `recalculate_materialized_views`
  - Graceful shutdown hooks for API and worker
- Health & Metrics
  - `/health`: DB + Redis check, return 200 only if OK
  - `/readiness`: include migrations-applied check
  - `/metrics`: auto-exposed Prometheus metrics
- CI & Testing
  - Add coverage thresholds (e.g., 80% for touched code)
  - Add service containers in CI (Postgres, Redis) for integration tests
  - Add smoke tests for `/health` and DB connection

### Acceptance Criteria
- API and worker containers start and stop cleanly with Docker Compose
- Health endpoints validate dependencies correctly
- CI runs integration tests with service containers
- Background jobs can be triggered manually and log activity

### Deliverables
- Celery scaffolding and scheduled tasks plan
- Health/readiness endpoints specification
- CI with integration tests and coverage report

### Demo Script
- Show `docker-compose up` starting all services
- Hit `/health` to show green status
- Trigger a dummy Celery task and show logs

---

## Roles & Estimates
- Backend dev: 70–80% of effort (primary)
- DevOps: 20–30% (compose/CI/logging)
- Designer/UX: consult on API responses for UI needs

---

## Exit Criteria (Phase Gate)
- API skeleton, DB, Redis operational via Docker Compose
- Migrations framework in place with base tables
- Health, readiness, and metrics endpoints defined and testable
- CI pipeline green with lint + tests + coverage

---

## References
- `ARCHITECTURE.md` → Backend structure and services
- `IMPLEMENTATION_GUIDE.md` → Phase 1 steps & commands
- `DEPLOYMENT.md` → Docker + logging + metrics patterns
- `DEVELOPMENT_READINESS.md` → Missing files and priorities
