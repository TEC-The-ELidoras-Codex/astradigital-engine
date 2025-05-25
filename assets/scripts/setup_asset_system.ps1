#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Sets up the TEC asset system

.DESCRIPTION
    This master script runs all the necessary setup steps for the TEC asset system:
    1. Creates the directory structure
    2. Sets up the tools and dependencies
    3. Migrates existing assets (optional)

.NOTES
    File Name      : setup_asset_system.ps1
    Author         : TEC Development Team
#>

param (
    [switch]$SkipDirSetup,
    [switch]$SkipTools,
    [switch]$SkipMigration,
    [switch]$Force,
    [switch]$Verbose
)

# Determine base directories
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Path $scriptPath -Parent
$assetsDir = Split-Path -Path $scriptDir -Parent

# Function to run a script and check if it succeeded
function Invoke-Setup {
    param (
        [string]$ScriptPath,
        [string]$Description,
        [string[]]$Arguments
    )
    
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Starting: $Description" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    $scriptCommand = $ScriptPath
    if ($Arguments) {
        $scriptCommand += " " + ($Arguments -join " ")
    }
    
    Write-Host "Running: $scriptCommand" -ForegroundColor DarkCyan
    
    try {
        & $ScriptPath @Arguments
        
        if ($LASTEXITCODE -ne 0) {
            throw "Script exited with code $LASTEXITCODE"
        }
        
        Write-Host "Completed: $Description" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error in $Description : $_" -ForegroundColor Red
        
        $continue = Read-Host "Continue setup despite this error? (y/n)"
        if ($continue -ne "y") {
            return $false
        }
        
        return $true
    }
}

Write-Host "TEC Asset System Setup" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host "Assets Directory: $assetsDir" -ForegroundColor Cyan

# Create directory structure
if (-not $SkipDirSetup) {
    $createStructureScript = Join-Path -Path $scriptDir -ChildPath "create_asset_structure.ps1"
    $args = @()
    
    if ($Force) {
        $args += "-Force"
    }
    
    if ($Verbose) {
        $args += "-Verbose"
    }
    
    if (-not (Invoke-Setup -ScriptPath $createStructureScript -Description "Directory Structure Setup" -Arguments $args)) {
        Write-Host "Setup failed at directory structure creation." -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "Skipping directory structure setup." -ForegroundColor Yellow
}

# Set up tools
if (-not $SkipTools) {
    $setupToolsScript = Join-Path -Path $scriptDir -ChildPath "setup_asset_tools.ps1"
    $args = @()
    
    if ($Force) {
        $args += "-Force"
    }
    
    if (-not (Invoke-Setup -ScriptPath $setupToolsScript -Description "Asset Tools Setup" -Arguments $args)) {
        Write-Host "Setup failed at tools installation." -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "Skipping tools setup." -ForegroundColor Yellow
}

# Migrate assets
if (-not $SkipMigration) {
    $sourceDumpDir = Join-Path -Path $assetsDir -ChildPath "Data-dump&Deploy"
    
    if (Test-Path -Path $sourceDumpDir) {
        $migrateAssetsScript = Join-Path -Path $scriptDir -ChildPath "migrate_assets.ps1"
        $args = @("-SourceDir", "Data-dump&Deploy", "-DestRoot", $assetsDir)
        
        if ($Force) {
            $args += "-Force"
        }
        
        if ($Verbose) {
            $args += "-Verbose"
        }
        
        if (-not (Invoke-Setup -ScriptPath $migrateAssetsScript -Description "Asset Migration" -Arguments $args)) {
            Write-Host "Setup failed at asset migration." -ForegroundColor Red
            exit 1
        }
    }
    else {
        Write-Host "No Data-dump&Deploy directory found. Skipping migration." -ForegroundColor Yellow
    }
}
else {
    Write-Host "Skipping asset migration." -ForegroundColor Yellow
}

Write-Host "`n=============================================" -ForegroundColor Green
Write-Host "TEC Asset System Setup Completed Successfully!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "  1. Activate the environment: & '$scriptDir\activate_env.ps1'" -ForegroundColor Yellow
Write-Host "  2. Optimize images: python $scriptDir\optimize.py --help" -ForegroundColor Yellow
Write-Host "  3. Prepare WordPress assets: python $scriptDir\prepare_wp_assets.py --help" -ForegroundColor Yellow
Write-Host "  4. Prepare HuggingFace assets: python $scriptDir\prepare_hf_assets.py --help" -ForegroundColor Yellow
Write-Host "  5. Prepare Docker assets: python $scriptDir\prepare_docker_assets.py --help" -ForegroundColor Yellow
