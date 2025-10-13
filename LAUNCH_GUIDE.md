# 🚀 Quick Launch Guide

## One-Command Launch

```powershell
.\scripts\launch-system.ps1
```

This script will:
- ✅ Find available ports automatically
- ✅ Start PostgreSQL and Redis (Docker)
- ✅ Run database migrations
- ✅ Start backend server
- ✅ Start frontend server
- ✅ Open browser automatically

---

## What Ports Are Used?

The system needs these ports:

| Service    | Default Port | Purpose                |
|------------|--------------|------------------------|
| Frontend   | 3000         | React web application  |
| Backend    | 8000         | FastAPI REST API       |
| PostgreSQL | 5432         | Database               |
| Redis      | 6379         | Cache & message broker |

**Note**: If default ports are busy, the launcher will automatically use the next available port (e.g., 8001, 3001, etc.)

---

## Manual Launch (If Needed)

### Step 1: Start Docker Services

```powershell
# PostgreSQL
docker run -d --name migration-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=migration_forecast -p 5432:5432 postgis/postgis:15-3.3

# Redis
docker run -d --name migration-redis -p 6379:6379 redis:7-alpine
```

### Step 2: Start Backend (Terminal 1)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8001
```

### Step 3: Start Frontend (Terminal 2)

```powershell
cd frontend
npm run dev -- --port 3001
```

---

## Check What's Running

```powershell
# Check all ports
netstat -ano | findstr "LISTENING" | findstr ":8000 :3000 :5432 :6379"

# Check Docker containers
docker ps

# Check backend health
curl http://localhost:8000/health

# Or use the test script
.\scripts\test-system.ps1
```

---

## Stop Everything

### Stop Servers
Press `Ctrl+C` in each terminal window

### Stop Docker Containers
```powershell
docker stop migration-postgres migration-redis
```

### Kill Processes on Specific Ports
```powershell
# Find process on port 8000
netstat -ano | findstr :8000
# Kill it (replace <PID> with actual process ID)
taskkill /PID <PID> /F

# Find process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

## Troubleshooting

### "Port already in use"
The launcher script automatically finds available ports. If you see this error, something else is using many consecutive ports. Try:
```powershell
# Stop all Docker containers
docker stop $(docker ps -aq)

# Kill processes on default ports
netstat -ano | findstr ":8000 :3000"
# Then kill those PIDs
```

### "Docker daemon not running"
1. Open Docker Desktop
2. Wait for it to fully start
3. Run the launcher again

### "Cannot connect to database"
```powershell
# Check PostgreSQL is running
docker ps | findstr postgres

# If not, start it
docker start migration-postgres

# Or recreate it
docker rm migration-postgres
docker run -d --name migration-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=migration_forecast -p 5432:5432 postgis/postgis:15-3.3
```

### "Module not found" (Backend)
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Module not found" (Frontend)
```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## URLs After Launch

Once everything is running:

- **Frontend**: http://localhost:3000 (or next available port)
- **Backend API**: http://localhost:8000 (or next available port)
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

The launcher will tell you the exact ports being used.

---

## Quick Commands

```powershell
# Launch everything
.\scripts\launch-system.ps1

# Test system health
.\scripts\test-system.ps1

# View backend logs
# (Check the PowerShell window that opened)

# View frontend logs
# (Check the other PowerShell window that opened)

# Restart just backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Restart just frontend
cd frontend
npm run dev
```

---

## First Time Setup

If you haven't run setup yet:

```powershell
.\scripts\setup-local.ps1
```

This installs all dependencies and creates configuration files.

---

## Next Steps After Launch

1. ✅ Open http://localhost:3000 in browser
2. ✅ Explore the dashboard
3. ✅ Check API docs at http://localhost:8000/docs
4. ✅ Run health check: `.\scripts\test-system.ps1`
5. ✅ Add sample data (see QUICK_START.md)

---

**Happy coding! 🚀**
