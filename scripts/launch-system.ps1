# Launch Migration Forecasting System
# Automatically finds available ports and launches services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migration Forecasting System Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if port is available
function Test-Port {
    param($Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue -InformationLevel Quiet
    return -not $connection
}

# Function to find available port
function Find-AvailablePort {
    param($PreferredPort, $Range = 10)
    
    if (Test-Port -Port $PreferredPort) {
        return $PreferredPort
    }
    
    for ($i = 1; $i -le $Range; $i++) {
        $testPort = $PreferredPort + $i
        if (Test-Port -Port $testPort) {
            return $testPort
        }
    }
    
    return $null
}

Write-Host "Checking available ports..." -ForegroundColor Yellow

# Find available ports
$backendPort = Find-AvailablePort -PreferredPort 8000
$frontendPort = Find-AvailablePort -PreferredPort 3000
$postgresPort = Find-AvailablePort -PreferredPort 5432
$redisPort = Find-AvailablePort -PreferredPort 6379

if (-not $backendPort) {
    Write-Host "Error: Could not find available port for backend (tried 8000-8010)" -ForegroundColor Red
    exit 1
}

if (-not $frontendPort) {
    Write-Host "Error: Could not find available port for frontend (tried 3000-3010)" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Backend will use port: $backendPort" -ForegroundColor Green
Write-Host "✓ Frontend will use port: $frontendPort" -ForegroundColor Green
Write-Host ""

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    $dockerAvailable = $true
    Write-Host "✓ Docker is available" -ForegroundColor Green
} catch {
    $dockerAvailable = $false
    Write-Host "✗ Docker is not available" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop and try again" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Start PostgreSQL if not running
Write-Host "Starting PostgreSQL..." -ForegroundColor Yellow
$postgresRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "migration-postgres"

if ($postgresRunning) {
    Write-Host "✓ PostgreSQL is already running" -ForegroundColor Green
} else {
    # Check if container exists but stopped
    $postgresExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "migration-postgres"
    
    if ($postgresExists) {
        Write-Host "Starting existing PostgreSQL container..." -ForegroundColor Cyan
        docker start migration-postgres | Out-Null
    } else {
        Write-Host "Creating new PostgreSQL container..." -ForegroundColor Cyan
        docker run -d `
            --name migration-postgres `
            -e POSTGRES_PASSWORD=postgres `
            -e POSTGRES_DB=migration_forecast `
            -p "${postgresPort}:5432" `
            postgis/postgis:15-3.3 | Out-Null
    }
    Start-Sleep -Seconds 5
    Write-Host "✓ PostgreSQL started" -ForegroundColor Green
}
Write-Host ""

# Start Redis if not running
Write-Host "Starting Redis..." -ForegroundColor Yellow
$redisRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "migration-redis"

if ($redisRunning) {
    Write-Host "✓ Redis is already running" -ForegroundColor Green
} else {
    # Check if container exists but stopped
    $redisExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "migration-redis"
    
    if ($redisExists) {
        Write-Host "Starting existing Redis container..." -ForegroundColor Cyan
        docker start migration-redis | Out-Null
    } else {
        Write-Host "Creating new Redis container..." -ForegroundColor Cyan
        docker run -d `
            --name migration-redis `
            -p "${redisPort}:6379" `
            redis:7-alpine | Out-Null
    }
    Write-Host "✓ Redis started" -ForegroundColor Green
}
Write-Host ""

# Update .env file with correct ports
Write-Host "Updating configuration..." -ForegroundColor Yellow
$envContent = @"
# App Settings
ENV=development
LOG_LEVEL=INFO
SECRET_KEY=dev-secret-key-change-in-production

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:$postgresPort/migration_forecast

# Redis
REDIS_URL=redis://localhost:$redisPort/0

# JWT
JWT_SECRET_KEY=dev-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MLflow
MLFLOW_TRACKING_URI=file:./mlruns
"@

$envContent | Out-File -FilePath "backend\.env" -Encoding UTF8 -Force
Write-Host "✓ Configuration updated" -ForegroundColor Green
Write-Host ""

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
Set-Location backend
& .\venv\Scripts\Activate.ps1
try {
    alembic upgrade head 2>&1 | Out-Null
    Write-Host "✓ Migrations complete" -ForegroundColor Green
} catch {
    Write-Host "Note: Migrations may have already been run" -ForegroundColor Yellow
}
Set-Location ..
Write-Host ""

# Start Backend
Write-Host "Starting Backend server..." -ForegroundColor Yellow
$backendScript = @"
Set-Location backend
.\venv\Scripts\Activate.ps1
Write-Host ''
Write-Host '========================================' -ForegroundColor Cyan
Write-Host 'Backend Server Running' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ''
Write-Host 'API:      http://localhost:$backendPort' -ForegroundColor White
Write-Host 'Docs:     http://localhost:$backendPort/docs' -ForegroundColor White
Write-Host 'Health:   http://localhost:$backendPort/health' -ForegroundColor White
Write-Host ''
Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow
Write-Host ''
uvicorn app.main:app --reload --host 0.0.0.0 --port $backendPort
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript
Write-Host "✓ Backend server starting on port $backendPort" -ForegroundColor Green
Start-Sleep -Seconds 3
Write-Host ""

# Update frontend proxy configuration
Write-Host "Updating frontend configuration..." -ForegroundColor Yellow
$viteConfig = @"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: $frontendPort,
    proxy: {
      '/api': {
        target: 'http://localhost:$backendPort',
        changeOrigin: true,
      },
    },
  },
})
"@

$viteConfig | Out-File -FilePath "frontend\vite.config.js" -Encoding UTF8 -Force
Write-Host "✓ Frontend configuration updated" -ForegroundColor Green
Write-Host ""

# Start Frontend
Write-Host "Starting Frontend server..." -ForegroundColor Yellow
$frontendScript = @"
Set-Location frontend
Write-Host ''
Write-Host '========================================' -ForegroundColor Cyan
Write-Host 'Frontend Server Running' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ''
Write-Host 'App:      http://localhost:$frontendPort' -ForegroundColor White
Write-Host ''
Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow
Write-Host ''
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript
Write-Host "✓ Frontend server starting on port $frontendPort" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "System Launched Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Frontend:    http://localhost:$frontendPort" -ForegroundColor White
Write-Host "  Backend API: http://localhost:$backendPort" -ForegroundColor White
Write-Host "  API Docs:    http://localhost:$backendPort/docs" -ForegroundColor White
Write-Host ""
Write-Host "Two PowerShell windows have been opened." -ForegroundColor Cyan
Write-Host "Close them or press Ctrl+C to stop the servers." -ForegroundColor Cyan
Write-Host ""
Write-Host "Waiting 5 seconds before opening browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Open browser
Start-Process "http://localhost:$frontendPort"

Write-Host "✓ Browser opened" -ForegroundColor Green
Write-Host ""
