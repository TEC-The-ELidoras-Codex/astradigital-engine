# GitHub Repository Settings Guide

This document outlines recommended GitHub repository settings to enhance security and prevent the accidental exposure of sensitive information.

## Branch Protection Rules

To set up branch protection rules:

1. Go to your repository on GitHub
2. Click on "Settings" > "Branches" > "Add rule"
3. Configure the following settings:

### Main Branch Protection

- **Branch name pattern**: `main` (or your default branch name)
- **Require pull request reviews before merging**: ✓
  - **Required approvals**: 1 (or more)
  - **Dismiss stale pull request approvals when new commits are pushed**: ✓
  - **Require review from Code Owners**: Optional
- **Require status checks to pass before merging**: ✓
  - Search for and select relevant CI checks
- **Require signed commits**: ✓
- **Include administrators**: ✓
- **Allow force pushes**: ✗ (disabled)
- **Allow deletions**: ✗ (disabled)

## Secret Scanning

Enable GitHub secret scanning to automatically detect accidentally committed credentials:

1. Go to "Settings" > "Code security and analysis"
2. Enable "Secret scanning"
3. Enable "Push protection" to block commits containing secrets

## Security Policies

Create a security policy:

1. Create a file at `.github/SECURITY.md`
2. Include guidelines on reporting security vulnerabilities
3. Outline the process for handling security issues

## Managing Secrets in GitHub

Use GitHub Secrets for CI/CD:

1. Go to "Settings" > "Secrets and variables" > "Actions"
2. Add required secrets for workflows (e.g., `OPENAI_API_KEY`, `WP_PASSWORD`)
3. Reference these in GitHub Actions workflows like:
   ```yaml
   env:
     OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
   ```

## Using .gitignore

Ensure sensitive files are properly excluded:

1. Verify `.gitignore` includes `.env` and other configuration files
2. Use `.env.example` templates instead of real configuration files
3. Run `git check-ignore .env` to verify files are properly ignored

## Regular Audits

Schedule regular repository audits:

1. Check Git history for accidental commits of sensitive information
2. Verify protection rules are still applied appropriately
3. Rotate API keys and credentials regularly

## What to Do If Secrets Are Exposed

If sensitive information is accidentally committed:

1. Revoke and rotate the exposed credentials immediately
2. Remove the sensitive data from Git history using the `clean_git_history.ps1` script
3. Notify all contributors to pull fresh copies of the repository
4. Document the incident and update security practices
