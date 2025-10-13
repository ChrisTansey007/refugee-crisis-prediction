# System Test Script
# Run with: .\scripts\test-system.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migration Forecasting System - Health Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# Test Backend Health
Write-Host "Testing Backend Health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    if ($response.status -eq "healthy") {
        Write-Host "✓ Backend is healthy (v$($response.version))" -ForegroundColor Green
    } else {
        Write-Host "✗ Backend health check failed" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host "✗ Backend is not responding (is it running?)" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# Test Backend Readiness
Write-Host "Testing Backend Readiness..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/readiness" -Method Get -TimeoutSec 5
    if ($response.status -eq "ready") {
        Write-Host "✓ Backend is ready (database connected)" -ForegroundColor Green
    } else {
        Write-Host "✗ Backend is not ready: $($response.detail)" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host "✗ Backend readiness check failed" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# Test ETL Status
Write-Host "Testing ETL Status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/etl/status" -Method Get -TimeoutSec 5
    Write-Host "✓ ETL Status retrieved successfully" -ForegroundColor Green
    Write-Host "  Dimensions:" -ForegroundColor Cyan
    Write-Host "    Countries: $($response.dimensions.countries)" -ForegroundColor Gray
    Write-Host "    Dates: $($response.dimensions.dates)" -ForegroundColor Gray
    Write-Host "  Facts:" -ForegroundColor Cyan
    Write-Host "    Displacement: $($response.facts.displacement)" -ForegroundColor Gray
    Write-Host "    Economic: $($response.facts.economic)" -ForegroundColor Gray
    Write-Host "    Conflict: $($response.facts.conflict)" -ForegroundColor Gray
    Write-Host "    Climate: $($response.facts.climate)" -ForegroundColor Gray
} catch {
    Write-Host "✗ ETL status check failed" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# Test Frontend
Write-Host "Testing Frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -Method Get -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Frontend is accessible" -ForegroundColor Green
    } else {
        Write-Host "✗ Frontend returned status code: $($response.StatusCode)" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host "✗ Frontend is not responding (is it running?)" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# Test Docker Services
Write-Host "Testing Docker Services..." -ForegroundColor Yellow

$postgresRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "migration-postgres"
if ($postgresRunning) {
    Write-Host "✓ PostgreSQL container is running" -ForegroundColor Green
} else {
    Write-Host "✗ PostgreSQL container is not running" -ForegroundColor Red
    $allPassed = $false
}

$redisRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "migration-redis"
if ($redisRunning) {
    Write-Host "✓ Redis container is running" -ForegroundColor Green
} else {
    Write-Host "✗ Redis container is not running" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "All tests passed! ✓" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "System is ready to use:" -ForegroundColor White
    Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Cyan
    Write-Host "  Backend:   http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
} else {
    Write-Host "Some tests failed ✗" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  1. Backend server is running (uvicorn)" -ForegroundColor White
    Write-Host "  2. Frontend server is running (npm run dev)" -ForegroundColor White
    Write-Host "  3. Docker containers are running (docker ps)" -ForegroundColor White
    Write-Host "  4. Database migrations have been run (alembic upgrade head)" -ForegroundColor White
}
Write-Host ""
