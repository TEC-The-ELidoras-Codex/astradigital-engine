# TEC Testing Script for CI/CD on Windows
# Usage: .\run_ci_tests.ps1 [all|wordpress|integration|unit]

param (
    [Parameter(Position=0)]
    [ValidateSet("all", "wordpress", "integration", "unit")]
    [string]$TestType = "all"
)

# Create virtual environment if it doesn't exist
if (-not (Test-Path -Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
pip install pytest pytest-cov

# Create basic config for tests
Write-Host "Setting up test configuration..." -ForegroundColor Cyan
if (-not (Test-Path -Path "config\.env.ci")) {
    $configContent = @"
# CI Testing Environment
WP_URL=http://example.com/xmlrpc.php
WP_API_URL=http://example.com/wp-json
WP_USERNAME=test_user
WP_PASSWORD=test_password
WP_SITE_URL=http://example.com/xmlrpc.php
TEST_MODE=true
CI_MODE=true
"@
    $configContent | Out-File -FilePath "config\.env.ci" -Encoding utf8
}

# Run the tests
Write-Host "Running $TestType tests..." -ForegroundColor Green
switch ($TestType) {
    "wordpress" {
        python -m pytest tests\wordpress -v --no-header --cov=src.wordpress --cov-report=term
    }
    "integration" {
        python -m pytest tests\integration -v --no-header --cov=src --cov-report=term
    }
    "unit" {
        python -m pytest tests\unit -v --no-header --cov=src --cov-report=term
    }
    default {
        python -m pytest tests -v --no-header --cov=src --cov-report=term
    }
}

# Deactivate virtual environment
deactivate

Write-Host "Testing completed!" -ForegroundColor Green
