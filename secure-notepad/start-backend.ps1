# Secure Notepad - Startup Script for Windows PowerShell

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host " Secure Notepad Application Startup" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Change to project root
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Node.js is not installed!" -ForegroundColor Red
    Write-Host "Please install from https://nodejs.org/" -ForegroundColor Red
    exit 1
}
Write-Host "Node.js $nodeVersion: OK" -ForegroundColor Green

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed!" -ForegroundColor Red
    Write-Host "Please install from https://www.python.org/" -ForegroundColor Red
    exit 1
}
Write-Host "Python: OK" -ForegroundColor Green

# Backend Setup
Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Yellow
Push-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "Installing Python packages..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --quiet

Write-Host "Starting Flask server on port 5000..." -ForegroundColor Green
# Keep terminal open and start Flask
Write-Host ""
Write-Host "Backend is starting..." -ForegroundColor Cyan
Write-Host "Flask will run at http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
python app.py
