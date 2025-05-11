"""
AstraDigital Engine Main Entry Point
"""
import os
import sys
import logging
import argparse
from pathlib import Path

# Ensure the repository root is in sys.path
repo_root = Path(__file__).parent.parent
sys.path.append(str(repo_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            f"{repo_root}/logs/astradigital_{Path(__file__).stem}.log"
        )
    ]
)

logger = logging.getLogger("astradigital")

def main():
    """Main entry point for the AstraDigital Engine."""
    parser = argparse.ArgumentParser(description="AstraDigital Engine")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    if args.version:
        print("AstraDigital Engine v0.1.0")
        return
    
    logger.info("Starting AstraDigital Engine...")
    logger.info("For more information, visit https://elidorascodex.com")
    
    # Additional initialization code would go here

if __name__ == "__main__":
    main()
