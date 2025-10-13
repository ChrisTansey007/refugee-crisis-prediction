# 🚀 START HERE - Launch the Migration Forecasting System

**Quick guide to get the system running locally**

---

## Step 1: Start Docker Desktop

1. Open **Docker Desktop** application
2. Wait for it to fully start (whale icon in system tray should be steady)
3. Verify it's running:
   ```powershell
   docker ps
   ```

---

## Step 2: Start Database Services

```powershell
# Start PostgreSQL
docker run -d `
  --name migration-postgres `
  -e POSTGRES_PASSWORD=postgres `
  -e POSTGRES_DB=migration_forecast `
  -p 5432:5432 `
  postgis/postgis:15-3.3

# Start Redis
docker run -d `
  --name migration-redis `
  -p 6379:6379 `
  redis:7-alpine

# Wait 5 seconds for PostgreSQL to initialize
Start-Sleep -Seconds 5
```

---

## Step 3: Run Database Migrations

```powershell
cd backend
.\venv\Scripts\Activate.ps1
alembic upgrade head
cd ..
```

---

## Step 4: Start Backend Server

**Terminal 1** - Keep this open:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 5: Start Frontend Server

**Terminal 2** - Open a new terminal:
```powershell
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## Step 6: Open Your Browser

Navigate to: **http://localhost:3000**

You should see the Migration Forecasting System dashboard!

---

## Step 7: Verify Everything Works

Run the health check script:
```powershell
.\scripts\test-system.ps1
```

All checks should pass ✓

---

## 🎉 You're Ready!

### Explore the Application:

1. **Dashboard** (`/`) - System overview with stats
2. **Map View** (`/map`) - Interactive world map
3. **Data Sources** (`/data-sources`) - Manage connectors
4. **Models** (`/models`) - ML model dashboard
5. **Predictions** (`/predictions`) - View forecasts
6. **Reports** (`/reports`) - Generate reports

### Test the API:

Open **http://localhost:8000/docs** for interactive API documentation

---

## 📝 Optional: Add Sample Data

### Populate Dimension Tables

```powershell
# Add date dimension (2015-2025)
curl -X POST http://localhost:8000/api/v1/etl/dim-date `
  -H "Content-Type: application/json" `
  -d '{"start_year": 2015, "end_year": 2025}'

# Add country dimension
curl -X POST http://localhost:8000/api/v1/etl/dim-country `
  -H "Content-Type: application/json" `
  -d '{
    "countries": [
      {"iso3_code": "AFG", "name": "Afghanistan", "region": "Asia", "subregion": "South Asia"},
      {"iso3_code": "SYR", "name": "Syria", "region": "Middle East", "subregion": "Western Asia"},
      {"iso3_code": "SOM", "name": "Somalia", "region": "Africa", "subregion": "East Africa"}
    ]
  }'
```

### Check ETL Status

```powershell
curl http://localhost:8000/api/v1/etl/status
```

---

## 🛑 Stopping the System

1. Press `Ctrl+C` in both terminal windows (backend and frontend)
2. Stop Docker containers:
   ```powershell
   docker stop migration-postgres migration-redis
   ```

---

## 🔄 Restarting Later

If Docker containers already exist:

```powershell
# Start existing containers
docker start migration-postgres migration-redis

# Terminal 1: Backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## ❓ Troubleshooting

### Docker containers won't start
```powershell
# Remove old containers
docker rm -f migration-postgres migration-redis

# Start fresh (run Step 2 again)
```

### Port already in use
```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
```

### Backend won't start
```powershell
# Check PostgreSQL is running
docker ps | findstr postgres

# Check .env file exists
ls backend\.env

# Reinstall dependencies
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend won't start
```powershell
# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

---

## 📚 More Information

- **QUICK_START.md** - Detailed quick start
- **LOCAL_SETUP.md** - Complete setup guide
- **PROJECT_COMPLETE.md** - Full project documentation
- **README.md** - Project overview

---

**Happy exploring! 🚀**
