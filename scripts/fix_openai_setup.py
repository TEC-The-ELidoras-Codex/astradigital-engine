#!/usr/bin/env python3
"""
OpenAI API Setup Fixer and Tester

This script helps you validate and fix your OpenAI API configuration.
It will:
1. Check if your OpenAI API key is properly set
2. Test the API key with a simple request
3. Update your .env file with the working key
4. Ensure the system is using the correct API version
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv, set_key
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OpenAISetupFixer")

def check_openai_installation():
    """Check if OpenAI is installed and install it if not."""
    try:
        import openai
        from openai import OpenAI
        logger.info("✅ OpenAI module is already installed.")
        return True
    except ImportError:
        logger.warning("❌ OpenAI module is not installed.")
        print("\nInstalling OpenAI module...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
        logger.info("✅ OpenAI module has been installed.")
        return True
    except Exception as e:
        logger.error(f"❌ Error checking OpenAI installation: {e}")
        return False

def test_openai_api_key(api_key):
    """Test if the OpenAI API key works."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="Hello, are you working? Just say yes or no.",
            max_tokens=10
        )
        response_text = response.choices[0].text.strip()
        logger.info(f"✅ API key works! Response: {response_text}")
        return True, response_text
    except Exception as e:
        logger.error(f"❌ API key test failed: {e}")
        return False, str(e)

def get_env_file_path():
    """Find the .env file path"""
    # Check for .env in config directory
    config_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', '.env')
    if os.path.exists(config_env):
        return config_env
        
    # Check for .env in project root
    root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(root_env):
        return root_env
        
    # Default to config directory
    return config_env

def update_env_file(api_key):
    """Update the .env file with the new API key."""
    try:
        env_file = get_env_file_path()
        env_dir = os.path.dirname(env_file)
        
        if not os.path.exists(env_dir):
            os.makedirs(env_dir)
            
        if not os.path.exists(env_file):
            # Create a new .env file
            with open(env_file, 'w') as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            logger.info(f"✅ Created new .env file at {env_file} with API key")
        else:
            # Update existing .env file
            set_key(env_file, "OPENAI_API_KEY", api_key)
            logger.info(f"✅ Updated API key in {env_file}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Failed to update .env file: {e}")
        return False

def check_current_api_key():
    """Check for the current API key in environment variables and .env file."""
    # Load from .env file
    env_file = get_env_file_path()
    load_dotenv(env_file)
    
    # Check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        logger.info("Found existing API key in environment")
        return api_key
    else:
        logger.warning("No API key found in environment")
        return None

def main():
    """Main function for checking and fixing OpenAI setup."""
    parser = argparse.ArgumentParser(description='OpenAI API Setup Fixer')
    parser.add_argument('--key', type=str, help='Provide an OpenAI API key to test and set')
    args = parser.parse_args()
    
    print("\n==== OpenAI Setup Fixer ====\n")
    
    # Step 1: Check OpenAI installation
    print("Step 1: Checking OpenAI installation...")
    if not check_openai_installation():
        print("Failed to install or verify OpenAI. Please install it manually with:")
        print("pip install openai")
        return 1
    
    # Step 2: Check if API key is already set and working
    current_api_key = check_current_api_key()
    api_key = args.key or current_api_key
    
    if not api_key:
        print("\nNo API key found or provided. Please provide your OpenAI API key:")
        api_key = input("API Key: ").strip()
    
    # Step 3: Test the API key
    print("\nStep 2: Testing API key...")
    success, response = test_openai_api_key(api_key)
    
    if not success:
        print("\n❌ The API key test failed.")
        print("Please check that you have a valid OpenAI API key and sufficient credits.")
        print("You can get an API key at: https://platform.openai.com/api-keys")
        
        if args.key or current_api_key != api_key:
            retry = input("\nWould you like to enter a different API key? (y/n): ")
            if retry.lower() == 'y':
                new_api_key = input("New API Key: ").strip()
                success, response = test_openai_api_key(new_api_key)
                if success:
                    api_key = new_api_key
    
    # Step 4: Update .env file if needed
    if success:
        print("\nStep 3: Updating configuration...")
        update_env_file(api_key)
        
        print("\n✅ SUCCESS! Your OpenAI API key has been verified and saved.")
        print("The system will now use this API key for all OpenAI requests.")
        print("\nIf you still encounter issues, try restarting your application")
        print("or check the OpenAI status page: https://status.openai.com/")
        return 0
    else:
        print("\n❌ Failed to verify a working API key.")
        print("Please check your OpenAI account and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
