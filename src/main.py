"""
AstraDigital Engine Main Entry Point
With Unity & MetaQuest VR Development Support
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

def check_unity_installation():
    """Check if Unity is installed & configured."""
    # Unity installation paths by platform
    if sys.platform == "win32":
        unity_paths = [
            "C:\\Program Files\\Unity\\Hub\\Editor",
            "C:\\Program Files\\Unity"
        ]
    elif sys.platform == "darwin":  # macOS
        unity_paths = [
            "/Applications/Unity/Hub/Editor",
            "/Applications/Unity"
        ]
    else:  # Linux
        unity_paths = [
            "/opt/unity/editor",
            "~/Unity/Hub/Editor"
        ]
    
    for path in unity_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            logger.info(f"Unity installation found at: {expanded_path}")
            return expanded_path
    
    logger.warning("Unity installation not found. Install Unity Hub for full VR development capabilities.")
    return None

def check_metaquest_sdk():
    """Check for MetaQuest SDK installation."""
    # MetaQuest SDK expected paths
    if sys.platform == "win32":
        sdk_paths = [
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Oculus", "SDK"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Oculus", "SDK")
        ]
    else:
        sdk_paths = [
            "~/Library/Application Support/Oculus/SDK",  # macOS
            "~/.local/share/Oculus/SDK"  # Linux
        ]
    
    for path in sdk_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            logger.info(f"MetaQuest SDK found at: {expanded_path}")
            return expanded_path
    
    logger.warning("MetaQuest SDK not found. Install the Oculus SDK for MetaQuest development.")
    return None

def setup_vr_environment():
    """Configure the VR development environment."""
    logger.info("Setting up VR development environment...")
    unity_path = check_unity_installation()
    metaquest_sdk = check_metaquest_sdk()
    
    # Create VR project directory if it doesn't exist
    vr_project_path = repo_root / "unity_projects" / "tec_vr"
    vr_project_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"VR project directory: {vr_project_path}")
    
    # Return environment status
    return {
        "unity_installed": unity_path is not None,
        "metaquest_sdk_installed": metaquest_sdk is not None,
        "vr_project_path": str(vr_project_path)
    }

def launch_unity_project(project_path=None):
    """Launch the TEC Unity project if Unity is installed."""
    unity_path = check_unity_installation()
    if not unity_path:
        logger.error("Cannot launch Unity project: Unity not found")
        return False
    
    if not project_path:
        project_path = repo_root / "unity_projects" / "tec_vr"
    
    if not project_path.exists():
        logger.error(f"Unity project not found at: {project_path}")
        logger.info("Creating new Unity project structure...")
        project_path.mkdir(parents=True, exist_ok=True)
        # In a real scenario, this would use Unity's command-line tools to create a project
    
    logger.info(f"Unity project path: {project_path}")
    logger.info("For proper Unity integration, launch Unity Hub & open this project")
    
    return True

def main():
    """Main entry point for the AstraDigital Engine."""
    parser = argparse.ArgumentParser(description="AstraDigital Engine with VR Development")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--unity", action="store_true", help="Check Unity integration")
    parser.add_argument("--metaquest", action="store_true", help="Check MetaQuest SDK integration")
    parser.add_argument("--launch-unity", action="store_true", help="Launch Unity with TEC project")
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    if args.version:
        print("AstraDigital Engine v0.1.0 with VR Integration")
        return
    
    logger.info("Starting AstraDigital Engine...")
    logger.info("For more information, visit https://elidorascodex.com")
    
    if args.unity:
        unity_path = check_unity_installation()
        print(f"Unity status: {'INSTALLED' if unity_path else 'NOT INSTALLED'}")
        if unity_path:
            print(f"Unity path: {unity_path}")
    
    if args.metaquest:
        metaquest_sdk = check_metaquest_sdk()
        print(f"MetaQuest SDK status: {'INSTALLED' if metaquest_sdk else 'NOT INSTALLED'}")
        if metaquest_sdk:
            print(f"MetaQuest SDK path: {metaquest_sdk}")
    
    if args.launch_unity:
        launch_unity_project()
    
    # Setup VR environment by default
    vr_env = setup_vr_environment()
    logger.info(f"VR Environment Status: Unity {'✓' if vr_env['unity_installed'] else '✗'}, "
                f"MetaQuest SDK {'✓' if vr_env['metaquest_sdk_installed'] else '✗'}")

if __name__ == "__main__":
    main()
