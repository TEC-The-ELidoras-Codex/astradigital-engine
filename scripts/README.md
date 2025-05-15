# TEC Office Suite Utility Scripts

This directory contains utility scripts for managing and testing the TEC Office Suite Docker environment.

> **Note:** Formal test scripts have been moved to the `/tests` directory. Please use the new pytest-based testing framework for running tests.
> 
> Legacy test scripts (older versions) have been moved to the `/scripts/Tests` directory and are kept for reference purposes.

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

# Scripts

## Purpose

The `scripts` folder contains all scripts used for automation, data processing, and other functionalities in TEC.

## Subfolder Structure

- **airth_blog_post.py**: Script for automating blog posts.
- **airth_news_automation.py**: Main script for news automation.
- **fix_indentation.ps1**: PowerShell script for fixing indentation issues.
- **run_tests.py**: Python script for running tests.

## Naming Conventions

- Use descriptive names with snake_case for Python scripts (e.g., `data_processor.py`).
- Use Verb-Noun naming convention for PowerShell scripts (e.g., `Fix-Indentation.ps1`).

## Metadata Standards

- Include docstrings in Python scripts to describe functionality.
- Use comment-based help in PowerShell scripts.

## Notes

- Test all scripts in a development environment before deploying.
- Follow coding standards outlined in the TEC AI Directive.
