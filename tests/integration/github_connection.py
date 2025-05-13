#!/usr/bin/env python3
"""
GitHub Connection Script for TEC_OFFICE_REPO.
This script provides utilities for interacting with GitHub repositories.
"""
import os
import sys
import argparse
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.GitHub")

# Load environment variables
config_env_path = os.path.join('config', '.env')
if os.path.exists(config_env_path):
    load_dotenv(config_env_path)
else:
    logger.warning("Warning: .env file not found in config directory")

# Try to import the GitHub API library
GITHUB_AVAILABLE = False
try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    logger.error("PyGithub library not found. Please install it with 'pip install PyGithub'")


def connect_to_github() -> Optional[Any]:
    """
    Connect to GitHub using the token from environment variables.
    
    Returns:
        GitHub client instance if successful, None otherwise
    """
    if not GITHUB_AVAILABLE:
        logger.error("Cannot connect to GitHub: PyGithub library not available")
        return None
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GitHub token not found in environment variables")
        return None
    
    try:
        github = Github(github_token)
        user = github.get_user()
        logger.info(f"Connected to GitHub as {user.login}")
        return github
    except Exception as e:
        logger.error(f"Failed to connect to GitHub: {e}")
        return None


def create_repository(name: str, description: str, private: bool = False) -> Dict[str, Any]:
    """
    Create a new GitHub repository.
    
    Args:
        name: Repository name
        description: Repository description
        private: Whether the repository should be private
        
    Returns:
        Dictionary with repository information
    """
    if not GITHUB_AVAILABLE:
        return {"success": False, "error": "PyGithub library not available"}
    
    github = connect_to_github()
    if not github:
        return {"success": False, "error": "Failed to connect to GitHub"}
    
    try:
        user = github.get_user()
        repo = user.create_repo(
            name=name,
            description=description,
            private=private,
            has_issues=True,
            has_projects=True,
            has_wiki=True
        )
        logger.info(f"Created repository: {repo.html_url}")
        return {
            "success": True,
            "name": repo.name,
            "full_name": repo.full_name,
            "url": repo.html_url,
            "clone_url": repo.clone_url,
            "ssh_url": repo.ssh_url,
            "private": repo.private
        }
    except Exception as e:
        logger.error(f"Failed to create repository: {e}")
        return {"success": False, "error": str(e)}


def check_repository_exists(owner: str, name: str) -> Dict[str, Any]:
    """
    Check if a repository exists.
    
    Args:
        owner: Repository owner/organization
        name: Repository name
        
    Returns:
        Dictionary with repository information
    """
    if not GITHUB_AVAILABLE:
        return {"success": False, "error": "PyGithub library not available"}
    
    github = connect_to_github()
    if not github:
        return {"success": False, "error": "Failed to connect to GitHub"}
    
    try:
        repo = github.get_repo(f"{owner}/{name}")
        logger.info(f"Repository exists: {repo.html_url}")
        return {
            "success": True,
            "exists": True,
            "name": repo.name,
            "full_name": repo.full_name,
            "url": repo.html_url,
            "clone_url": repo.clone_url,
            "ssh_url": repo.ssh_url,
            "private": repo.private
        }
    except GithubException as e:
        if e.status == 404:
            logger.info(f"Repository {owner}/{name} does not exist")
            return {"success": True, "exists": False}
        else:
            logger.error(f"GitHub API error: {e}")
            return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Failed to check repository: {e}")
        return {"success": False, "error": str(e)}


def main():
    """Main function to run the script from the command line."""
    parser = argparse.ArgumentParser(description='GitHub Repository Management Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Create repository command
    create_parser = subparsers.add_parser('create', help='Create a new repository')
    create_parser.add_argument('name', help='Repository name')
    create_parser.add_argument('--description', '-d', help='Repository description')
    create_parser.add_argument('--private', '-p', action='store_true', help='Make repository private')
    
    # Check repository command
    check_parser = subparsers.add_parser('check', help='Check if a repository exists')
    check_parser.add_argument('owner', help='Repository owner/organization')
    check_parser.add_argument('name', help='Repository name')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        result = create_repository(args.name, args.description or "", args.private)
        if result["success"]:
            print(f"Repository created: {result['url']}")
        else:
            print(f"Failed to create repository: {result['error']}")
            sys.exit(1)
    elif args.command == 'check':
        result = check_repository_exists(args.owner, args.name)
        if result["success"]:
            if result.get("exists"):
                print(f"Repository exists: {result['url']}")
            else:
                print(f"Repository does not exist: {args.owner}/{args.name}")
        else:
            print(f"Failed to check repository: {result['error']}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
