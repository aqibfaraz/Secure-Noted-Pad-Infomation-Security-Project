# Secure Notepad - Frontend Startup Script for Windows PowerShell

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host " Secure Notepad - Frontend Server" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Change to project root
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$projectRoot\frontend"

Write-Host "Installing npm packages..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "Starting Vite dev server on port 3000..." -ForegroundColor Green
Write-Host ""
Write-Host "Frontend will run at http://localhost:3000" -ForegroundColor Cyan
Write-Host "This browser window will open automatically." -ForegroundColor Cyan
Write-Host ""

npm run dev
