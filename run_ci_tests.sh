#!/bin/bash
# TEC Testing Script for CI/CD
# Usage: ./run_ci_tests.sh [wordpress|integration|unit|all]

set -e

# Default test type is all
TEST_TYPE=${1:-all}

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install pytest pytest-cov

# Create basic config for tests
echo "Setting up test configuration..."
if [ ! -f "config/.env.ci" ]; then
  cat > config/.env.ci << EOF
# CI Testing Environment
WP_URL=http://example.com/xmlrpc.php
WP_API_URL=http://example.com/wp-json
WP_USERNAME=test_user
WP_PASSWORD=test_password
WP_SITE_URL=http://example.com/xmlrpc.php
TEST_MODE=true
CI_MODE=true
EOF
fi

# Run the tests
echo "Running $TEST_TYPE tests..."
case $TEST_TYPE in
  wordpress)
    python -m pytest tests/wordpress -v --no-header --cov=src.wordpress --cov-report=term
    ;;
  integration)
    python -m pytest tests/integration -v --no-header --cov=src --cov-report=term
    ;;
  unit)
    python -m pytest tests/unit -v --no-header --cov=src --cov-report=term
    ;;
  all|*)
    python -m pytest tests -v --no-header --cov=src --cov-report=term
    ;;
esac

# Deactivate virtual environment
deactivate

echo "Testing completed!"
