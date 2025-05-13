#!/usr/bin/env python3
"""
Test runner for The Elidoras Codex.
This script provides a convenient wrapper around pytest for running TEC tests.
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

# Ensure we're running from the project root
PROJECT_ROOT = Path(__file__).parent.parent
if not (PROJECT_ROOT / 'tests').exists():
    print("Error: This script must be run from the project root directory.")
    sys.exit(1)

def main():
    """Parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Run tests for The Elidoras Codex")
    parser.add_argument(
        'test_type',
        nargs='?',
        choices=['all', 'wordpress', 'integration', 'unit'],
        default='all',
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Enable verbose output"
    )
    parser.add_argument(
        '--collect-only',
        action='store_true',
        help="Only collect tests, don't run them"
    )
    parser.add_argument(
        '--junit-xml',
        help="Generate JUnit XML report"
    )

    args = parser.parse_args()
    
    # Determine the test path
    if args.test_type == 'all':
        test_path = 'tests'
    else:
        test_path = f'tests/{args.test_type}'
    
    # Build pytest command
    pytest_args = ['python', '-m', 'pytest', test_path]
    
    if args.verbose:
        pytest_args.append('-v')
    
    if args.collect_only:
        pytest_args.append('--collect-only')
    
    if args.junit_xml:
        pytest_args.extend(['--junit-xml', args.junit_xml])
    
    # Print command for debugging purposes
    print(f"Running: {' '.join(pytest_args)}")
    
    # Execute pytest
    try:
        result = subprocess.run(pytest_args, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
