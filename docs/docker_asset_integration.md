# Docker Asset Integration Guide

## Overview

This guide explains how to use the TEC asset system for Docker container deployments. The system optimizes assets for Docker containers to minimize image size while maintaining quality.

## Asset Preparation Workflow

### 1. Directory Structure

Docker-specific assets are organized in the following structure:

```
assets/
├── source/            # Original, high-quality source files
├── optimized/
│   └── docker/        # Docker-optimized versions
│       ├── static/    # Web files (HTML, CSS, JS)
│       ├── images/    # Optimized images (primarily WebP)
│       └── config/    # Configuration files
└── deployment/
    └── docker/        # Ready-to-deploy Docker asset packages
```

### 2. Asset Optimization Process

The Docker asset optimization process focuses on:

1. **Size reduction**: Converting images to WebP format and resizing them
2. **Organization**: Structuring assets for container deployment
3. **Integration**: Providing snippets for Dockerfile and docker-compose.yml

## Using the Docker Asset Preparation Script

### Basic Usage

```powershell
# Navigate to the project directory
cd "C:\Users\Ghedd\TEC_CODE\astradigital-engine"

# Prepare assets for a specific Docker container
python assets/scripts/prepare_docker_assets.py --name "tec-api-server" --source "assets/source/images/logos"
```

### Arguments

- `--name`: Name of the Docker container (used for naming the package)
- `--source`: Source directory containing assets to prepare

### Output

The script creates a deployment package in `assets/deployment/docker/YYYYMMDD-container-name/` with:

1. **Optimized assets**: Static files, images, and configurations
2. **Dockerfile snippet**: Ready to paste into your Dockerfile
3. **Docker Compose snippet**: Ready to use with docker-compose
4. **README.md**: Documentation for the asset package

## Integrating Assets into Docker Containers

### Option 1: Using the Dockerfile Snippet

Copy the contents of `Dockerfile.snippet` into your Dockerfile:

```dockerfile
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

### Option 2: Using Docker Compose

Use the `docker-compose.snippet.yml` in your docker-compose.yml file:

```yaml
services:
  tec-api-server:
    build: .
    volumes:
      - ./assets/config:/app/config
    environment:
      - ASSET_PATH=/app
      - STATIC_PATH=/app/static
      - IMAGES_PATH=/app/images
      - CONFIG_PATH=/app/config
```

## Best Practices for Docker Assets

### Size Optimization

1. **Convert images to WebP**: Can reduce size by 30-50% compared to JPG/PNG
2. **Use appropriate dimensions**: Don't include images larger than needed
3. **Minify static files**: Compress HTML, CSS, and JavaScript
4. **Use multi-stage builds**: Keep build tools out of final image

### Development vs. Production

For development:
```yaml
volumes:
  - ./assets/source:/app/assets
```

For production:
```dockerfile
COPY ./assets/optimized/docker/ /app/assets/
```

### Asset Versioning

Use environment variables for asset versioning:

```dockerfile
ENV ASSET_VERSION=2.1.0
ENV ASSET_PATH=/app/assets/$ASSET_VERSION
```

## Monitoring and Managing Asset Size

To analyze the impact of assets on your Docker image size:

```powershell
# Build image
docker build -t tec-app:latest .

# Analyze layers
docker history tec-app:latest
```

Look for large layers and consider further optimization if needed.

## Example Implementation

Complete Dockerfile example with asset integration:

```dockerfile
# Build stage
FROM node:14 AS build
WORKDIR /build
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Final stage
FROM python:3.9-slim
WORKDIR /app

# Copy application code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/

# Copy optimized assets from the Docker asset package
COPY assets/deployment/docker/20250524-tec-api/static/ /app/static/
COPY assets/deployment/docker/20250524-tec-api/images/ /app/images/
COPY assets/deployment/docker/20250524-tec-api/config/ /app/config/

# Environment variables
ENV ASSET_PATH=/app
ENV STATIC_PATH=/app/static
ENV IMAGES_PATH=/app/images
ENV CONFIG_PATH=/app/config

# Expose port and start application
EXPOSE 8000
CMD ["python", "app.py"]
```

## Troubleshooting

### Common Issues

1. **Container size too large**: Check image sizes and optimize larger assets
2. **Assets not found in container**: Verify paths and COPY commands in Dockerfile
3. **Performance issues**: Consider using volumes for development, embedded assets for production
