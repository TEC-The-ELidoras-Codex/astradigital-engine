#!/usr/bin/env python3
"""
Docker setup and testing script for TEC_OFFICE_REPO.
This script helps manage Docker containers for the project.
"""
import os
import sys
import argparse
import logging
import subprocess
import platform
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.Docker")

# Docker command prefix based on OS
DOCKER_CMD = "docker" if platform.system() != "Windows" else "docker"
DOCKER_COMPOSE_CMD = "docker-compose" if platform.system() != "Windows" else "docker-compose"

def check_docker_installed() -> Tuple[bool, str]:
    """
    Check if Docker is installed.
    
    Returns:
        Tuple of (is_installed, version)
    """
    try:
        result = subprocess.run(
            [DOCKER_CMD, "--version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        logger.info(f"Docker is installed: {result.stdout.strip()}")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError:
        logger.error("Docker command failed. Is Docker installed and running?")
        return False, ""
    except FileNotFoundError:
        logger.error("Docker command not found. Please install Docker.")
        return False, ""

def check_docker_compose_installed() -> Tuple[bool, str]:
    """
    Check if Docker Compose is installed.
    
    Returns:
        Tuple of (is_installed, version)
    """
    try:
        result = subprocess.run(
            [DOCKER_COMPOSE_CMD, "--version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        logger.info(f"Docker Compose is installed: {result.stdout.strip()}")
        return True, result.stdout.strip()
    except subprocess.CalledProcessError:
        logger.error("Docker Compose command failed.")
        return False, ""
    except FileNotFoundError:
        logger.error("Docker Compose command not found.")
        return False, ""

def build_image() -> bool:
    """
    Build the Docker image.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("Building Docker image...")
        result = subprocess.run(
            [DOCKER_CMD, "build", "-t", "tec-office:latest", "."],
            check=True
        )
        logger.info("Docker image built successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Docker build failed: {e}")
        return False

def run_docker_compose_up(detached: bool = True) -> bool:
    """
    Run docker-compose up.
    
    Args:
        detached: Run in detached mode
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = [DOCKER_COMPOSE_CMD, "up"]
        if detached:
            cmd.append("-d")
        
        logger.info(f"Running {' '.join(cmd)}...")
        result = subprocess.run(cmd, check=True)
        logger.info("Docker Compose started successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Docker Compose failed: {e}")
        return False

def run_docker_compose_down() -> bool:
    """
    Run docker-compose down.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("Running docker-compose down...")
        result = subprocess.run(
            [DOCKER_COMPOSE_CMD, "down"],
            check=True
        )
        logger.info("Docker Compose stopped successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Docker Compose down failed: {e}")
        return False

def check_container_status(container_name: str = "tec_office") -> Dict[str, Any]:
    """
    Check the status of a container.
    
    Args:
        container_name: Name of the container
        
    Returns:
        Dictionary with container status information
    """
    try:
        result = subprocess.run(
            [DOCKER_CMD, "ps", "-a", "--filter", f"name={container_name}", "--format", "{{.Names}}|{{.Status}}|{{.Ports}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout.strip()
        if not output:
            logger.warning(f"Container {container_name} not found")
            return {"exists": False}
        
        parts = output.split("|", 2)
        name = parts[0] if len(parts) > 0 else ""
        status = parts[1] if len(parts) > 1 else ""
        ports = parts[2] if len(parts) > 2 else ""
        
        is_running = status.lower().startswith("up")
        
        logger.info(f"Container {name} status: {status}")
        return {
            "exists": True,
            "name": name,
            "status": status,
            "is_running": is_running,
            "ports": ports
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check container status: {e}")
        return {"exists": False, "error": str(e)}

def view_logs(container_name: str = "tec_office", tail: int = 100) -> str:
    """
    View the logs of a container.
    
    Args:
        container_name: Name of the container
        tail: Number of lines to show
        
    Returns:
        Container logs
    """
    try:
        result = subprocess.run(
            [DOCKER_CMD, "logs", f"--tail={tail}", container_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        logs = result.stdout
        logger.info(f"Retrieved {tail} lines of logs from {container_name}")
        return logs
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to view container logs: {e}")
        return f"Error viewing logs: {e}"

def run_tests_in_container(container_name: str = "tec_office", test_path: str = "tests/") -> str:
    """
    Run tests inside the container.
    
    Args:
        container_name: Name of the container
        test_path: Path to tests in the container
        
    Returns:
        Test output
    """
    try:
        result = subprocess.run(
            [DOCKER_CMD, "exec", container_name, "python", "-m", "pytest", test_path, "-v"],
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout
        logger.info(f"Tests completed in {container_name}")
        return output
    except subprocess.CalledProcessError as e:
        logger.error(f"Tests failed in container: {e}")
        return f"Tests failed: {e}\n\nOutput:\n{e.stdout}\n\nErrors:\n{e.stderr}"

def main():
    """Main function to run the script from the command line."""
    parser = argparse.ArgumentParser(description='Docker Management for TEC_OFFICE_REPO')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check if Docker is installed')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build the Docker image')
    
    # Up command
    up_parser = subparsers.add_parser('up', help='Start containers with docker-compose up')
    up_parser.add_argument('--detached', '-d', action='store_true', help='Run in detached mode')
    
    # Down command
    down_parser = subparsers.add_parser('down', help='Stop containers with docker-compose down')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check container status')
    status_parser.add_argument('--name', default='tec_office', help='Container name')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='View container logs')
    logs_parser.add_argument('--name', default='tec_office', help='Container name')
    logs_parser.add_argument('--tail', type=int, default=100, help='Number of lines to show')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests in the container')
    test_parser.add_argument('--name', default='tec_office', help='Container name')
    test_parser.add_argument('--path', default='tests/', help='Path to tests')
    
    args = parser.parse_args()
    
    if args.command == 'check':
        docker_installed, docker_version = check_docker_installed()
        compose_installed, compose_version = check_docker_compose_installed()
        
        if docker_installed and compose_installed:
            print("✅ Docker environment is ready to use")
            print(f"Docker: {docker_version}")
            print(f"Docker Compose: {compose_version}")
            sys.exit(0)
        else:
            print("❌ Docker environment is not properly set up")
            sys.exit(1)
    elif args.command == 'build':
        success = build_image()
        if success:
            print("✅ Docker image built successfully")
            sys.exit(0)
        else:
            print("❌ Failed to build Docker image")
            sys.exit(1)
    elif args.command == 'up':
        success = run_docker_compose_up(args.detached)
        if success:
            print("✅ Docker Compose started successfully")
            # Check container status after starting
            time.sleep(3)  # Give it a moment to start
            status = check_container_status()
            if status.get("is_running"):
                print(f"Container is running: {status.get('name')}")
                print(f"Status: {status.get('status')}")
                print(f"Ports: {status.get('ports')}")
            sys.exit(0)
        else:
            print("❌ Failed to start Docker Compose")
            sys.exit(1)
    elif args.command == 'down':
        success = run_docker_compose_down()
        if success:
            print("✅ Docker Compose stopped successfully")
            sys.exit(0)
        else:
            print("❌ Failed to stop Docker Compose")
            sys.exit(1)
    elif args.command == 'status':
        status = check_container_status(args.name)
        if status.get("exists"):
            print(f"Container: {status.get('name')}")
            print(f"Status: {status.get('status')}")
            print(f"Running: {'Yes' if status.get('is_running') else 'No'}")
            print(f"Ports: {status.get('ports')}")
            sys.exit(0 if status.get("is_running") else 1)
        else:
            print(f"❌ Container {args.name} not found")
            sys.exit(1)
    elif args.command == 'logs':
        logs = view_logs(args.name, args.tail)
        print(logs)
    elif args.command == 'test':
        output = run_tests_in_container(args.name, args.path)
        print(output)
        sys.exit(0 if "failed" not in output.lower() else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
