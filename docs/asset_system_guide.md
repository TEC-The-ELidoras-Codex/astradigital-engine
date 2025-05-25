# TEC Asset System Usage Guide

This guide explains how to use the new TEC asset organization system for WordPress and HuggingFace deployments.

## Table of Contents
- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Asset Workflow](#asset-workflow)
- [WordPress Integration](#wordpress-integration)
- [HuggingFace Integration](#huggingface-integration)
- [Docker Integration](#docker-integration)
- [Asset Optimization Scripts](#asset-optimization-scripts)
- [Troubleshooting](#troubleshooting)

## Overview

The TEC asset system organizes all multimedia resources for optimal use across different deployment platforms. It maintains:

1. **Source assets** - Original, high-quality files
2. **Optimized assets** - Platform-specific versions of assets, optimized for performance
3. **Deployment assets** - Ready-to-use assets for specific deployment targets

## Directory Structure

```
assets/
├── source/            # Original files
├── optimized/         # Platform-specific optimized versions
│   ├── wordpress/     # WordPress optimizations
│   ├── huggingface/   # HuggingFace optimizations
│   └── web/           # General web optimizations
├── deployment/        # Ready-for-deployment assets
└── scripts/           # Asset processing scripts
```

## Asset Workflow

### 1. Adding New Assets

Place new assets in the appropriate `source` subdirectory:

```powershell
# For images
Copy-Item "path\to\your\image.png" -Destination "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\source\images\[category]\"

# For audio
Copy-Item "path\to\your\audio.mp3" -Destination "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\source\audio\[category]\"
```

### 2. Optimizing Assets

Use the optimization scripts to create platform-specific versions:

```powershell
# For WordPress
cd C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\scripts
python optimize.py --source ..\source\images --target wordpress

# For HuggingFace
python optimize.py --source ..\source\images --target huggingface

# For general web use
python optimize.py --source ..\source\images --target web
```

### 3. Deploying Assets

Copy optimized assets to deployment directories when ready for use:

```powershell
# Example: Copy WordPress-optimized images to deployment
Copy-Item "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\optimized\wordpress\*" -Destination "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\deployment\wordpress\" -Recurse
```

## WordPress Integration

### Using Assets in WordPress Posts

1. **Upload to WordPress**: Use the WordPress agent to upload optimized images:

```python
from src.agents.wp_poster import WordPressAgent

wp_agent = WordPressAgent()
media_data = wp_agent.upload_media(
    file_path="C:/Users/Ghedd/TEC_CODE/astradigital-engine/assets/optimized/wordpress/featured/character-airth-portrait.jpg",
    title="Airth Character Portrait"
)

# Get the media ID for use in posts
media_id = media_data.get("id")
```

2. **Use in Post Content**: Reference the optimized content images in your post HTML:

```python
content = f"""
<p>This is a blog post about Airth.</p>
<img src="{media_data['source_url']}" alt="Airth Character Portrait" class="wp-image-{media_id}"/>
<p>More content here...</p>
"""

post_data = wp_agent.create_post(
    title="Airth's Adventures",
    content=content,
    featured_media_id=media_id  # Set as featured image
)
```

### Optimizing for WordPress Performance

- **Featured Images**: Use images from `optimized/wordpress/featured` (1200×630px)
- **Thumbnails**: Use images from `optimized/wordpress/thumbnails` (150×150px)
- **Content Images**: Use images from `optimized/wordpress/content` (800px max width)

## HuggingFace Integration

### Setting Up Assets for HuggingFace Spaces

1. **Prepare Assets**:

```powershell
# Optimize images for HuggingFace
python assets\scripts\optimize.py --source assets\source\images --target huggingface
```

2. **Deploy to HuggingFace Space**:

Update your Hugging Face deployment script to include the optimized assets:

```powershell
# Example addition to deploy_to_hf_space.ps1
$assetsPath = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\optimized\huggingface"
$deployPath = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\hf_app_assets"

# Create target directory if it doesn't exist
if (-not (Test-Path $deployPath)) {
    New-Item -Path $deployPath -ItemType Directory -Force | Out-Null
}

# Copy optimized assets to deployment directory
Copy-Item "$assetsPath\*" -Destination "$deployPath" -Recurse -Force
```

3. **Reference in HuggingFace App**:

```python
# In your Gradio app (app.py or hf_app.py)
import os
import gradio as gr

# Define image paths
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "hf_app_assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "ui", "tec-logo.png")
BACKGROUND_PATH = os.path.join(ASSETS_DIR, "images", "background-astradigital.webp")

# Use in Gradio components
with gr.Blocks(theme="huggingface", title="TEC Office - The Elidoras Codex") as demo:
    with gr.Row():
        gr.Image(LOGO_PATH, show_label=False, elem_id="tec-logo")
        
    with gr.Row():
        gr.HTML(f'<div style="background-image: url(\'{BACKGROUND_PATH}\')">...</div>')
```

### Optimizing for HuggingFace Performance

- Keep total asset size minimal (HF Space has size limits)
- Use WebP format for images (better compression)
- Use SVG for UI elements when possible (scalable, small file size)
- Compress all assets aggressively

## Docker Integration

The Docker integration allows you to prepare and optimize assets for Docker container deployment. This ensures minimal container size while preserving asset quality.

### Preparing Assets for Docker

```powershell
# Navigate to the project directory
cd "C:\Users\Ghedd\TEC_CODE\astradigital-engine"

# Prepare assets for a specific Docker container
python assets/scripts/prepare_docker_assets.py --name "tec-container" --source "assets/source/images/logo"
```

### Docker Asset Package Structure

The Docker asset preparation script creates a deployment package with:

1. **Optimized images**: Converted to WebP format with reduced size
2. **Configuration files**: Preserved in their original format
3. **Static files**: Web assets for use in containers
4. **Docker integration files**: Dockerfile snippets and Docker Compose examples

### Using Docker Assets in Containers

Each Docker asset package includes:

1. `Dockerfile.snippet`: Copy-paste these commands into your Dockerfile
2. `docker-compose.snippet.yml`: Example configuration for Docker Compose
3. `README.md`: Specific instructions for this asset package

Example Dockerfile integration:

```dockerfile
# Base image
FROM python:3.9-slim

# Application setup
WORKDIR /app
COPY . /app/

# Copy assets into container
COPY ./assets/static/ /app/static/
COPY ./assets/images/ /app/images/
COPY ./assets/config/ /app/config/

# Environment variables for asset paths
ENV ASSET_PATH=/app
ENV STATIC_PATH=/app/static
ENV IMAGES_PATH=/app/images
ENV CONFIG_PATH=/app/config
```

### Including Assets in Docker Containers

1. **Add to Dockerfile**:

```Dockerfile
# Copy only necessary optimized assets
COPY assets/optimized/web /app/assets

# For WordPress-specific containers
COPY assets/optimized/wordpress /app/wordpress_assets
```

2. **Use Volume Mounts for Development**:

```yaml
# In docker-compose.yml
services:
  tec_app:
    build: .
    volumes:
      - ./assets/optimized:/app/assets:ro
```

3. **Access in Application**:

```python
import os

ASSETS_DIR = os.environ.get("ASSETS_DIR", "/app/assets")

def get_asset_path(asset_type, filename):
    """Get the path to an asset file"""
    return os.path.join(ASSETS_DIR, asset_type, filename)
```

### Optimizing Docker Image Size

Efficient asset management is crucial for Docker container optimization:

1. **Use Multi-stage Builds**:

```Dockerfile
# Build stage for asset optimization
FROM python:3.9-slim as asset-builder

WORKDIR /build
COPY assets/source ./source
COPY assets/scripts ./scripts

RUN pip install Pillow
RUN python scripts/optimize.py --source ./source --target web

# Final stage with only optimized assets
FROM nginx:alpine
COPY --from=asset-builder /build/optimized/web /usr/share/nginx/html/assets
```

2. **Create Platform-Specific Asset Packages**:

```powershell
# Prepare Docker-specific assets
python assets\scripts\optimize.py --source assets\source\images --target web --docker

# The --docker flag will create Docker-optimized assets with extra compression
```

3. **Docker-Specific Asset Configuration**:

You can override the default web optimization settings for Docker specifically:

```python
# In your Python script
docker_config = {
    "images": {
        "max_width": 1000,
        "quality": 70,
        "format": "WEBP"
    },
    "icons": {
        "max_width": 64,
        "quality": 85, 
        "format": "PNG"
    }
}

# Apply Docker-specific optimizations
optimize_for_docker(source_dir, output_dir, docker_config)
```

## Asset Optimization Scripts

The `assets/scripts` directory contains Python tools for optimizing assets:

- `optimize.py` - Main script for optimizing assets for different platforms
- `wordpress.py` - WordPress-specific optimization
- `huggingface.py` - HuggingFace-specific optimization

### Script Usage Examples

```powershell
# Basic optimization
python assets\scripts\optimize.py --source assets\source\images\characters --target wordpress

# WordPress optimization options
python assets\scripts\wordpress.py --image assets\source\images\characters\airth-portrait.png --type featured

# HuggingFace optimization
python assets\scripts\huggingface.py --asset assets\source\images\ui\logo.png --type ui
```

## Troubleshooting

### Common Issues

1. **Missing Assets**:
   - Verify assets are in the correct source directory
   - Check that optimization scripts have been run
   - Ensure deployment scripts copy the assets to the correct location

2. **WordPress Upload Errors**:
   - Check WordPress upload file size limits
   - Verify WordPress API credentials
   - Look for PHP errors in WordPress logs

3. **HuggingFace Deployment Issues**:
   - Check total asset size (HF has space limitations)
   - Verify assets are correctly referenced in the app
   - Test locally before deploying

4. **Image Quality Issues**:
   - Adjust quality settings in optimization scripts
   - Use proper image formats for each use case
   - Start with higher-quality source images

### Getting Help

If you encounter persistent issues with the asset system:

1. Check the asset optimization logs
2. Verify file paths and permissions
3. Run the scripts with `--verbose` flag for more detailed output
4. Consult the full documentation in `docs/assets.md`
