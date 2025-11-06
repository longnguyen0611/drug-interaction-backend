# Quick Start Script for Windows PowerShell
# Run this to setup and start the backend locally

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Drug Interaction Backend API - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Create venv if not exists
if (-Not (Test-Path "venv")) {
    Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[2/5] Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate venv
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check data files
Write-Host "[5/5] Checking data files..." -ForegroundColor Yellow
$csvExists = Test-Path "data\drug_tfidf_reduced_128d.csv"
$gsExists = Test-Path "data\graphsage.pt"
$epExists = Test-Path "data\edge_predictor.pt"

if ($csvExists) {
    Write-Host "✅ drug_tfidf_reduced_128d.csv" -ForegroundColor Green
} else {
    Write-Host "❌ drug_tfidf_reduced_128d.csv not found" -ForegroundColor Red
}

if ($gsExists) {
    Write-Host "✅ graphsage.pt" -ForegroundColor Green
} else {
    Write-Host "⚠️  graphsage.pt not found (will use fallback)" -ForegroundColor Yellow
}

if ($epExists) {
    Write-Host "✅ edge_predictor.pt" -ForegroundColor Green
} else {
    Write-Host "⚠️  edge_predictor.pt not found (will use fallback)" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the server, run:" -ForegroundColor Yellow
Write-Host "  uvicorn server:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
Write-Host ""
Write-Host "Or simply:" -ForegroundColor Yellow
Write-Host "  python server.py" -ForegroundColor White
Write-Host ""
Write-Host "API will be available at:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000" -ForegroundColor White
Write-Host "  http://localhost:8000/docs (Swagger UI)" -ForegroundColor White
Write-Host ""
