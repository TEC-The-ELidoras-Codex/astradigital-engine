#!/usr/bin/env python3
"""
Test script to verify OpenAI integration in the Airth News Automation system.
This script tests if the AirthNewsAutomation system properly uses the OpenAI API
for content generation.
"""
import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TestAirthLLM")

# Import the AirthNewsAutomation class
try:
    from scripts.airth_news_automation import AirthNewsAutomation
    from dotenv import load_dotenv
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    print(f"Error: Failed to import required modules. Make sure all dependencies are installed.")
    print(f"Details: {e}")
    sys.exit(1)

def test_openai_integration():
    """Test the OpenAI integration in the AirthNewsAutomation system."""
    logger.info("Creating AirthNewsAutomation instance...")
    
    # Load environment variables
    env_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))),
        'config',
        '.env')
    load_dotenv(env_path)
    
    # Create the automation instance
    automation = AirthNewsAutomation()
    
    # Check if the adapter was created
    if not hasattr(automation, 'airth') or not automation.airth:
        logger.error("AirthWPAdapter not initialized.")
        return False
    
    # Check if the OpenAI client is initialized
    if hasattr(automation.airth, 'llm_client') and automation.airth.llm_client:
        logger.info("OpenAI client initialized successfully.")
    else:
        logger.error("OpenAI client not initialized. Check the OPENAI_API_KEY environment variable.")
        return False
    
    # Test the _interact_llm method
    logger.info("Testing _interact_llm method with a simple prompt...")
    prompt = "Generate a short paragraph about artificial intelligence."
    
    result = automation.airth._interact_llm(prompt, max_tokens=150)
    
    if result and len(result) > 20 and "Error:" not in result and "Generated content based on" not in result:
        logger.info(f"Content generation successful. Generated {len(result)} characters.")
        logger.info("Sample content: " + result[:100] + ("..." if len(result) > 100 else ""))
        return True
    else:
        logger.error("Content generation failed or returned dummy content.")
        logger.error(f"Result: {result}")
        return False

if __name__ == "__main__":
    logger.info("Starting OpenAI integration test...")
    
    if test_openai_integration():
        logger.info("Test successful! The AirthNewsAutomation system is correctly using OpenAI API.")
        sys.exit(0)
    else:
        logger.error("Test failed. The AirthNewsAutomation system may not be correctly using the OpenAI API.")
        sys.exit(1)
