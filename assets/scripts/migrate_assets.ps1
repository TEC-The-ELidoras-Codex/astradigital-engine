#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Migrates assets from old structure to the new TEC asset organization system

.DESCRIPTION
    This script helps migrate existing assets from the old structure (Data-dump&Deploy)
    to the new organized structure. It preserves original files while organizing them
    into the appropriate directories based on type and purpose.

.NOTES
    File Name      : migrate_assets.ps1
    Author         : TEC Development Team
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$SourceDir = "Data-dump&Deploy",

    [Parameter(Mandatory = $false)]
    [string]$DestRoot = "$PWD",

    [switch]$Force,
    [switch]$Verbose
)

# Ensure the destination directory exists
if (-not (Test-Path -Path $DestRoot)) {
    Write-Host "Destination directory does not exist: $DestRoot" -ForegroundColor Red
    exit 1
}

# Set up source path
$sourcePath = Join-Path -Path $PWD -ChildPath $SourceDir
if (-not (Test-Path -Path $sourcePath)) {
    Write-Host "Source directory does not exist: $sourcePath" -ForegroundColor Red
    exit 1
}

# Set up logging
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path -Path $DestRoot -ChildPath "migration_log_$timestamp.txt"

function Write-Log {
    param (
        [string]$Message,
        [string]$Color = "White"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $logFile -Append
    
    if ($Verbose) {
        Write-Host $Message -ForegroundColor $Color
    }
}

# Start logging
Write-Log "Starting TEC asset migration: $sourcePath -> $DestRoot" "Green"
Write-Log "Source: $sourcePath"
Write-Log "Destination: $DestRoot"

# Define mapping of old directories to new structure
$migrationMap = @{
    # Images
    "Image"                           = "source/images"
    "Image/Airth_Character_Concept_Alpha" = "source/images/characters"
    "Image/MACHINE_GODDESS_MOSTW"     = "source/images/characters"
    "Visuals/Branding"                = "source/images/branding"
    "Visuals/Graphics"                = "source/images/ui"
    "Visuals/Animations"              = "source/video/animations"
    "Visuals/Mindmaps"                = "source/documents/lore"
    
    # Audio
    "audio"                           = "source/audio"
    
    # Video
    "video"                           = "source/video"
    
    # Written content
    "writing"                         = "source/documents"
    "Written"                         = "source/documents"
    
    # Deployment-specific assets
    "Visuals/DEPLOYED/WordPress"      = "deployment/wordpress"
    "Visuals/DEPLOYED/SocialMedia"    = "deployment/web"
    "Visuals/DEPLOYED/YouTube"        = "deployment/web"
    "Visuals/DEPLOYED/GameEngine"     = "source/images"
    "Visuals/DEPLOYED/GenericWebApp"  = "deployment/web"
    "Visuals/DEPLOYED/PodcastPlatform" = "deployment/web"
}

# Statistics
$stats = @{
    TotalFiles = 0
    CopiedFiles = 0
    SkippedFiles = 0
    Errors = 0
    ByType = @{}
}

# Create directory structure if needed
foreach ($destDir in $migrationMap.Values | Sort-Object -Unique) {
    $path = Join-Path -Path $DestRoot -ChildPath $destDir
    if (-not (Test-Path -Path $path)) {
        Write-Log "Creating directory: $path"
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

# Process each mapping
foreach ($sourceRelPath in $migrationMap.Keys) {
    $destRelPath = $migrationMap[$sourceRelPath]
    $sourceDirPath = Join-Path -Path $sourcePath -ChildPath $sourceRelPath
    $destDirPath = Join-Path -Path $DestRoot -ChildPath $destRelPath
    
    # Skip if source doesn't exist
    if (-not (Test-Path -Path $sourceDirPath)) {
        Write-Log "Source path not found: $sourceDirPath" "Yellow"
        continue
    }
    
    # Track asset type
    $assetType = $destRelPath.Split('/')[0] + "/" + $destRelPath.Split('/')[1]
    if (-not $stats.ByType.ContainsKey($assetType)) {
        $stats.ByType[$assetType] = @{
            Total = 0
            Copied = 0
            Skipped = 0
            Errors = 0
        }
    }
    
    Write-Log "Processing $sourceRelPath -> $destRelPath" "Cyan"
    
    # Get all files in the source directory
    $files = Get-ChildItem -Path $sourceDirPath -File -Recurse
    
    foreach ($file in $files) {
        $stats.TotalFiles++
        $stats.ByType[$assetType].Total++
        
        # Get relative path from source root
        $relPath = $file.FullName.Substring($sourceDirPath.Length + 1)
        $destFilePath = Join-Path -Path $destDirPath -ChildPath $relPath
        
        # Create destination directory if needed
        $destFileDir = Split-Path -Path $destFilePath -Parent
        if (-not (Test-Path -Path $destFileDir)) {
            New-Item -ItemType Directory -Path $destFileDir -Force | Out-Null
        }
        
        try {
            # Check if destination file already exists
            if ((Test-Path -Path $destFilePath) -and -not $Force) {
                Write-Log "Skipping (already exists): $relPath" "Yellow"
                $stats.SkippedFiles++
                $stats.ByType[$assetType].Skipped++
                continue
            }
            
            # Copy the file
            Copy-Item -Path $file.FullName -Destination $destFilePath -Force
            Write-Log "Copied: $($file.Name) -> $destFilePath"
            $stats.CopiedFiles++
            $stats.ByType[$assetType].Copied++
        }
        catch {
            Write-Log "Error copying $($file.FullName): $_" "Red"
            $stats.Errors++
            $stats.ByType[$assetType].Errors++
        }
    }
}

# Write migration summary
Write-Log "`nMigration Summary:" "Green"
Write-Log "  Total Files: $($stats.TotalFiles)"
Write-Log "  Files Copied: $($stats.CopiedFiles)"
Write-Log "  Files Skipped: $($stats.SkippedFiles)"
Write-Log "  Errors: $($stats.Errors)"

Write-Log "`nBy Asset Type:"
foreach ($assetType in $stats.ByType.Keys) {
    Write-Log "  $assetType:"
    Write-Log "    Total: $($stats.ByType[$assetType].Total)"
    Write-Log "    Copied: $($stats.ByType[$assetType].Copied)"
    Write-Log "    Skipped: $($stats.ByType[$assetType].Skipped)"
    Write-Log "    Errors: $($stats.ByType[$assetType].Errors)"
}

Write-Host "`nTEC asset migration completed!" -ForegroundColor Green
Write-Host "  Total Files: $($stats.TotalFiles)" -ForegroundColor Cyan
Write-Host "  Files Copied: $($stats.CopiedFiles)" -ForegroundColor Cyan
Write-Host "  Files Skipped: $($stats.SkippedFiles)" -ForegroundColor Yellow
Write-Host "  Errors: $($stats.Errors)" -ForegroundColor Red
Write-Host "`nLog file: $logFile" -ForegroundColor Cyan
