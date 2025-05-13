"""
MetaQuest VR Development Module for AstraDigital Engine
Manages MetaQuest device connectivity, build deployment & testing
"""
import os
import sys
import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger("astradigital.metaquest")

class MetaQuestDevelopment:
    """Handles MetaQuest device interaction & app deployment."""
    
    def __init__(self, unity_project_path=None):
        """Initialize MetaQuest development tools.
        
        Args:
            unity_project_path: Path to Unity project with MetaQuest integration
        """
        self.repo_root = Path(__file__).parent.parent.parent
        
        if unity_project_path:
            self.unity_project_path = Path(unity_project_path)
        else:
            self.unity_project_path = self.repo_root / "unity_projects" / "tec_vr"
        
        # Path for build outputs
        self.build_path = self.repo_root / "builds" / "metaquest"
        self.build_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"MetaQuest development module initialized")
        logger.info(f"Unity project path: {self.unity_project_path}")
        logger.info(f"Build output path: {self.build_path}")
    
    def check_adb_installation(self):
        """Check if Android Debug Bridge (ADB) is installed for device communication."""
        try:
            # Try to run adb version command
            result = subprocess.run(
                ["adb", "version"], 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            if result.returncode == 0:
                logger.info(f"ADB installed: {result.stdout.strip()}")
                return True
            else:
                logger.warning("ADB not found or not functioning correctly")
                return False
        except (FileNotFoundError, subprocess.SubprocessError):
            logger.warning("ADB not installed or not in PATH")
            return False
    
    def list_connected_devices(self):
        """List connected MetaQuest devices via ADB."""
        if not self.check_adb_installation():
            logger.error("Cannot list devices: ADB not installed")
            return []
        
        try:
            result = subprocess.run(
                ["adb", "devices"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            # Parse device list
            lines = result.stdout.strip().split('\n')
            devices = []
            
            # Skip header line
            for line in lines[1:]:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        devices.append({
                            "id": parts[0].strip(),
                            "status": parts[1].strip()
                        })
            
            logger.info(f"Found {len(devices)} connected devices")
            for device in devices:
                logger.info(f"Device: {device['id']}, Status: {device['status']}")
            
            return devices
        except subprocess.SubprocessError as e:
            logger.error(f"Failed to list devices: {e}")
            return []
    
    def create_build_config(self):
        """Create a build configuration for MetaQuest deployment."""
        config = {
            "buildTargetPlatform": "Android",
            "xrTarget": "OculusQuest",
            "appName": "TECAstradigital",
            "companyName": "ElidorasCodex",
            "productName": "The Elidoras Codex VR",
            "version": "0.1.0",
            "bundleIdentifier": "com.elidorascodex.tecvr",
            "developmentBuild": True,
            "scriptingBackend": "IL2CPP"
        }
        
        config_path = self.unity_project_path / "metaquest_build_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"MetaQuest build configuration created at: {config_path}")
        
        # Create build instructions
        instructions = """
        # Building for MetaQuest
        
        ## Prerequisites
        1. Unity with Android Build Support installed
        2. Meta Quest developer account & registered device
        3. Oculus Integration package installed in Unity
        
        ## Build Steps
        1. Open Project in Unity
        2. File > Build Settings
        3. Switch Platform to Android
        4. Set Target Device to "Oculus Quest" or "Oculus Quest 2/3"
        5. Enable "Development Build" option
        6. Connect MetaQuest device via USB
        7. Click "Build And Run"
        
        ## Alternative Build Process
        1. Run the `build_for_metaquest.py` script in this directory
        2. Wait for automated build process to complete
        3. APK will be deployed to connected device automatically
        
        For troubleshooting, see: https://developer.oculus.com/documentation/unity
        """
        
        with open(self.unity_project_path / "METAQUEST_BUILD_GUIDE.md", 'w') as f:
            f.write(instructions)
        
        logger.info("MetaQuest build instructions created")
        return str(config_path)
    
    def create_build_script(self):
        """Create a Python script to automate building for MetaQuest."""
        script_content = """#!/usr/bin/env python3
'''
Automated build script for MetaQuest deployment
'''
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

def find_unity_executable():
    '''Find Unity executable based on platform'''
    if sys.platform == "win32":
        unity_paths = [
            "C:\\Program Files\\Unity\\Hub\\Editor",
            "C:\\Program Files\\Unity"
        ]
        for base in unity_paths:
            if os.path.exists(base):
                # Find newest version
                versions = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
                if versions:
                    latest = sorted(versions)[-1]
                    unity_exe = os.path.join(base, latest, "Editor", "Unity.exe")
                    if os.path.exists(unity_exe):
                        return unity_exe
    elif sys.platform == "darwin":  # macOS
        # Find newest version on macOS
        base_path = "/Applications/Unity/Hub/Editor"
        if os.path.exists(base_path):
            versions = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
            if versions:
                latest = sorted(versions)[-1]
                unity_app = f"{base_path}/{latest}/Unity.app/Contents/MacOS/Unity"
                if os.path.exists(unity_app):
                    return unity_app
    
    print("ERROR: Unity executable not found")
    return None

def main():
    '''Main entry point for build script'''
    parser = argparse.ArgumentParser(description="Build TEC for MetaQuest")
    parser.add_argument("--project", default=".", help="Path to Unity project")
    parser.add_argument("--output", default="../builds/metaquest", help="Output path for build")
    parser.add_argument("--run", action="store_true", help="Run on device after build")
    
    args = parser.parse_args()
    
    # Ensure paths are absolute
    project_path = Path(args.project).absolute()
    output_path = Path(args.output).absolute()
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load build config if exists
    config_path = project_path / "metaquest_build_config.json"
    config = {}
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    
    # Find Unity
    unity_exe = find_unity_executable()
    if not unity_exe:
        print("Cannot proceed without Unity installation")
        return 1
    
    print(f"Using Unity: {unity_exe}")
    print(f"Building project: {project_path}")
    print(f"Output path: {output_path}")
    
    # Build command would go here in a real implementation
    # This would use Unity's command line build system
    # For now, we just print instructions
    
    print("\\nIn a real implementation, this script would:")
    print("1. Start Unity in batch mode")
    print("2. Execute build script for Android/Oculus platform")
    print("3. Generate APK in the output directory")
    if args.run:
        print("4. Deploy built APK to connected device")
    
    print("\\nSince this is a placeholder script, please follow the manual")
    print("build instructions in METAQUEST_BUILD_GUIDE.md")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        
        script_path = self.unity_project_path / "build_for_metaquest.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable on Unix-like systems
        if sys.platform != "win32":
            os.chmod(script_path, 0o755)
        
        logger.info(f"Created MetaQuest build script at: {script_path}")
        return str(script_path)
    
    def create_device_preview_script(self):
        """Create a Python script to preview TEC world on MetaQuest."""
        script_content = """#!/usr/bin/env python3
'''
AstraDigital MetaQuest Preview Tool
Visualize the current state of the TEC world in VR
'''
import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
import webbrowser

def check_device_connection():
    '''Check if a MetaQuest device is connected via ADB'''
    try:
        result = subprocess.run(
            ["adb", "devices"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Parse device list
        lines = result.stdout.strip().split('\\n')
        devices = []
        
        # Skip header line
        for line in lines[1:]:
            if line.strip():
                parts = line.split('\\t')
                if len(parts) >= 2:
                    devices.append({
                        "id": parts[0].strip(),
                        "status": parts[1].strip()
                    })
        
        return len(devices) > 0
    except (FileNotFoundError, subprocess.SubprocessError):
        print("ADB not installed or not in PATH")
        return False

def generate_preview_data():
    '''Create a sample visualization of current TEC world state'''
    # In a real implementation, this would read from AstraDigital engine data
    # For now, we'll create a placeholder visualization
    preview_data = {
        "worldName": "Astradigital Ocean - Live Preview",
        "timestamp": time.time(),
        "locations": [
            {
                "name": "Current Position",
                "position": {"x": 0, "y": 1.8, "z": 0},
                "description": "Your current location in the Astradigital Ocean"
            },
            {
                "name": "MAGMASOX Hub",
                "position": {"x": 10, "y": 0, "z": 15},
                "description": "Live connection to the MAGMASOX faction hub"
            },
            {
                "name": "Data Stream Alpha",
                "position": {"x": -5, "y": 3, "z": 8},
                "description": "Active data stream from the TEC repository"
            }
        ]
    }
    
    # Save preview data to temporary file
    output_dir = Path.home() / ".tec" / "vr_preview"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    preview_path = output_dir / "live_preview.json"
    with open(preview_path, 'w') as f:
        json.dump(preview_data, f, indent=2)
    
    return str(preview_path)

def main():
    '''Main entry point for VR preview tool'''
    parser = argparse.ArgumentParser(description="AstraDigital MetaQuest Preview Tool")
    parser.add_argument("--mode", choices=["live", "static"], default="live",
                        help="Preview mode (live or static visualization)")
    
    args = parser.parse_args()
    
    print("======================================")
    print("   AstraDigital MetaQuest Preview   ")
    print("======================================")
    
    # Check if device is connected
    if not check_device_connection():
        print("⚠️  No MetaQuest device detected!")
        print("Please connect your device via USB and ensure:")
        print("1. Developer mode is enabled on your headset")
        print("2. USB debugging is allowed")
        print("3. You've accepted the connection prompt in your headset")
        return 1
    
    print("✅ MetaQuest device detected")
    
    # Generate preview data
    preview_path = generate_preview_data()
    print(f"✅ Generated visualization data: {preview_path}")
    
    print("\\nIn a real implementation, this script would:")
    if args.mode == "live":
        print("1. Push the visualization data to the headset")
        print("2. Launch the TEC Viewer app in the headset")
        print("3. Stream real-time updates as you work")
    else:
        print("1. Generate a static 3D visualization of the TEC world")
        print("2. Deploy to the headset for viewing")
    
    print("\\nSince this is a placeholder script, please follow these steps:")
    print("1. Build and deploy the TEC VR app using build_for_metaquest.py")
    print("2. Launch the app from your MetaQuest home environment")
    print("3. The app will load the most recent TEC world data")
    
    # Open documentation in browser
    webbrowser.open("https://elidorascodex.com")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        
        script_path = self.unity_project_path / "preview_on_metaquest.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable on Unix-like systems
        if sys.platform != "win32":
            os.chmod(script_path, 0o755)
        
        logger.info(f"Created MetaQuest preview script at: {script_path}")
        return str(script_path)
    
    def setup_full_environment(self):
        """Setup the complete MetaQuest development environment."""
        logger.info("Setting up complete MetaQuest development environment...")
        
        # 1. Create build configuration
        self.create_build_config()
        
        # 2. Create build script
        self.create_build_script()
        
        # 3. Create device preview script
        self.create_device_preview_script()
        
        # 4. Check for ADB installation
        adb_installed = self.check_adb_installation()
        
        # 5. Check for connected devices
        devices = []
        if adb_installed:
            devices = self.list_connected_devices()
        
        logger.info("MetaQuest development environment setup complete")
        logger.info(f"ADB installed: {'✓' if adb_installed else '✗'}")
        logger.info(f"Connected devices: {len(devices)}")
        
        return {
            "adb_installed": adb_installed,
            "connected_devices": devices,
            "build_path": str(self.build_path),
            "unity_project": str(self.unity_project_path)
        }
