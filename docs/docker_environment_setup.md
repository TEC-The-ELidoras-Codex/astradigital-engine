# Docker Environment Setup for TEC Office Suite

This guide will help you set up the Docker environment for the TEC Office Suite, including proper handling of environment variables and security best practices.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- Git repository cloned locally

## Secure Setup Process

### 1. Create and Configure Environment Variables

First, you need to set up your environment variables in a `.env` file. This file contains sensitive information and **should never be committed to your repository**.

#### Using the Setup Script (Recommended)

Run the appropriate setup script for your operating system:

**Windows (PowerShell):**
```powershell
cd scripts
.\setup_env.ps1
```

**Linux/macOS:**
```bash
cd scripts
bash ./setup_env.sh
```

The script will:
- Create a `.env` file based on the `.env.template`
- Guide you through entering your credentials
- Set appropriate file permissions to secure your secrets

#### Manual Setup

Alternatively, you can:
1. Copy the template file: `cp config/.env.template config/.env`
2. Edit the `.env` file with your favorite text editor
3. Fill in all required credentials

### 2. Essential Environment Variables

At minimum, you need to configure:

- **WordPress Credentials:**
  - `WP_URL` - Your WordPress site URL
  - `WP_USERNAME` - Your WordPress username
  - `WP_PASSWORD` - Your WordPress application password (create in WordPress admin)
  - `WP_XMLRPC_PATH` - Path to WordPress XML-RPC endpoint (usually `/xmlrpc.php`)

- **AI Provider API Keys:**
  - `OPENAI_API_KEY` - Your OpenAI API key
  - `ANTHROPIC_API_KEY` - Your Anthropic API key (optional)

### 3. Testing WordPress Connectivity

Before building the Docker container, verify that your WordPress credentials work:

```powershell
python scripts/test_wordpress.py
```

This will test your WordPress configuration by creating a draft post.

### 4. Building and Running the Docker Container

Once you've set up your environment variables and verified your WordPress connection, you can build and run the Docker container:

**Build the Docker image:**
```powershell
docker build -t tec_office:latest .
```

**Start the Docker container:**
```powershell
docker-compose up -d
```

**Check if the container is running:**
```powershell
docker ps
```

### 5. Testing the Airth Agent WordPress Posting

To test Airth's ability to post the roadmap article:

```powershell
python scripts/post_roadmap_article.py
```

This will generate a draft article in your WordPress site.

## Security Best Practices

### Protecting Sensitive Information

1. **Never commit credentials to Git**:
   - Always use `.env` files for sensitive information
   - Make sure `.env` is in your `.gitignore` file
   - Use `.env.template` or `.env.example` with placeholder values

2. **Fix leaked credentials immediately**:
   - If credentials were previously committed to Git:
     - Revoke and rotate all leaked API keys and passwords
     - Use [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) to remove sensitive data from Git history

3. **Set restrictive permissions**:
   - Ensure `.env` file permissions are set to be readable only by the owner

4. **Use environment variables in Docker**:
   - Pass credentials through environment variables, not by building them into the image
   - The `docker-compose.yml` file should reference variables from the host's `.env` file

### GitHub Security

1. **Enable branch protection**:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Use pre-commit hooks to check for sensitive information

2. **Use GitHub Secrets**:
   - For CI/CD workflows, use GitHub Secrets instead of hardcoded values

## Troubleshooting

### Common Issues

1. **Docker container fails to start**:
   - Check Docker logs: `docker logs tec_office`
   - Verify all required environment variables are set

2. **WordPress posting fails**:
   - Run the WordPress test script to verify credentials
   - Check if your WordPress site has XML-RPC enabled
   - Verify application password is correctly configured

3. **API authentication fails**:
   - Check that API keys are correctly formatted
   - Verify API subscription is active and has sufficient quota

### Getting Help

If you continue to experience issues:
1. Check the logs in the `logs/` directory
2. Review the Docker container logs
3. Create an issue in the GitHub repository with detailed error information
