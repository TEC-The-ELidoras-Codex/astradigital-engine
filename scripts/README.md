# TEC Office Suite Utility Scripts

This directory contains utility scripts for managing and testing the TEC Office Suite Docker environment.

## Environment Setup

### `setup_env.ps1` (Windows)
PowerShell script to securely create and configure the `.env` file with your credentials.

```powershell
# Run from the scripts directory
.\setup_env.ps1
```

### `setup_env.sh` (Linux/macOS)
Bash script to securely create and configure the `.env` file with your credentials.

```bash
# Run from the scripts directory
bash ./setup_env.sh
# OR
chmod +x ./setup_env.sh
./setup_env.sh
```

## WordPress Testing

### `test_wordpress.py`
Tests WordPress connectivity by checking credentials and attempting to create a draft post.

```powershell
# Run from the scripts directory
python test_wordpress.py
```

### `enhanced_wordpress_test.py`
A more comprehensive WordPress test that validates configuration, categories, and posting abilities.

### `initialize_wordpress.py`
Initializes WordPress with default categories and tags for TEC content.

## Docker Management

### `docker_manager.py`
Utility script for managing Docker containers and images for TEC Office Suite.

## Content Creation

### `post_roadmap_article.py`
Script to post the TEC AI Employee roadmap article to WordPress via Airth.

```powershell
# Run from the scripts directory
python post_roadmap_article.py
```

### `airth_blog_post.py`
Creates a blog post using Airth's content generation capabilities.

## Demo and Testing

### `airth_timer_demo.py`
Demonstrates Airth's timer functionality.

### `run_airth_mvp.py`
Runs a minimal viable product version of Airth for testing.

## Deployment

### `deploy_to_hf_space.bat` (Windows) / `deploy_to_hf_space.sh` (Linux/macOS)
Scripts for deploying the TEC Office Suite to a Hugging Face Space.
