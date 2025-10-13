# Render Deployment Guide (Docker-Free)

Last Updated: 2025-10-13

This guide explains how to deploy the Migration Forecasting System to Render without Docker. It uses Render-managed PostgreSQL and Redis, a Python Web Service (FastAPI), a Worker (Celery), a Cron Job for schedules, and a Static Site for the frontend.

---

## Architecture on Render

```
GitHub Repo → Render (Auto-deploy on main)

[Static Site: Frontend]
  ↳ Build: npm ci && npm run build
  ↳ Publish: frontend/dist
  ↳ Env: VITE_API_URL=https://<backend-service>.onrender.com

[Web Service: Backend API (FastAPI)]
  ↳ Env: Python 3.11
  ↳ Build: pip install -r backend/requirements.txt (rootDir=backend)
  ↳ Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ↳ Health Check: /health
  ↳ Env Vars: DATABASE_URL, REDIS_URL, SECRET_KEY, LOG_LEVEL

[Worker: Celery]
  ↳ Env: Python 3.11
  ↳ Build: pip install -r backend/requirements.txt (rootDir=backend)
  ↳ Start: celery -A app.workers.celery_app worker --loglevel=info
  ↳ Env Vars: DATABASE_URL, REDIS_URL, SECRET_KEY, LOG_LEVEL

[Cron Job: Schedules]
  ↳ Env: Python 3.11
  ↳ Build: pip install -r backend/requirements.txt (rootDir=backend)
  ↳ Start: python -m app.workers.run_scheduled_jobs
  ↳ Schedule: 0 2 * * * (example: daily at 02:00 UTC)

[Managed PostgreSQL]   [Managed Redis]
```

---

## Prerequisites
- Render account connected to your GitHub repository
- Repository at the project root (backend at `backend/`, frontend at `frontend/`)
- Confirm `backend/requirements.txt` and `frontend/package.json` exist

---

## Step-by-Step Setup

### 1) Create a Managed PostgreSQL Database
- Render Dashboard → New → PostgreSQL
- Plan: Free (for testing) or Starter
- After creation, note:
  - Internal Connection URL (use for `DATABASE_URL`)
  - External Connection URL (optional for external access)
- Create extension after first deploy (one-time):
  - Connect (psql or DataGrip) → `CREATE EXTENSION IF NOT EXISTS postgis;`

### 2) Create a Managed Redis Instance
- Render Dashboard → New → Redis
- Plan: Free (for testing) or Starter
- Note the Internal Redis URL (use for `REDIS_URL`)

### 3) Backend Web Service (FastAPI)
- Render Dashboard → New → Web Service
- Name: `backend-api`
- Environment: `Python` (3.11)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/health`
- Environment Variables:
  - `DATABASE_URL` = <Postgres Internal URL>
  - `REDIS_URL` = <Redis Internal URL>
  - `SECRET_KEY` = <secure random string>
  - `LOG_LEVEL` = `INFO`
- Auto Deploy: Yes (on push to main)

Run Migrations post-deploy:
- Create a Render Shell or use a temporary job to run `alembic upgrade head` once models/migrations exist.

### 4) Celery Worker Service
- Render Dashboard → New → Worker
- Environment: `Python` (3.11)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `celery -A app.workers.celery_app worker --loglevel=info`
- Environment Variables: same as Web Service

### 5) Scheduled Jobs (Cron)
- Render Dashboard → New → Cron Job
- Environment: `Python` (3.11)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python -m app.workers.run_scheduled_jobs`
- Schedule: choose (e.g., `0 2 * * *`)
- Env Vars: same as Web Service

Alternatively, if you prefer Celery Beat:
- Create another Worker with Start Command: `celery -A app.workers.celery_app beat --loglevel=info`
- Note: Celery Beat requires persistent schedule (e.g., in DB/Redis) to survive container restarts.

### 6) Frontend Static Site
- Render Dashboard → New → Static Site
- Name: `frontend`
- Root Directory: `frontend`
- Build Command: `npm ci && npm run build`
- Publish Directory: `dist`
- Environment Variables:
  - `VITE_API_URL` = `https://<backend-api>.onrender.com`
- Redirects/Rewrites: add `/*  /index.html  200` for SPA routing

---

## Render Blueprint (Optional)
A starting-point `render.yaml` is provided (see `render.yaml`). Validate keys against Render's latest docs and update names before use.

---

## Environment Variables Summary
- Backend/Worker/Cron:
  - `DATABASE_URL` (Render Postgres Internal URL)
  - `REDIS_URL` (Render Redis Internal URL)
  - `SECRET_KEY` (random, long)
  - `LOG_LEVEL` (INFO/DEBUG)
- Frontend:
  - `VITE_API_URL` (public URL of backend web service)

---

## Observability & Limits
- Logs: Available per service in Render
- Health Checks: Use `/health` for backend
- Persistence: Write data to Postgres; container filesystems are ephemeral
- Rate Limits: Use caching in Redis and retry/backoff in ETL connectors

---

## Post-Deployment Tasks
- Run DB migrations (Alembic)
- Seed reference data (regions, admin boundaries) when ready
- Create admin/API users if needed
- Test `/health` and basic endpoints
- Confirm CORS settings (allow frontend origin)

---

## Local Development (No Docker)
- Backend: Python venv, `pip install -r backend/requirements.txt`, `uvicorn app.main:app --reload`
- Frontend: `npm install`, `npm run dev`
- Postgres/Redis: Use local installs or Render External URLs (not recommended for heavy dev)

---

## Troubleshooting
- 500 errors on startup → check `DATABASE_URL`, `REDIS_URL`, and migrations
- Health check failing → ensure app binds to `$PORT` and `/health` returns 200
- CORS issues → configure allowed origins in FastAPI settings
- Cron job not running → verify schedule syntax and logs
