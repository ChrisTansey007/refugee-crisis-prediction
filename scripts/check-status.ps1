# Quick Status Check

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "System Status Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check ports
Write-Host "Checking ports..." -ForegroundColor Yellow
Write-Host ""

$ports = @{
    "PostgreSQL" = 5432
    "Redis" = 6379
    "Backend (8000)" = 8000
    "Backend (8001)" = 8001
    "Frontend (3000)" = 3000
    "Frontend (3001)" = 3001
}

$runningServices = @{}

foreach ($service in $ports.Keys) {
    $port = $ports[$service]
    $connection = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue -InformationLevel Quiet
    
    if ($connection) {
        Write-Host "✓ $service - Port $port is OPEN" -ForegroundColor Green
        $runningServices[$service] = $port
    } else {
        Write-Host "✗ $service - Port $port is closed" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($runningServices.Count -gt 0) {
    Write-Host "Running Services:" -ForegroundColor Green
    Write-Host ""
    
    foreach ($service in $runningServices.Keys) {
        $port = $runningServices[$service]
        
        if ($service -like "*Backend*") {
            Write-Host "  Backend API:  http://localhost:$port" -ForegroundColor White
            Write-Host "  API Docs:     http://localhost:$port/docs" -ForegroundColor White
        }
        elseif ($service -like "*Frontend*") {
            Write-Host "  Frontend:     http://localhost:$port" -ForegroundColor White
        }
    }
    
    Write-Host ""
    
    # Test backend health if running
    $backendPort = $null
    if ($runningServices.ContainsKey("Backend (8001)")) {
        $backendPort = 8001
    } elseif ($runningServices.ContainsKey("Backend (8000)")) {
        $backendPort = 8000
    }
    
    if ($backendPort) {
        Write-Host "Testing backend health..." -ForegroundColor Yellow
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:$backendPort/health" -Method Get -TimeoutSec 3
            if ($response.status -eq "healthy") {
                Write-Host "✓ Backend is healthy (v$($response.version))" -ForegroundColor Green
            }
        } catch {
            Write-Host "✗ Backend health check failed" -ForegroundColor Red
        }
    }
} else {
    Write-Host "No services are running" -ForegroundColor Red
    Write-Host ""
    Write-Host "To start the system, run:" -ForegroundColor Yellow
    Write-Host "  .\scripts\launch-system.ps1" -ForegroundColor White
}

Write-Host ""
