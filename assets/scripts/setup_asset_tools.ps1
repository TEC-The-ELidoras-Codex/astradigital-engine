#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Sets up the Python tools needed for the TEC asset system

.DESCRIPTION
    This script installs the necessary Python packages for the TEC asset
    optimization and processing tools. It creates a virtual environment
    and installs all required dependencies.

.NOTES
    File Name      : setup_asset_tools.ps1
    Author         : TEC Development Team
#>

param (
    [string]$VenvName = "tec-asset-env",
    [switch]$Force
)

# Determine the scripts directory
$scriptsDir = $PSScriptRoot
$assetsDir = Split-Path -Path $scriptsDir -Parent

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Found $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Python not found. Please install Python 3.8 or newer." -ForegroundColor Red
    exit 1
}

# Check if pip is installed
try {
    $pipVersion = python -m pip --version
    Write-Host "Found pip: $pipVersion" -ForegroundColor Green
}
catch {
    Write-Host "pip not found. Please install pip." -ForegroundColor Red
    exit 1
}

# Set up virtual environment
$venvPath = Join-Path -Path $assetsDir -ChildPath $VenvName

if (Test-Path -Path $venvPath) {
    if ($Force) {
        Write-Host "Removing existing virtual environment: $venvPath" -ForegroundColor Yellow
        Remove-Item -Path $venvPath -Recurse -Force
    }
    else {
        Write-Host "Virtual environment already exists: $venvPath" -ForegroundColor Yellow
        $continue = Read-Host "Do you want to recreate it? (y/n)"
        
        if ($continue -eq "y") {
            Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
            Remove-Item -Path $venvPath -Recurse -Force
        }
        else {
            Write-Host "Using existing virtual environment." -ForegroundColor Cyan
            
            # Activate the virtual environment
            if ($IsWindows) {
                $activateScript = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"
            }
            else {
                $activateScript = Join-Path -Path $venvPath -ChildPath "bin/activate.ps1"
            }
            
            if (Test-Path -Path $activateScript) {
                Write-Host "Activating virtual environment..." -ForegroundColor Cyan
                & $activateScript
            }
            else {
                Write-Host "Error: Virtual environment activation script not found." -ForegroundColor Red
                exit 1
            }
            
            # Update packages
            Write-Host "Updating packages in virtual environment..." -ForegroundColor Cyan
            python -m pip install --upgrade pip
            
            # Create requirements file
            $reqFile = Join-Path -Path $assetsDir -ChildPath "scripts\requirements.txt"
            if (-not (Test-Path -Path $reqFile)) {
                Write-Host "Creating requirements file..." -ForegroundColor Cyan
                @"
Pillow>=9.0.0
webp>=0.1.0
tqdm>=4.64.0
"@ | Out-File -FilePath $reqFile -Encoding utf8
            }
            
            # Install requirements
            Write-Host "Installing required packages..." -ForegroundColor Cyan
            python -m pip install -r $reqFile
            
            Write-Host "Virtual environment is ready!" -ForegroundColor Green
            exit 0
        }
    }
}

# Create virtual environment
Write-Host "Creating virtual environment: $venvPath" -ForegroundColor Cyan
python -m venv $venvPath

if (-not $?) {
    Write-Host "Failed to create virtual environment." -ForegroundColor Red
    exit 1
}

# Activate the virtual environment
if ($IsWindows) {
    $activateScript = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"
}
else {
    $activateScript = Join-Path -Path $venvPath -ChildPath "bin/activate.ps1"
}

if (Test-Path -Path $activateScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & $activateScript
}
else {
    Write-Host "Error: Virtual environment activation script not found." -ForegroundColor Red
    exit 1
}

# Update pip
Write-Host "Updating pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Create requirements file
$reqFile = Join-Path -Path $assetsDir -ChildPath "scripts\requirements.txt"
Write-Host "Creating requirements file..." -ForegroundColor Cyan
@"
Pillow>=9.0.0
webp>=0.1.0
tqdm>=4.64.0
"@ | Out-File -FilePath $reqFile -Encoding utf8

# Install requirements
Write-Host "Installing required packages..." -ForegroundColor Cyan
python -m pip install -r $reqFile

if (-not $?) {
    Write-Host "Failed to install required packages." -ForegroundColor Red
    exit 1
}

Write-Host "`nTEC asset tools setup completed successfully!" -ForegroundColor Green
Write-Host "`nTo activate this environment in the future, run:" -ForegroundColor Cyan
Write-Host "  & '$activateScript'"

# Create activation shortcut script
$activateShortcut = Join-Path -Path $assetsDir -ChildPath "scripts\activate_env.ps1"
Write-Host "`nCreating activation shortcut script: $activateShortcut" -ForegroundColor Cyan

@"
# TEC Asset Tools Environment Activator
# This script activates the virtual environment for TEC asset tools

& "$activateScript"
Write-Host "TEC asset tools environment activated!" -ForegroundColor Green
Write-Host "Available commands:"
Write-Host "  python $assetsDir\scripts\optimize.py --help" -ForegroundColor Cyan
Write-Host "  python $assetsDir\scripts\prepare_wp_assets.py --help" -ForegroundColor Cyan
Write-Host "  python $assetsDir\scripts\prepare_hf_assets.py --help" -ForegroundColor Cyan
"@ | Out-File -FilePath $activateShortcut -Encoding utf8

Write-Host "`nYou can now run:" -ForegroundColor Yellow
Write-Host "  & '$activateShortcut'" -ForegroundColor Yellow
