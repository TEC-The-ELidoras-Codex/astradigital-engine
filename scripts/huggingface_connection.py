#!/usr/bin/env python3
"""
Hugging Face Space Connection Script for TEC_OFFICE_REPO.
This script provides utilities for managing the connection to Hugging Face Spaces.
"""
import os
import sys
import argparse
import logging
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.HuggingFace")

# Load environment variables
config_env_path = os.path.join('config', '.env')
if os.path.exists(config_env_path):
    load_dotenv(config_env_path)
else:
    logger.warning("Warning: .env file not found in config directory")

# Try to import the Hugging Face Hub library
HF_AVAILABLE = False
try:
    from huggingface_hub import HfApi, SpaceStage, SpaceHardware, SpaceSdk, login
    from huggingface_hub.utils import RepositoryNotFoundError
    HF_AVAILABLE = True
except ImportError:
    logger.error("Hugging Face Hub library not found. Please install it with 'pip install huggingface_hub'")


def login_to_huggingface() -> bool:
    """
    Log in to Hugging Face Hub using token from environment variables.
    
    Returns:
        True if login successful, False otherwise
    """
    if not HF_AVAILABLE:
        logger.error("Cannot log in to Hugging Face: huggingface_hub library not available")
        return False
    
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        logger.error("Hugging Face token not found in environment variables")
        return False
    
    try:
        login(token=hf_token)
        logger.info("Logged in to Hugging Face successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to log in to Hugging Face: {e}")
        return False


def check_space_exists(username: str, space_name: str) -> Dict[str, Any]:
    """
    Check if a Hugging Face Space exists.
    
    Args:
        username: Hugging Face username or organization
        space_name: Space name
        
    Returns:
        Dictionary with space information
    """
    if not HF_AVAILABLE:
        return {"success": False, "error": "huggingface_hub library not available"}
    
    if not login_to_huggingface():
        return {"success": False, "error": "Failed to log in to Hugging Face"}
    
    api = HfApi()
    space_id = f"{username}/{space_name}"
    
    try:
        space_info = api.space_info(space_id)
        logger.info(f"Space exists: {space_info.name}")
        return {
            "success": True,
            "exists": True,
            "name": space_info.name,
            "id": space_info.id,
            "url": f"https://huggingface.co/spaces/{space_id}",
            "sdk": space_info.sdk.value if space_info.sdk else None,
            "hardware": space_info.hardware.value if space_info.hardware else None
        }
    except RepositoryNotFoundError:
        logger.info(f"Space does not exist: {space_id}")
        return {"success": True, "exists": False, "id": space_id}
    except Exception as e:
        logger.error(f"Failed to check space: {e}")
        return {"success": False, "error": str(e)}


def create_space(username: str, space_name: str, sdk: str = "gradio", 
               hardware: str = "cpu-basic", private: bool = False) -> Dict[str, Any]:
    """
    Create a new Hugging Face Space.
    
    Args:
        username: Hugging Face username or organization
        space_name: Space name
        sdk: Space SDK (gradio, streamlit, etc.)
        hardware: Hardware tier
        private: Whether the space should be private
        
    Returns:
        Dictionary with space information
    """
    if not HF_AVAILABLE:
        return {"success": False, "error": "huggingface_hub library not available"}
    
    if not login_to_huggingface():
        return {"success": False, "error": "Failed to log in to Hugging Face"}
    
    api = HfApi()
    space_id = f"{username}/{space_name}"
    
    # Map SDK and hardware strings to enum values
    sdk_map = {
        "gradio": SpaceSdk.GRADIO,
        "streamlit": SpaceSdk.STREAMLIT,
        "static": SpaceSdk.STATIC,
        "docker": SpaceSdk.DOCKER
    }
    
    hardware_map = {
        "cpu-basic": SpaceHardware.CPU_BASIC,
        "cpu-upgrade": SpaceHardware.CPU_UPGRADE,
        "t4-small": SpaceHardware.T4_SMALL,
        "t4-medium": SpaceHardware.T4_MEDIUM
    }
    
    try:
        sdk_enum = sdk_map.get(sdk.lower(), SpaceSdk.GRADIO)
        hardware_enum = hardware_map.get(hardware.lower(), SpaceHardware.CPU_BASIC)
        
        repo_url = api.create_repo(
            repo_id=space_id,
            repo_type="space",
            space_sdk=sdk_enum,
            space_hardware=hardware_enum,
            private=private
        )
        
        logger.info(f"Space created: {repo_url}")
        return {
            "success": True,
            "url": repo_url,
            "id": space_id,
            "sdk": sdk,
            "hardware": hardware,
            "private": private
        }
    except Exception as e:
        logger.error(f"Failed to create space: {e}")
        return {"success": False, "error": str(e)}


def upload_to_space(username: str, space_name: str, files: List[str] = None) -> Dict[str, Any]:
    """
    Upload files to a Hugging Face Space.
    
    Args:
        username: Hugging Face username or organization
        space_name: Space name
        files: List of files or directories to upload (defaults to all files in the current directory)
        
    Returns:
        Dictionary with upload information
    """
    if not HF_AVAILABLE:
        return {"success": False, "error": "huggingface_hub library not available"}
    
    if not login_to_huggingface():
        return {"success": False, "error": "Failed to log in to Hugging Face"}
    
    api = HfApi()
    space_id = f"{username}/{space_name}"
    
    try:
        # Check if space exists
        space_exists = check_space_exists(username, space_name)
        if not space_exists.get("success"):
            return space_exists
        
        if not space_exists.get("exists"):
            logger.error(f"Space does not exist: {space_id}")
            return {"success": False, "error": f"Space does not exist: {space_id}"}
        
        # If no files specified, upload all files in the current directory
        if not files:
            folder_path = "."
            ignore_patterns = [".git*", "venv", "__pycache__", "*.pyc", ".env"]
            api.upload_folder(
                folder_path=folder_path,
                repo_id=space_id,
                repo_type="space",
                ignore_patterns=ignore_patterns
            )
            logger.info(f"Uploaded all files to {space_id}")
        else:
            # Upload specified files
            uploaded_files = []
            for file_path in files:
                path = Path(file_path)
                if path.is_dir():
                    api.upload_folder(
                        folder_path=str(path),
                        repo_id=space_id,
                        repo_type="space",
                        path_in_repo=path.name
                    )
                    uploaded_files.append(f"{path.name}/*")
                else:
                    api.upload_file(
                        path_or_fileobj=str(path),
                        path_in_repo=path.name,
                        repo_id=space_id,
                        repo_type="space"
                    )
                    uploaded_files.append(path.name)
            logger.info(f"Uploaded files to {space_id}: {', '.join(uploaded_files)}")
        
        return {
            "success": True,
            "id": space_id,
            "url": f"https://huggingface.co/spaces/{space_id}"
        }
    except Exception as e:
        logger.error(f"Failed to upload to space: {e}")
        return {"success": False, "error": str(e)}


def main():
    """Main function to run the script from the command line."""
    parser = argparse.ArgumentParser(description='Hugging Face Space Management Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Check space command
    check_parser = subparsers.add_parser('check', help='Check if a space exists')
    check_parser.add_argument('username', help='Hugging Face username or organization')
    check_parser.add_argument('space_name', help='Space name')
    
    # Create space command
    create_parser = subparsers.add_parser('create', help='Create a new space')
    create_parser.add_argument('username', help='Hugging Face username or organization')
    create_parser.add_argument('space_name', help='Space name')
    create_parser.add_argument('--sdk', choices=['gradio', 'streamlit', 'static', 'docker'], 
                             default='gradio', help='Space SDK')
    create_parser.add_argument('--hardware', choices=['cpu-basic', 'cpu-upgrade', 't4-small', 't4-medium'], 
                             default='cpu-basic', help='Hardware tier')
    create_parser.add_argument('--private', action='store_true', help='Make space private')
    
    # Upload to space command
    upload_parser = subparsers.add_parser('upload', help='Upload files to a space')
    upload_parser.add_argument('username', help='Hugging Face username or organization')
    upload_parser.add_argument('space_name', help='Space name')
    upload_parser.add_argument('--files', nargs='*', help='Files to upload (default: all files in current directory)')
    
    args = parser.parse_args()
    
    if args.command == 'check':
        result = check_space_exists(args.username, args.space_name)
        if result["success"]:
            if result.get("exists"):
                print(f"Space exists: {result['url']}")
                print(f"SDK: {result.get('sdk')}")
                print(f"Hardware: {result.get('hardware')}")
            else:
                print(f"Space does not exist: {result['id']}")
        else:
            print(f"Failed to check space: {result['error']}")
            sys.exit(1)
    elif args.command == 'create':
        result = create_space(args.username, args.space_name, args.sdk, args.hardware, args.private)
        if result["success"]:
            print(f"Space created: {result['url']}")
            print(f"SDK: {result['sdk']}")
            print(f"Hardware: {result['hardware']}")
        else:
            print(f"Failed to create space: {result['error']}")
            sys.exit(1)
    elif args.command == 'upload':
        result = upload_to_space(args.username, args.space_name, args.files)
        if result["success"]:
            print(f"Files uploaded to: {result['url']}")
        else:
            print(f"Failed to upload files: {result['error']}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
