# setup_asset_system.ps1
# Script to setup the complete TEC asset organization system
# This script:
# 1. Creates the directory structure
# 2. Migrates existing assets to the new structure
# 3. Sets up asset optimization tools
# 4. Runs initial optimization for WordPress and HuggingFace
# 5. Validates the asset system

Write-Host "TEC Asset System Setup" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "C:\Users\Ghedd\TEC_CODE\astradigital-engine"
$assetsRoot = Join-Path -Path $projectRoot -ChildPath "assets"
$scriptsDir = Join-Path -Path $projectRoot -ChildPath "scripts"

# Step 1: Create directory structure
Write-Host "Step 1: Creating directory structure..." -ForegroundColor Yellow

$createStructureScript = Join-Path -Path $scriptsDir -ChildPath "create_asset_structure.ps1"
if (Test-Path $createStructureScript) {
    & $createStructureScript
} else {
    Write-Host "Error: create_asset_structure.ps1 not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Migrate existing assets
Write-Host "Step 2: Migrating existing assets..." -ForegroundColor Yellow

$migrateAssetsScript = Join-Path -Path $scriptsDir -ChildPath "migrate_assets.ps1"
if (Test-Path $migrateAssetsScript) {
    & $migrateAssetsScript
} else {
    Write-Host "Error: migrate_assets.ps1 not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Set up asset optimization tools
Write-Host "Step 3: Setting up asset optimization tools..." -ForegroundColor Yellow

$setupToolsScript = Join-Path -Path $scriptsDir -ChildPath "setup_asset_tools.ps1"
if (Test-Path $setupToolsScript) {
    & $setupToolsScript
} else {
    Write-Host "Error: setup_asset_tools.ps1 not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 4: Run initial optimization for WordPress and HuggingFace
Write-Host "Step 4: Running initial asset optimization..." -ForegroundColor Yellow

$sourcePath = Join-Path -Path $assetsRoot -ChildPath "source"

# Check if there are any images to process
$sourceImages = Join-Path -Path $sourcePath -ChildPath "images"
$hasImages = (Get-ChildItem -Path $sourceImages -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0

if ($hasImages) {
    # Run WordPress optimization
    Write-Host "Running WordPress optimization..." -ForegroundColor Cyan
    try {
        $wpOptimizeScript = Join-Path -Path $assetsRoot -ChildPath "scripts\optimize.py"
        if (Test-Path $wpOptimizeScript) {
            & python $wpOptimizeScript --source $sourceImages --target wordpress
        } else {
            Write-Host "  Warning: WordPress optimization script not found" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Error during WordPress optimization: $_" -ForegroundColor Red
    }
    
    # Run HuggingFace optimization
    Write-Host "Running HuggingFace optimization..." -ForegroundColor Cyan
    try {
        $hfOptimizeScript = Join-Path -Path $assetsRoot -ChildPath "scripts\optimize.py"
        if (Test-Path $hfOptimizeScript) {
            & python $hfOptimizeScript --source $sourceImages --target huggingface
        } else {
            Write-Host "  Warning: HuggingFace optimization script not found" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Error during HuggingFace optimization: $_" -ForegroundColor Red
    }
} else {
    Write-Host "No source images found to optimize" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Validate the asset system
Write-Host "Step 5: Validating asset system..." -ForegroundColor Yellow

$structureValid = $true

# Check for essential directories
$requiredDirs = @(
    "source\images",
    "optimized\wordpress",
    "optimized\huggingface",
    "deployment\wordpress",
    "deployment\huggingface",
    "scripts"
)

foreach ($dir in $requiredDirs) {
    $dirPath = Join-Path -Path $assetsRoot -ChildPath $dir
    if (-not (Test-Path $dirPath)) {
        Write-Host "  Missing directory: $dir" -ForegroundColor Red
        $structureValid = $false
    }
}

# Check for essential scripts
$requiredScripts = @(
    "scripts\optimize.py",
    "scripts\wordpress.py",
    "scripts\huggingface.py",
    "scripts\prepare_wp_assets.py",
    "scripts\prepare_hf_assets.py"
)

foreach ($script in $requiredScripts) {
    $scriptPath = Join-Path -Path $assetsRoot -ChildPath $script
    if (-not (Test-Path $scriptPath)) {
        Write-Host "  Missing script: $script" -ForegroundColor Red
        $structureValid = $false
    }
}

# Check if documentation exists
$docsPath = Join-Path -Path $projectRoot -ChildPath "docs\asset_system_guide.md"
if (-not (Test-Path $docsPath)) {
    Write-Host "  Missing documentation: docs\asset_system_guide.md" -ForegroundColor Red
    $structureValid = $false
}

if ($structureValid) {
    Write-Host "  Asset system validated successfully" -ForegroundColor Green
} else {
    Write-Host "  Asset system validation found issues" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "TEC Asset System Setup Complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Optimize your assets for WordPress: python assets\scripts\optimize.py --source assets\source\images --target wordpress" -ForegroundColor White
Write-Host "2. Optimize your assets for HuggingFace: python assets\scripts\optimize.py --source assets\source\images --target huggingface" -ForegroundColor White
Write-Host "3. Prepare WordPress assets for a post: python assets\scripts\prepare_wp_assets.py --post \"Post Title\" --source assets\source\images\post-folder" -ForegroundColor White
Write-Host "4. Prepare HuggingFace assets: python assets\scripts\prepare_hf_assets.py --name \"space-name\" --source assets\source\images" -ForegroundColor White
Write-Host "5. Read the documentation: docs\asset_system_guide.md" -ForegroundColor White
