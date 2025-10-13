# Start Development Servers
# Run with: .\scripts\start-dev.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Migration Forecasting System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker services are running
Write-Host "Checking Docker services..." -ForegroundColor Yellow

$postgresRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "migration-postgres"
$redisRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "migration-redis"

if (-not $postgresRunning) {
    Write-Host "Starting PostgreSQL..." -ForegroundColor Cyan
    docker start migration-postgres | Out-Null
    Start-Sleep -Seconds 3
}

if (-not $redisRunning) {
    Write-Host "Starting Redis..." -ForegroundColor Cyan
    docker start migration-redis | Out-Null
}

Write-Host "✓ Docker services running" -ForegroundColor Green
Write-Host ""

# Start Backend in new window
Write-Host "Starting Backend server..." -ForegroundColor Yellow
$backendScript = @"
Set-Location backend
.\venv\Scripts\Activate.ps1
Write-Host 'Backend server starting on http://localhost:8000' -ForegroundColor Green
Write-Host 'API docs available at http://localhost:8000/docs' -ForegroundColor Cyan
Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow
Write-Host ''
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend in new window
Write-Host "Starting Frontend server..." -ForegroundColor Yellow
$frontendScript = @"
Set-Location frontend
Write-Host 'Frontend server starting on http://localhost:3000' -ForegroundColor Green
Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow
Write-Host ''
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Development servers started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application:" -ForegroundColor Yellow
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Two PowerShell windows have been opened." -ForegroundColor Cyan
Write-Host "Close them or press Ctrl+C in each to stop the servers." -ForegroundColor Cyan
Write-Host ""
