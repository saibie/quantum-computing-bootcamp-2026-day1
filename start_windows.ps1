# start_windows.ps1
$ErrorActionPreference = "Stop"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Quantum Computing Bootcamp Day 1 - Environment Starter" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot

# 1. Register default uv paths if existing
$uvSearchPaths = @(
    "$env:USERPROFILE\.local\bin",
    "$env:USERPROFILE\.cargo\bin",
    "$env:LOCALAPPDATA\bin"
)

foreach ($dir in $uvSearchPaths) {
    if (Test-Path "$dir\uv.exe") {
        if ($env:Path -notlike "*$dir*") {
            $env:Path = "$dir;$env:Path"
        }
    }
}

# 2. Install uv if not found
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[*] uv package manager not found. Installing uv..." -ForegroundColor Yellow
    try {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
        $env:Path = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:LOCALAPPDATA\bin;$env:Path"
    } catch {
        Write-Host "[ERROR] Failed to install uv: $_" -ForegroundColor Red
        Read-Host "Press Enter to exit..."
        exit 1
    }
}

# 3. Final verification of uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] uv is not detected in PATH. Please restart terminal." -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

$uvVer = (uv --version)
Write-Host "[OK] uv detected: $uvVer" -ForegroundColor Green
Write-Host ""

# 4. Sync Python 3.12 and dependencies
Write-Host "[*] Synchronizing Python 3.12, NumPy, Qiskit, Jupyter Lab..." -ForegroundColor Cyan
try {
    uv sync
    if ($LASTEXITCODE -ne 0) {
        throw "uv sync failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Host "[ERROR] uv sync failed. Please check internet connection." -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

# 5. Launch Jupyter Lab
Write-Host ""
Write-Host "[*] Launching Jupyter Lab in your default browser..." -ForegroundColor Green
Write-Host "[*] Please keep this window open during the lab session." -ForegroundColor Yellow
Write-Host ""

uv run jupyter lab --notebook-dir=hands_on
