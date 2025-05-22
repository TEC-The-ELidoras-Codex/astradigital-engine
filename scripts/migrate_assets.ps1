# migrate_assets.ps1
# Script to migrate existing assets from Data-dump&Deploy to the new structure

# Set the assets root directory
$assetsRoot = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets"
$sourceDump = Join-Path -Path $assetsRoot -ChildPath "Data-dump&Deploy"

# Check if source directory exists
if (-not (Test-Path $sourceDump)) {
    Write-Host "Error: Data-dump&Deploy directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Starting asset migration..." -ForegroundColor Cyan
Write-Host "This script will migrate assets from the old structure to the new organization." -ForegroundColor Cyan
Write-Host "Source: $sourceDump" -ForegroundColor Yellow
Write-Host "Target: $assetsRoot\source" -ForegroundColor Yellow
Write-Host ""

# Mapping of old directories to new structure
$migrationMap = @{
    # Images
    "Image" = "source\images"
    "Image\Airth_Character_Concept_Alpha" = "source\images\characters"
    "Image\MACHINE_GODDESS_MOSTW" = "source\images\characters"
    "Visuals\Branding" = "source\images\branding"
    "Visuals\Graphics" = "source\images\ui"
    "Visuals\Animations" = "source\video\animations"
    "Visuals\Mindmaps" = "source\documents\lore"
    
    # Audio
    "audio" = "source\audio"
    
    # Video
    "video" = "source\video"
    
    # Written content
    "writing" = "source\documents"
    "Written" = "source\documents"
    
    # Deployment-specific assets (keep a record of what was deployed)
    "Visuals\DEPLOYED\WordPress" = "deployment\wordpress"
    "Visuals\DEPLOYED\SocialMedia" = "deployment\web"
    "Visuals\DEPLOYED\YouTube" = "deployment\web"
    "Visuals\DEPLOYED\GameEngine" = "source\images"  # These need proper categorization later
    "Visuals\DEPLOYED\GenericWebApp" = "deployment\web"
    "Visuals\DEPLOYED\PodcastPlatform" = "deployment\web"
}

# Function to recursively copy assets while preserving folder structure
function Copy-AssetWithStructure {
    param (
        [string]$sourcePath,
        [string]$destinationBase,
        [string]$destSubPath
    )
    
    # Create full destination path
    $destinationPath = Join-Path -Path $destinationBase -ChildPath $destSubPath
    
    # Ensure destination directory exists
    if (-not (Test-Path $destinationPath)) {
        New-Item -Path $destinationPath -ItemType Directory -Force | Out-Null
    }
    
    # Get all files in the source directory
    if (Test-Path $sourcePath) {
        $files = Get-ChildItem -Path $sourcePath -File
        
        # Copy each file
        foreach ($file in $files) {
            $destFile = Join-Path -Path $destinationPath -ChildPath $file.Name
            
            # Check if destination already exists
            if (Test-Path $destFile) {
                Write-Host "  Skipping (already exists): $($file.Name)" -ForegroundColor Yellow
            } else {
                Copy-Item -Path $file.FullName -Destination $destFile
                Write-Host "  Copied: $($file.Name)" -ForegroundColor Green
            }
        }
        
        # Process subdirectories
        $dirs = Get-ChildItem -Path $sourcePath -Directory
        
        foreach ($dir in $dirs) {
            $newDestSubPath = Join-Path -Path $destSubPath -ChildPath $dir.Name
            Copy-AssetWithStructure -sourcePath $dir.FullName -destinationBase $destinationBase -destSubPath $newDestSubPath
        }
    } else {
        Write-Host "Warning: Source path not found: $sourcePath" -ForegroundColor Yellow
    }
}

# Process each mapping
foreach ($mapping in $migrationMap.GetEnumerator()) {
    $sourcePath = Join-Path -Path $sourceDump -ChildPath $mapping.Key
    $destPath = Join-Path -Path $assetsRoot -ChildPath $mapping.Value
    
    Write-Host "Migrating: $($mapping.Key) -> $($mapping.Value)" -ForegroundColor Cyan
    
    if (Test-Path $sourcePath) {
        # Copy assets
        Copy-AssetWithStructure -sourcePath $sourcePath -destinationBase $assetsRoot -destSubPath $mapping.Value
    } else {
        Write-Host "  Source directory not found: $sourcePath" -ForegroundColor Yellow
    }
}

# Create a migration log
$logContent = @"
# Asset Migration Log
Migration performed on: $(Get-Date)

## Migration Mappings
$(($migrationMap.GetEnumerator() | ForEach-Object { "- $($_.Key) -> $($_.Value)" }) -join "`n")

## Notes
- This migration preserved the original files in Data-dump&Deploy
- Assets were categorized based on their original location
- Additional optimization and categorization may be needed
"@

$logPath = Join-Path -Path $assetsRoot -ChildPath "migration_log.md"
$logContent | Out-File -FilePath $logPath -Encoding utf8

Write-Host "`nAsset migration complete!" -ForegroundColor Cyan
Write-Host "Migration log created at: $logPath" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Review migrated assets and ensure proper categorization" -ForegroundColor Yellow
Write-Host "2. Run optimization scripts for WordPress, HuggingFace, etc." -ForegroundColor Yellow
Write-Host "3. Update code references to use the new asset paths" -ForegroundColor Yellow
