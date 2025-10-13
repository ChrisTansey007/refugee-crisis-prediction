# Quick Start Guide

Get the Migration Forecasting System running locally in 5 minutes!

---

## Prerequisites

Install these first:
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)

---

## Option 1: Automated Setup (Recommended)

### Step 1: Run Setup Script

Open PowerShell in the project root and run:

```powershell
.\scripts\setup-local.ps1
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Start PostgreSQL and Redis in Docker
- ✅ Run database migrations
- ✅ Create configuration files

### Step 2: Start Development Servers

```powershell
.\scripts\start-dev.ps1
```

This opens two windows:
- **Backend** on http://localhost:8000
- **Frontend** on http://localhost:3000

### Step 3: Open Your Browser

Navigate to **http://localhost:3000**

You should see the Migration Forecasting System dashboard!

---

## Option 2: Manual Setup

### Backend

```powershell
# Terminal 1 - Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start Docker services
docker run -d --name migration-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=migration_forecast -p 5432:5432 postgis/postgis:15-3.3
docker run -d --name migration-redis -p 6379:6379 redis:7-alpine

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend

```powershell
# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

---

## Verify Installation

### Check Backend

```powershell
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"0.4.0"}
```

### Check Frontend

Open browser to **http://localhost:3000**

You should see:
- ✅ Dashboard with navigation sidebar
- ✅ System stats (may show 0 initially)
- ✅ Charts and visualizations

### Check API Docs

Open **http://localhost:8000/docs**

Interactive API documentation with all endpoints.

---

## Initial Data Setup (Optional)

### Populate Dimension Tables

```powershell
# Date dimension (2015-2025)
curl -X POST http://localhost:8000/api/v1/etl/dim-date `
  -H "Content-Type: application/json" `
  -d '{"start_year": 2015, "end_year": 2025}'

# Country dimension
curl -X POST http://localhost:8000/api/v1/etl/dim-country `
  -H "Content-Type: application/json" `
  -d '{
    "countries": [
      {"iso3_code": "AFG", "name": "Afghanistan", "region": "Asia", "subregion": "South Asia"},
      {"iso3_code": "SYR", "name": "Syria", "region": "Middle East", "subregion": "Western Asia"},
      {"iso3_code": "SOM", "name": "Somalia", "region": "Africa", "subregion": "East Africa"},
      {"iso3_code": "YEM", "name": "Yemen", "region": "Middle East", "subregion": "Western Asia"},
      {"iso3_code": "SSD", "name": "South Sudan", "region": "Africa", "subregion": "East Africa"}
    ]
  }'
```

### Test Data Ingestion

```powershell
# UNHCR data (public, no API key needed)
curl -X POST http://localhost:8000/api/v1/ingest/unhcr `
  -H "Content-Type: application/json" `
  -d '{"year": 2023, "country_codes": ["AFG"]}'

# World Bank data (public, no API key needed)
curl -X POST http://localhost:8000/api/v1/ingest/worldbank `
  -H "Content-Type: application/json" `
  -d '{
    "country_codes": ["AFG"],
    "indicator_codes": ["NY.GDP.PCAP.CD"],
    "start_year": 2020,
    "end_year": 2023
  }'
```

---

## Explore the Application

### Dashboard (`/`)
- System overview
- Data source statistics
- Health indicators

### Map View (`/map`)
- Interactive world map
- Displacement visualization
- Layer selection

### Data Sources (`/data-sources`)
- Manage data connectors
- View ingestion history
- Refresh data

### Models (`/models`)
- ML model management
- Performance metrics
- Model comparison

### Predictions (`/predictions`)
- Forecast visualizations
- Confidence intervals
- Contributing factors

### Reports (`/reports`)
- Generate reports
- Download exports

---

## Common Commands

### Start Services
```powershell
.\scripts\start-dev.ps1
```

### Stop Services
Press `Ctrl+C` in each terminal window

Or stop Docker containers:
```powershell
docker stop migration-postgres migration-redis
```

### View Logs
Check the terminal windows where services are running

### Reset Database
```powershell
cd backend
.\venv\Scripts\Activate.ps1
alembic downgrade base
alembic upgrade head
```

---

## Troubleshooting

### Port Already in Use

**Backend (8000)**:
```powershell
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**Frontend (3000)**:
```powershell
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
```

### Docker Not Starting

1. Ensure Docker Desktop is running
2. Check Docker status:
   ```powershell
   docker ps
   ```

### Module Not Found

**Backend**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Frontend**:
```powershell
cd frontend
rm -rf node_modules
npm install
```

---

## Next Steps

1. ✅ Explore the frontend interface
2. ✅ Test API endpoints at http://localhost:8000/docs
3. ✅ Ingest sample data
4. ✅ View data in dashboard
5. ✅ Check out the map visualization

For detailed documentation, see:
- `LOCAL_SETUP.md` - Complete setup guide
- `README.md` - Project overview
- `ARCHITECTURE.md` - System architecture
- `API_REFERENCE.md` - API documentation

---

## Support

Having issues? Check:
1. All prerequisites are installed
2. Docker Desktop is running
3. Ports 3000, 8000, 5432, 6379 are available
4. Virtual environment is activated (backend)
5. Dependencies are installed

For more help, see `LOCAL_SETUP.md` or `TROUBLESHOOTING.md`

---

**Enjoy exploring the Migration Forecasting System!** 🚀
