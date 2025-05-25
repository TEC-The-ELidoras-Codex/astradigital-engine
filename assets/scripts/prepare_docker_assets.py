#!/usr/bin/env python3
"""
Docker Asset Preparation Script

This script prepares assets for Docker deployment by:
1. Optimizing source images for Docker containers
2. Creating a deployment package with proper structure
3. Generating Dockerfile snippets for easy integration

Usage:
    python prepare_docker_assets.py --name [container_name] --source [source_dir]
"""

import os
import sys
import argparse
import logging
import shutil
import json
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.DockerAssetPrep")

# Constants
ASSETS_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
OPTIMIZED_DIR = os.path.join(ASSETS_ROOT, "optimized", "docker")
DEPLOYMENT_DIR = os.path.join(ASSETS_ROOT, "deployment", "docker")

def optimize_for_docker(source_dir, container_name):
    """Optimize assets in source directory for Docker containers"""
    # Create container-specific subdirectories
    timestamp = datetime.now().strftime("%Y%m%d")
    container_dir = f"{timestamp}-{container_name}"
    
    static_dir = os.path.join(OPTIMIZED_DIR, "static", container_dir)
    images_dir = os.path.join(OPTIMIZED_DIR, "images", container_dir)
    config_dir = os.path.join(OPTIMIZED_DIR, "config", container_dir)
    
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    
    # Find source files
    source_path = Path(source_dir)
    
    # Find images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.svg', '*.webp']:
        image_files.extend(list(source_path.glob(f"**/{ext}")))
    
    # Find config files
    config_files = []
    for ext in ['*.json', '*.yaml', '*.yml', '*.conf', '*.cfg']:
        config_files.extend(list(source_path.glob(f"**/{ext}")))
    
    # Find other static files
    static_files = []
    for ext in ['*.html', '*.css', '*.js', '*.txt', '*.md']:
        static_files.extend(list(source_path.glob(f"**/{ext}")))
    
    if not (image_files or config_files or static_files):
        logger.warning(f"No assets found in {source_dir}")
        return None
        
    total_files = len(image_files) + len(config_files) + len(static_files)
    logger.info(f"Found {total_files} files to process")
    
    # Process each file using the optimize script
    results = {
        'static': [],
        'images': [],
        'config': []
    }
    
    # Path to optimizer script
    optimizer_script = os.path.join(ASSETS_ROOT, "scripts", "docker.py")
    
    # Process image files
    for img_path in image_files:
        output_file = os.path.join(images_dir, img_path.name)
        
        # Run optimizer in separate process
        logger.info(f"Processing image {img_path}")
        
        try:
            import subprocess
            subprocess.run([
                sys.executable, optimizer_script,
                "--asset", str(img_path),
                "--type", "image",
                "--output", output_file
            ], check=True)
            results['images'].append(output_file)
        except subprocess.CalledProcessError:
            logger.error(f"Failed to optimize {img_path}")
            # Fallback: copy the original
            shutil.copy(str(img_path), output_file)
            results['images'].append(output_file)
    
    # Process config files - just copy them
    for config_path in config_files:
        output_file = os.path.join(config_dir, config_path.name)
        logger.info(f"Copying config file {config_path}")
        shutil.copy(str(config_path), output_file)
        results['config'].append(output_file)
    
    # Process static files
    for static_path in static_files:
        output_file = os.path.join(static_dir, static_path.name)
        logger.info(f"Copying static file {static_path}")
        shutil.copy(str(static_path), output_file)
        results['static'].append(output_file)
    
    return results

def prepare_deployment_package(results, container_name):
    """Prepare a deployment package for Docker container"""
    timestamp = datetime.now().strftime("%Y%m%d")
    deploy_dir = os.path.join(DEPLOYMENT_DIR, f"{timestamp}-{container_name}")
    os.makedirs(deploy_dir, exist_ok=True)
    
    # Create subdirectories for assets
    os.makedirs(os.path.join(deploy_dir, "static"), exist_ok=True)
    os.makedirs(os.path.join(deploy_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(deploy_dir, "config"), exist_ok=True)
    
    # Copy all optimized assets to deployment directory
    all_files = []
    total_size = 0
    
    for category, file_list in results.items():
        category_dir = os.path.join(deploy_dir, category)
        
        for file_path in file_list:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(category_dir, filename)
            shutil.copy(file_path, dest_path)
            
            file_size = os.path.getsize(file_path)
            total_size += file_size
            
            all_files.append({
                'category': category,
                'filename': filename,
                'path': dest_path,
                'size': file_size
            })
    
    # Create metadata file
    metadata = {
        'container_name': container_name,
        'created': datetime.now().isoformat(),
        'files': all_files,
        'stats': {
            'static': len([f for f in all_files if f['category'] == 'static']),
            'images': len([f for f in all_files if f['category'] == 'images']),
            'config': len([f for f in all_files if f['category'] == 'config']),
            'total_files': len(all_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }
    }
    
    metadata_path = os.path.join(deploy_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Create Dockerfile snippet
    dockerfile_content = f"""
# Dockerfile snippet for {container_name}
# Generated by TEC Asset System on {datetime.now().strftime("%Y-%m-%d")}

# Copy assets into container
COPY ./assets/static/ /app/static/
COPY ./assets/images/ /app/images/
COPY ./assets/config/ /app/config/

# Environment variables for asset paths
ENV ASSET_PATH=/app
ENV STATIC_PATH=/app/static
ENV IMAGES_PATH=/app/images
ENV CONFIG_PATH=/app/config

# Set permissions if needed
RUN chmod -R 755 /app/static /app/images
"""
    
    dockerfile_path = os.path.join(deploy_dir, 'Dockerfile.snippet')
    with open(dockerfile_path, 'w', encoding='utf-8') as f:
        f.write(dockerfile_content)
    
    # Create Docker Compose snippet
    compose_content = f"""
# Docker Compose snippet for {container_name}
# Generated by TEC Asset System on {datetime.now().strftime("%Y-%m-%d")}

version: '3'
services:
  {container_name}:
    build: .
    volumes:
      - ./assets/config:/app/config
    environment:
      - ASSET_PATH=/app
      - STATIC_PATH=/app/static
      - IMAGES_PATH=/app/images
      - CONFIG_PATH=/app/config
"""
    
    compose_path = os.path.join(deploy_dir, 'docker-compose.snippet.yml')
    with open(compose_path, 'w', encoding='utf-8') as f:
        f.write(compose_content)
    
    # Create README for the package
    readme_content = f"""# Docker Assets - {container_name}

## Overview

This package contains optimized assets for the "{container_name}" Docker container.

- **Total files**: {metadata['stats']['total_files']}
- **Total size**: {metadata['stats']['total_size_mb']} MB
- **Static files**: {metadata['stats']['static']}
- **Images**: {metadata['stats']['images']}
- **Config files**: {metadata['stats']['config']}

## Usage Instructions

1. Copy the entire `assets` directory to your Docker build context
2. Include the Dockerfile snippet in your Dockerfile:

```dockerfile
{dockerfile_content}
```

3. Or use the docker-compose snippet in your docker-compose.yml file

## File Locations

Within your container, assets will be available at:

- `/app/static/` - Static web files
- `/app/images/` - Optimized images
- `/app/config/` - Configuration files

## Asset Optimization

All images have been optimized for minimal container size while maintaining quality.
The total asset package adds approximately {metadata['stats']['total_size_mb']} MB to your container size.

## Generated on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}
"""
    
    readme_path = os.path.join(deploy_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return deploy_dir

def main():
    parser = argparse.ArgumentParser(description='Prepare assets for Docker container')
    parser.add_argument('--name', type=str, required=True, help='Docker container name')
    parser.add_argument('--source', type=str, required=True, help='Source directory containing assets')
    args = parser.parse_args()
    
    # Validate source directory
    if not os.path.isdir(args.source):
        logger.error(f"Source directory not found: {args.source}")
        return 1
    
    logger.info(f"Preparing assets for Docker container: {args.name}")
    
    # Check if docker.py exists
    docker_script = os.path.join(ASSETS_ROOT, "scripts", "docker.py")
    if not os.path.exists(docker_script):
        # Create minimal version for this script to work
        os.makedirs(os.path.dirname(docker_script), exist_ok=True)
        with open(docker_script, 'w') as f:
            f.write('''
#!/usr/bin/env python3
"""
Docker Asset Optimizer Script
"""
import os
import sys
import argparse
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("PIL not available. Images will be copied without optimization.")

def optimize_image(input_path, output_path):
    """Optimize an image for Docker deployment"""
    try:
        if 'Image' in globals():
            img = Image.open(input_path)
            
            # Use WebP format for smaller file sizes in Docker
            output_path_webp = os.path.splitext(output_path)[0] + ".webp"
            
            # Reduce size to max 800px width
            width, height = img.size
            if width > 800:
                ratio = 800.0 / width
                height = int(height * ratio)
                width = 800
                img = img.resize((width, height), Image.LANCZOS)
            
            # Save as WebP with good compression
            img.save(output_path_webp, "WEBP", quality=75)
            return output_path_webp
        else:
            # No PIL available, just copy
            shutil.copy(input_path, output_path)
            return output_path
    except Exception as e:
        print(f"Error optimizing image: {e}")
        shutil.copy(input_path, output_path)
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Optimize assets for Docker')
    parser.add_argument('--asset', type=str, required=True, help='Path to source asset')
    parser.add_argument('--type', type=str, required=True, 
                      choices=['image', 'static', 'config'], 
                      help='Type of Docker asset')
    parser.add_argument('--output', type=str, help='Output file path')
    args = parser.parse_args()
    
    # Make sure output directory exists
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Process based on type
    if args.type == 'image':
        final_path = optimize_image(args.asset, args.output)
        print(f"Optimized image saved to: {final_path}")
    else:
        # For other file types, just copy
        shutil.copy(args.asset, args.output)
        print(f"Copied {args.type} file to: {args.output}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
''')
        logger.info(f"Created basic docker.py script at {docker_script}")

    # Optimize source assets
    results = optimize_for_docker(args.source, args.name)
    if not results:
        logger.error("Failed to process assets for Docker")
        return 1
    
    # Create deployment package
    deploy_path = prepare_deployment_package(results, args.name)
    
    logger.info(f"Docker asset package created: {deploy_path}")
    logger.info(f"- Static files: {len(results['static'])}")
    logger.info(f"- Images: {len(results['images'])}")
    logger.info(f"- Config files: {len(results['config'])}")
    logger.info(f"Deployment guide available at: {os.path.join(deploy_path, 'README.md')}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
