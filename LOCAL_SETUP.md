# Local Setup Guide

Complete guide to run the Migration Forecasting System locally.

---

## Prerequisites

### Required Software
- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **PostgreSQL 15+** - Database with PostGIS extension
- **Redis 7+** - Cache and message broker
- **Git** - Version control

### Windows-Specific
- PowerShell 5.1+ (comes with Windows 10/11)
- Windows Terminal (recommended)

---

## Quick Start (Automated)

### Option 1: Using Setup Script

```powershell
# Run the automated setup script
.\scripts\setup-local.ps1
```

This will:
1. Check prerequisites
2. Set up Python virtual environment
3. Install backend dependencies
4. Set up database and run migrations
5. Install frontend dependencies
6. Create environment files

### Option 2: Manual Setup (Step-by-Step)

Follow the sections below for detailed manual setup.

---

## Backend Setup

### 1. Create Virtual Environment

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment

Create `backend/.env` file:

```env
# App Settings
ENV=development
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/migration_forecast

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MLflow
MLFLOW_TRACKING_URI=file:./mlruns
```

### 4. Start PostgreSQL

**Using Docker** (Recommended):
```powershell
docker run -d `
  --name migration-postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=migration_forecast `
  -p 5432:5432 `
  postgis/postgis:15-3.3
```

**Or install PostgreSQL locally** and create database:
```sql
CREATE DATABASE migration_forecast;
CREATE EXTENSION postgis;
```

### 5. Start Redis

**Using Docker**:
```powershell
docker run -d `
  --name migration-redis `
  -p 6379:6379 `
  redis:7-alpine
```

**Or install Redis locally** and start service.

### 6. Run Database Migrations

```powershell
cd backend
alembic upgrade head
```

### 7. Start Backend Server

```powershell
# In backend directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

API docs at: **http://localhost:8000/docs**

### 8. Start Celery Worker (Optional)

In a new terminal:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
celery -A app.workers.celery_app worker --loglevel=info --pool=solo
```

---

## Frontend Setup

### 1. Install Dependencies

```powershell
cd frontend
npm install
```

### 2. Start Development Server

```powershell
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## Verification Steps

### 1. Check Backend Health

```powershell
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"0.4.0"}

curl http://localhost:8000/readiness
# Should return: {"status":"ready"}
```

### 2. Check Database Connection

```powershell
curl http://localhost:8000/api/v1/etl/status
# Should return dimension and fact table counts
```

### 3. Access Frontend

Open browser to **http://localhost:3000**

You should see the Dashboard with navigation sidebar.

### 4. Check API Documentation

Open **http://localhost:8000/docs** for interactive API documentation.

---

## Common Issues & Solutions

### Issue: Port Already in Use

**Backend (8000)**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process
taskkill /PID <process_id> /F
```

**Frontend (3000)**:
```powershell
# Find process using port 3000
netstat -ano | findstr :3000
# Kill process
taskkill /PID <process_id> /F
```

### Issue: PostgreSQL Connection Failed

1. Check PostgreSQL is running:
   ```powershell
   docker ps | findstr postgres
   ```

2. Verify connection string in `.env`

3. Test connection:
   ```powershell
   psql -h localhost -U postgres -d migration_forecast
   ```

### Issue: Redis Connection Failed

1. Check Redis is running:
   ```powershell
   docker ps | findstr redis
   ```

2. Test connection:
   ```powershell
   redis-cli ping
   # Should return: PONG
   ```

### Issue: Python Module Not Found

```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Node Modules Error

```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: Alembic Migration Failed

```powershell
# Check current version
alembic current

# Downgrade and upgrade
alembic downgrade -1
alembic upgrade head

# Or reset (CAUTION: drops all data)
alembic downgrade base
alembic upgrade head
```

---

## Testing the System

### 1. Populate Dimension Tables

```powershell
# Populate date dimension
curl -X POST http://localhost:8000/api/v1/etl/dim-date `
  -H "Content-Type: application/json" `
  -d '{"start_year": 2015, "end_year": 2025}'

# Populate country dimension
curl -X POST http://localhost:8000/api/v1/etl/dim-country `
  -H "Content-Type: application/json" `
  -d '{
    "countries": [
      {"iso3_code": "AFG", "name": "Afghanistan", "region": "Asia"},
      {"iso3_code": "SYR", "name": "Syria", "region": "Middle East"},
      {"iso3_code": "SOM", "name": "Somalia", "region": "Africa"}
    ]
  }'
```

### 2. Ingest Sample Data (Optional)

**Note**: Requires API keys for ACLED. UNHCR and World Bank are public.

```powershell
# UNHCR data
curl -X POST http://localhost:8000/api/v1/ingest/unhcr `
  -H "Content-Type: application/json" `
  -d '{"year": 2023, "country_codes": ["AFG"]}'

# World Bank data
curl -X POST http://localhost:8000/api/v1/ingest/worldbank `
  -H "Content-Type: application/json" `
  -d '{
    "country_codes": ["AFG"],
    "indicator_codes": ["NY.GDP.PCAP.CD"],
    "start_year": 2020,
    "end_year": 2023
  }'
```

### 3. Check ETL Status

```powershell
curl http://localhost:8000/api/v1/etl/status
```

### 4. View in Frontend

Navigate to **http://localhost:3000** and explore:
- Dashboard - See system stats
- Map View - Geographic visualization
- Data Sources - Check ingestion status
- Models - View ML models
- Predictions - See forecasts

---

## Development Workflow

### Backend Development

1. Make code changes
2. Server auto-reloads (uvicorn --reload)
3. Test endpoints at http://localhost:8000/docs
4. Check logs in terminal

### Frontend Development

1. Make code changes in `src/`
2. Vite hot-reloads automatically
3. View changes at http://localhost:3000
4. Check browser console for errors

### Database Changes

1. Modify models in `backend/app/models/`
2. Create migration:
   ```powershell
   alembic revision --autogenerate -m "description"
   ```
3. Review migration in `backend/alembic/versions/`
4. Apply migration:
   ```powershell
   alembic upgrade head
   ```

---

## Stopping Services

### Stop Backend
Press `Ctrl+C` in terminal running uvicorn

### Stop Frontend
Press `Ctrl+C` in terminal running npm dev

### Stop Celery Worker
Press `Ctrl+C` in terminal running celery

### Stop Docker Services
```powershell
docker stop migration-postgres migration-redis
docker rm migration-postgres migration-redis
```

---

## Clean Restart

To start fresh:

```powershell
# Stop all services
# Stop Docker containers
docker stop migration-postgres migration-redis
docker rm migration-postgres migration-redis

# Remove database volume (CAUTION: deletes all data)
docker volume rm migration_postgres_data

# Restart services
docker run -d --name migration-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=migration_forecast -p 5432:5432 postgis/postgis:15-3.3
docker run -d --name migration-redis -p 6379:6379 redis:7-alpine

# Run migrations
cd backend
alembic upgrade head

# Start backend
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev
```

---

## Next Steps

1. ✅ Verify all services are running
2. ✅ Populate dimension tables
3. ✅ Test API endpoints
4. ✅ Explore frontend interface
5. ✅ Ingest sample data (optional)
6. ✅ Train ML models (optional)

For production deployment, see `DEPLOYMENT_RENDER.md`.

---

## Support

- Check logs in terminal windows
- Review API docs at http://localhost:8000/docs
- See project documentation in repository root
- Check `TROUBLESHOOTING.md` for common issues
