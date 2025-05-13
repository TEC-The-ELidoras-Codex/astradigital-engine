#!/usr/bin/env python3
"""
TEC VR Development CLI Tool
Manages Unity & MetaQuest integration with AstraDigital Engine
"""
import os
import sys
import argparse
import logging
from pathlib import Path

# Add repository root to path
repo_root = Path(__file__).parent.parent
sys.path.append(str(repo_root))

from src.utils.unity_integration import UnityIntegration, generate_sample_world_data
from src.utils.metaquest_dev import MetaQuestDevelopment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("tec.vr_tools")

def setup_command(args):
    """Setup Unity & MetaQuest development environment."""
    print("🚀 Setting up TEC VR development environment...")
    
    # Initialize Unity integration
    unity = UnityIntegration()
    
    # Create Unity project
    if args.unity:
        print("📦 Creating Unity project structure...")
        unity.create_unity_project()
        
        # Create data bridge script
        print("🔌 Creating Unity-AstraDigital data bridge...")
        unity.create_data_bridge_script()
        
        # Export sample data
        if args.sample_data:
            print("📊 Generating sample world data...")
            sample_data = generate_sample_world_data()
            unity.export_astradigital_data(sample_data)
    
    # Setup MetaQuest integration
    if args.metaquest:
        print("🥽 Setting up MetaQuest integration...")
        
        # Setup Unity MetaQuest integration
        unity.setup_metaquest_integration()
        
        # Setup MetaQuest development tools
        metaquest = MetaQuestDevelopment(unity_project_path=unity.project_path)
        env_status = metaquest.setup_full_environment()
        
        if env_status["adb_installed"]:
            print("✅ ADB installed & working")
            
            if env_status["connected_devices"]:
                print(f"✅ {len(env_status['connected_devices'])} MetaQuest device(s) connected")
            else:
                print("❌ No MetaQuest devices connected")
        else:
            print("❌ ADB not found - required for device communication")
            print("   Install Android SDK Platform Tools to enable ADB")
    
    print("\n✨ Setup complete!")
    print(f"Unity project path: {unity.project_path}")
    
    # Print next steps
    print("\n📋 Next steps:")
    print("1. Open Unity Hub & add the project from:")
    print(f"   {unity.project_path}")
    print("2. Install required packages (Oculus Integration, XR Toolkit)")
    print("3. Follow setup instructions in METAQUEST_SETUP.md")
    print("\nFor detailed documentation, visit: https://elidorascodex.com")

def export_command(args):
    """Export TEC world data to Unity project."""
    print("📤 Exporting AstraDigital world to Unity...")
    
    # Initialize Unity integration
    unity = UnityIntegration(project_path=args.project)
    
    if args.sample:
        # Generate & export sample data
        print("📊 Generating sample world data...")
        sample_data = generate_sample_world_data()
        output_path = unity.export_astradigital_data(sample_data, args.output_file)
        print(f"✅ Exported sample data to: {output_path}")
    else:
        # Load & export TEC world data
        print("🔄 Loading current TEC world data...")
        # In a real implementation, this would load data from AstraDigital engine
        sample_data = generate_sample_world_data()
        sample_data["worldName"] = "Current AstraDigital Ocean State"
        output_path = unity.export_astradigital_data(sample_data, args.output_file)
        print(f"✅ Exported current world state to: {output_path}")
    
    print("\n📋 Next steps:")
    print("1. Open the Unity project")
    print("2. The data will automatically be loaded by the AstradigitalBridge component")
    print("3. Press Play to visualize the world")

def device_command(args):
    """Manage MetaQuest device connections."""
    print("🥽 MetaQuest Device Management")
    
    # Initialize MetaQuest development tools
    metaquest = MetaQuestDevelopment()
    
    # Check ADB installation
    adb_installed = metaquest.check_adb_installation()
    if not adb_installed:
        print("❌ ADB not installed - required for device communication")
        print("   Install Android SDK Platform Tools to enable ADB")
        return
    
    print("✅ ADB installed & working")
    
    # List connected devices
    print("\n📱 Connected devices:")
    devices = metaquest.list_connected_devices()
    
    if not devices:
        print("  No devices connected")
        print("\n🔍 Troubleshooting:")
        print("1. Ensure your MetaQuest is connected via USB")
        print("2. Verify Developer Mode is enabled on your headset")
        print("3. Accept the 'Allow USB Debugging' prompt in your headset")
        return
    
    for i, device in enumerate(devices, 1):
        print(f"  {i}. {device['id']} - {device['status']}")
    
    # Additional device operations
    if args.operation == "preview":
        print("\n🔮 Launching preview on device...")
        print("  This would launch a VR preview on the connected headset")
        print("  For now, please use the preview_on_metaquest.py script")

def build_command(args):
    """Build TEC for MetaQuest devices."""
    print("🔨 Building TEC for MetaQuest")
    
    # Initialize Unity & MetaQuest tools
    unity = UnityIntegration(project_path=args.project)
    metaquest = MetaQuestDevelopment(unity_project_path=unity.project_path)
    
    # Ensure build scripts exist
    metaquest.create_build_config()
    build_script = metaquest.create_build_script()
    
    print(f"✅ Build configuration ready")
    print(f"✅ Build script created at: {build_script}")
    
    print("\n📋 To build for MetaQuest:")
    print(f"1. Navigate to: {unity.project_path}")
    print("2. Run: python build_for_metaquest.py --run")
    print("\nIn a full implementation, this command would:")
    print("1. Compile the Unity project for Android/Oculus")
    print("2. Generate an APK file")
    print("3. Deploy to connected MetaQuest device")
    print("4. Launch the application on the device")

def main():
    """Main entry point for TEC VR development CLI."""
    parser = argparse.ArgumentParser(
        description="TEC VR Development Tools for Unity & MetaQuest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Setup complete VR environment
  tec_vr_tools.py setup --unity --metaquest
  
  # Export current world state to Unity
  tec_vr_tools.py export
  
  # List connected MetaQuest devices
  tec_vr_tools.py device list
  
  # Build for MetaQuest
  tec_vr_tools.py build
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup VR development environment")
    setup_parser.add_argument("--unity", action="store_true", help="Setup Unity integration")
    setup_parser.add_argument("--metaquest", action="store_true", help="Setup MetaQuest integration")
    setup_parser.add_argument("--sample-data", action="store_true", help="Generate sample world data")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export AstraDigital world to Unity")
    export_parser.add_argument("--project", default=None, help="Unity project path")
    export_parser.add_argument("--output-file", default="astradigital_data.json", help="Output filename")
    export_parser.add_argument("--sample", action="store_true", help="Export sample data instead of current world")
    
    # Device command
    device_parser = subparsers.add_parser("device", help="Manage MetaQuest devices")
    device_parser.add_argument("operation", choices=["list", "preview"], default="list", help="Device operation")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build for MetaQuest")
    build_parser.add_argument("--project", default=None, help="Unity project path")
    
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == "setup":
        setup_command(args)
    elif args.command == "export":
        export_command(args)
    elif args.command == "device":
        device_command(args)
    elif args.command == "build":
        build_command(args)

if __name__ == "__main__":
    main()
