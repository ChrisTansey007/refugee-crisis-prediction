# Local Setup Script for Migration Forecasting System
# Run with: .\scripts\setup-local.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migration Forecasting System - Local Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from project root
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Function to check if command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

$missingPrereqs = @()

if (-not (Test-Command "python")) {
    $missingPrereqs += "Python 3.11+"
}

if (-not (Test-Command "node")) {
    $missingPrereqs += "Node.js 18+"
}

if (-not (Test-Command "docker")) {
    Write-Host "Warning: Docker not found. You'll need to install PostgreSQL and Redis manually." -ForegroundColor Yellow
}

if ($missingPrereqs.Count -gt 0) {
    Write-Host "Missing prerequisites:" -ForegroundColor Red
    $missingPrereqs | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    Write-Host ""
    Write-Host "Please install missing software and try again." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Prerequisites check passed" -ForegroundColor Green
Write-Host ""

# Setup Backend
Write-Host "Setting up Backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "Installing Python dependencies (this may take a few minutes)..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Cyan
    @"
# App Settings
ENV=development
LOG_LEVEL=INFO
SECRET_KEY=dev-secret-key-change-in-production

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/migration_forecast

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=dev-jwt-secret-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# MLflow
MLFLOW_TRACKING_URI=file:./mlruns
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ Created .env file" -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Set-Location ..
Write-Host "✓ Backend setup complete" -ForegroundColor Green
Write-Host ""

# Setup Frontend
Write-Host "Setting up Frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing Node dependencies (this may take a few minutes)..." -ForegroundColor Cyan
    npm install --silent
} else {
    Write-Host "✓ Node modules already installed" -ForegroundColor Green
}

Set-Location ..
Write-Host "✓ Frontend setup complete" -ForegroundColor Green
Write-Host ""

# Docker services
Write-Host "Setting up Docker services..." -ForegroundColor Yellow

if (Test-Command "docker") {
    # Check if containers already exist
    $postgresExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "migration-postgres"
    $redisExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "migration-redis"
    
    # PostgreSQL
    if ($postgresExists) {
        Write-Host "PostgreSQL container already exists. Starting..." -ForegroundColor Cyan
        docker start migration-postgres | Out-Null
    } else {
        Write-Host "Creating PostgreSQL container..." -ForegroundColor Cyan
        docker run -d `
            --name migration-postgres `
            -e POSTGRES_PASSWORD=postgres `
            -e POSTGRES_DB=migration_forecast `
            -p 5432:5432 `
            postgis/postgis:15-3.3 | Out-Null
        Start-Sleep -Seconds 5
    }
    
    # Redis
    if ($redisExists) {
        Write-Host "Redis container already exists. Starting..." -ForegroundColor Cyan
        docker start migration-redis | Out-Null
    } else {
        Write-Host "Creating Redis container..." -ForegroundColor Cyan
        docker run -d `
            --name migration-redis `
            -p 6379:6379 `
            redis:7-alpine | Out-Null
    }
    
    Write-Host "✓ Docker services started" -ForegroundColor Green
    Write-Host ""
    
    # Wait for PostgreSQL to be ready
    Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Cyan
    Start-Sleep -Seconds 3
    
    # Run migrations
    Write-Host "Running database migrations..." -ForegroundColor Yellow
    Set-Location backend
    & .\venv\Scripts\Activate.ps1
    alembic upgrade head
    Set-Location ..
    Write-Host "✓ Database migrations complete" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "Skipping Docker setup (Docker not available)" -ForegroundColor Yellow
    Write-Host "Please start PostgreSQL and Redis manually" -ForegroundColor Yellow
    Write-Host ""
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start Backend (in backend directory):" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start Frontend (in frontend directory, new terminal):" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Access the application:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor Gray
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "For detailed instructions, see LOCAL_SETUP.md" -ForegroundColor Cyan
Write-Host ""
