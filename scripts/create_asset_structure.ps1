# create_asset_structure.ps1
# Script to create the TEC asset structure

# Set the assets root directory
$assetsRoot = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets"

# Define directory structure
$directories = @(
    # Source directories
    "source\images",
    "source\images\branding",
    "source\images\characters",
    "source\images\backgrounds",
    "source\images\ui",
    "source\images\posts",
    "source\images\social",
    "source\audio",
    "source\audio\music",
    "source\audio\sfx",
    "source\audio\voice",
    "source\video",
    "source\video\animations",
    "source\video\trailers",
    "source\video\tutorials",
    "source\documents",
    "source\documents\scripts",
    "source\documents\lore",
    "source\documents\templates",

    # Optimized directories - WordPress
    "optimized\wordpress\featured",
    "optimized\wordpress\thumbnails",
    "optimized\wordpress\content",

    # Optimized directories - HuggingFace
    "optimized\huggingface\ui",
    "optimized\huggingface\images",
    "optimized\huggingface\icons",

    # Optimized directories - Web
    "optimized\web\images",
    "optimized\web\audio",
    "optimized\web\video",

    # Deployment directories
    "deployment\wordpress",
    "deployment\docker",
    "deployment\huggingface",

    # Scripts directory
    "scripts"
)

Write-Host "Creating TEC asset directory structure..." -ForegroundColor Cyan

# Create each directory
foreach ($dir in $directories) {
    $path = Join-Path -Path $assetsRoot -ChildPath $dir
    
    # Check if directory already exists
    if (Test-Path $path) {
        Write-Host "Directory already exists: $dir" -ForegroundColor Yellow
    } else {
        # Create directory
        New-Item -Path $path -ItemType Directory -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    }
}

# Create sample metadata.json in the source directory
$metadataPath = Join-Path -Path $assetsRoot -ChildPath "source\metadata.json"
$metadataContent = @"
{
  "assets": [
    {
      "filename": "sample-asset.png",
      "type": "image",
      "category": "branding",
      "created": "$(Get-Date -Format "yyyy-MM-dd")",
      "creator": "TEC Design Team",
      "optimized_versions": {
        "wordpress": "/optimized/wordpress/content/sample-asset.jpg",
        "huggingface": "/optimized/huggingface/images/sample-asset.webp"
      },
      "tags": ["sample", "tec", "branding"],
      "usage": ["wordpress", "huggingface"]
    }
  ]
}
"@

if (-not (Test-Path $metadataPath)) {
    $metadataContent | Out-File -FilePath $metadataPath -Encoding utf8
    Write-Host "Created sample metadata.json file" -ForegroundColor Green
}

# Create placeholder optimizer script in the scripts directory
$optimizerPath = Join-Path -Path $assetsRoot -ChildPath "scripts\optimize.py"
$optimizerContent = @"
#!/usr/bin/env python3
"""
TEC Asset Optimizer Script

This script optimizes assets for different deployment targets:
- WordPress
- HuggingFace
- Web general use

Usage:
    python optimize.py --source [source_dir] --target [wordpress|huggingface|web]
"""
import os
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Optimize TEC assets for different platforms')
    parser.add_argument('--source', type=str, required=True, help='Source directory containing assets')
    parser.add_argument('--target', type=str, required=True, choices=['wordpress', 'huggingface', 'web'], 
                      help='Target platform for optimization')
    args = parser.parse_args()
    
    print(f"Optimizing assets from {args.source} for {args.target}...")
    # TODO: Implement actual optimization logic
    # For images: resize, compress, convert formats
    # For audio: convert formats, adjust bitrate
    # For video: compress, resize, adjust formats
    
    print("Optimization complete!")

if __name__ == '__main__':
    main()
"@

if (-not (Test-Path $optimizerPath)) {
    $optimizerContent | Out-File -FilePath $optimizerPath -Encoding utf8
    Write-Host "Created placeholder optimizer script" -ForegroundColor Green
}

# Create WordPress specific optimizer
$wpOptimizerPath = Join-Path -Path $assetsRoot -ChildPath "scripts\wordpress.py"
$wpOptimizerContent = @"
#!/usr/bin/env python3
"""
WordPress Asset Optimizer Script

This script processes and optimizes images specifically for WordPress:
- Creates featured images (1200x630px)
- Creates thumbnails (150x150px)
- Optimizes content images (800px max width)

Usage:
    python wordpress.py --image [image_path] --type [featured|thumbnail|content]
"""
import os
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Optimize images for WordPress')
    parser.add_argument('--image', type=str, required=True, help='Path to source image')
    parser.add_argument('--type', type=str, required=True, 
                       choices=['featured', 'thumbnail', 'content'], 
                       help='Type of WordPress image to create')
    args = parser.parse_args()
    
    print(f"Processing {args.image} as WordPress {args.type} image...")
    # TODO: Implement image processing
    # - For featured: resize to 1200x630
    # - For thumbnail: resize to 150x150
    # - For content: resize to max width 800px
    # - Compress all images to target file size
    
    print("WordPress image processing complete!")

if __name__ == '__main__':
    main()
"@

if (-not (Test-Path $wpOptimizerPath)) {
    $wpOptimizerContent | Out-File -FilePath $wpOptimizerPath -Encoding utf8
    Write-Host "Created WordPress optimizer script" -ForegroundColor Green
}

# Create HuggingFace specific optimizer
$hfOptimizerPath = Join-Path -Path $assetsRoot -ChildPath "scripts\huggingface.py"
$hfOptimizerContent = @"
#!/usr/bin/env python3
"""
HuggingFace Asset Optimizer Script

This script processes and optimizes assets specifically for HuggingFace Spaces:
- Compresses images to minimize total space usage
- Converts to web-friendly formats
- Ensures assets stay below size limits

Usage:
    python huggingface.py --asset [asset_path] --type [ui|image|icon]
"""
import os
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Optimize assets for HuggingFace')
    parser.add_argument('--asset', type=str, required=True, help='Path to source asset')
    parser.add_argument('--type', type=str, required=True, 
                       choices=['ui', 'image', 'icon'], 
                       help='Type of HuggingFace asset to create')
    args = parser.parse_args()
    
    print(f"Processing {args.asset} as HuggingFace {args.type}...")
    # TODO: Implement asset processing
    # - For UI: convert to SVG when possible, or optimize PNG
    # - For images: convert to WebP, max size 1200px on longest side
    # - For icons: create optimized PNG or SVG
    # - Target under 100KB per image
    
    print("HuggingFace asset processing complete!")

if __name__ == '__main__':
    main()
"@

if (-not (Test-Path $hfOptimizerPath)) {
    $hfOptimizerContent | Out-File -FilePath $hfOptimizerPath -Encoding utf8
    Write-Host "Created HuggingFace optimizer script" -ForegroundColor Green
}

Write-Host "`nTEC asset structure creation complete!" -ForegroundColor Cyan
Write-Host "Next steps:"
Write-Host "1. Run data migration script to move existing assets" -ForegroundColor Yellow
Write-Host "2. Implement the optimizer scripts with actual image processing" -ForegroundColor Yellow
Write-Host "3. Update code references to use the new asset paths" -ForegroundColor Yellow
