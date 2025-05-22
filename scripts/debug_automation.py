#!/usr/bin/env python3
"""
Debug wrapper for airth_news_automation.py that provides enhanced error handling.
"""
import os
import sys
import traceback
from datetime import datetime

# Create the debug directory
debug_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'debug')
os.makedirs(debug_dir, exist_ok=True)
debug_log = os.path.join(debug_dir, f"automation_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Redirect stdout and stderr to a log file
sys.stdout = open(debug_log, 'w')
sys.stderr = sys.stdout

try:
    print(f"Debug wrapper starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    print("\nImporting required modules...")
    import argparse
    print("argparse imported successfully")
    
    import logging
    print("logging imported successfully")
    
    from dotenv import load_dotenv
    print("dotenv imported successfully")
    
    # Attempt to import automation modules
    print("\nImporting automation modules...")
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scripts.airth_news_automation import main as automation_main
    print("Automation module imported successfully")
    
    print("\nExecuting automation with args:", sys.argv[1:])
    result = automation_main()
    print(f"\nAutomation completed with exit code: {result}")
    
except Exception as e:
    print(f"\n*** ERROR: AUTOMATION FAILED ***")
    print(f"Exception: {type(e).__name__}: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    
    # Check environment variables
    print("\nEnvironment variables:")
    print(f"OPENAI_API_KEY exists: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    print(f"WP_URL exists: {'Yes' if os.getenv('WP_URL') else 'No'}")
    print(f"WP_USERNAME exists: {'Yes' if os.getenv('WP_USERNAME') else 'No'}")
    print(f"WP_PASSWORD exists: {'Yes' if os.getenv('WP_PASSWORD') else 'No'}")
    
finally:
    print(f"\nDebug wrapper finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sys.stdout.close()
    
    # Reset stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
    print(f"Debug log written to {debug_log}")
