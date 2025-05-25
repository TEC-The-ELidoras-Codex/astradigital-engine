#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Creates the TEC asset directory structure

.DESCRIPTION
    This script sets up the required directory structure for the TEC asset organization system.
    It creates the main directory hierarchy needed for organizing assets for different platforms.

.NOTES
    File Name      : create_asset_structure.ps1
    Author         : TEC Development Team
#>

# Base assets directory (where this script should be run)
$assetsRoot = $PWD.Path

# Define the directory structure
$directories = @(
    # Source directories
    "source",
    "source/images",
    "source/images/characters",
    "source/images/locations",
    "source/images/concepts",
    "source/images/branding",
    "source/images/ui",
    "source/audio",
    "source/video",
    "source/documents",
    "source/documents/lore",

    # Optimized directories
    "optimized",
    "optimized/wordpress",
    "optimized/wordpress/featured",
    "optimized/wordpress/thumbnails",
    "optimized/wordpress/content",
    "optimized/huggingface",
    "optimized/huggingface/ui",
    "optimized/huggingface/images",
    "optimized/huggingface/icons",
    "optimized/web",
    "optimized/web/images",
    "optimized/web/thumbnails",
    "optimized/web/audio",
    "optimized/web/video",

    # Deployment directories
    "deployment",
    "deployment/wordpress",
    "deployment/huggingface",
    "deployment/docker",

    # Scripts directory
    "scripts"
)

# Create each directory
foreach ($dir in $directories) {
    $path = Join-Path -Path $assetsRoot -ChildPath $dir
    
    if (-not (Test-Path -Path $path)) {
        Write-Host "Creating directory: $path"
        New-Item -ItemType Directory -Path $path | Out-Null
    } else {
        Write-Host "Directory already exists: $path" -ForegroundColor Yellow
    }
}

# Create README files for key directories
$readmeFiles = @{
    "."                     = "# TEC Asset System`n`nThis directory contains all assets for The Elidoras Codex, organized by source, optimization level, and deployment target."
    "source"                = "# Source Assets`n`nThis directory contains original, high-quality source files. Always preserve these files in their original format and quality."
    "optimized"             = "# Optimized Assets`n`nThis directory contains platform-specific optimized versions of assets. These are automatically generated from source files."
    "deployment"            = "# Deployment Assets`n`nThis directory contains ready-to-deploy asset packages for different platforms."
    "scripts"               = "# Asset Processing Scripts`n`nThis directory contains scripts for processing, optimizing, and preparing assets for different platforms."
    "source/images"         = "# Source Images`n`nThis directory contains original, high-quality images. Preserve these files in their original format and quality."
    "source/audio"          = "# Source Audio`n`nThis directory contains original, high-quality audio files. Preserve these files in their original format and quality."
    "source/video"          = "# Source Video`n`nThis directory contains original, high-quality video files. Preserve these files in their original format and quality."
    "source/documents"      = "# Source Documents`n`nThis directory contains original text documents, scripts, and other written content."
    "optimized/wordpress"   = "# WordPress-Optimized Assets`n`nThis directory contains assets optimized specifically for WordPress."
    "optimized/huggingface" = "# HuggingFace-Optimized Assets`n`nThis directory contains assets optimized specifically for HuggingFace Spaces."
    "optimized/web"         = "# Web-Optimized Assets`n`nThis directory contains assets optimized for general web use."
    "deployment/wordpress"  = "# WordPress Deployment Packages`n`nThis directory contains ready-to-upload WordPress asset packages."
    "deployment/huggingface"= "# HuggingFace Deployment Packages`n`nThis directory contains ready-to-deploy HuggingFace asset packages."
}

foreach ($path in $readmeFiles.Keys) {
    $filePath = Join-Path -Path $assetsRoot -ChildPath "$path/README.md"
    
    if (-not (Test-Path -Path $filePath)) {
        Write-Host "Creating README: $filePath"
        $readmeFiles[$path] | Out-File -FilePath $filePath -Encoding utf8
    } else {
        Write-Host "README already exists: $filePath" -ForegroundColor Yellow
    }
}

Write-Host "`nTEC asset directory structure created successfully!" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  1. Run setup_asset_tools.ps1 to install required dependencies" -ForegroundColor Cyan
Write-Host "  2. Run migrate_assets.ps1 to migrate existing assets" -ForegroundColor Cyan
Write-Host "  3. Use optimize.py to prepare assets for different platforms" -ForegroundColor Cyan
