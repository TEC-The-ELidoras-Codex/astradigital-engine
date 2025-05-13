"""
Unity Integration Module for AstraDigital Engine
Handles communication between AstraDigital Engine & Unity/MetaQuest VR projects
"""
import os
import sys
import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger("astradigital.unity")

class UnityIntegration:
    """Manages Unity project integration with AstraDigital Engine."""
    
    def __init__(self, project_path=None, unity_version="2022.3.16f1"):
        """Initialize Unity integration.
        
        Args:
            project_path: Path to Unity project (creates if doesn't exist)
            unity_version: Target Unity version for project
        """
        self.repo_root = Path(__file__).parent.parent.parent
        self.unity_version = unity_version
        
        if project_path:
            self.project_path = Path(project_path)
        else:
            self.project_path = self.repo_root / "unity_projects" / "tec_vr"
            self.project_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Unity integration initialized for project: {self.project_path}")
    
    def find_unity_executable(self):
        """Find the Unity executable based on platform."""
        if sys.platform == "win32":
            base_paths = [
                "C:\\Program Files\\Unity\\Hub\\Editor",
                "C:\\Program Files\\Unity"
            ]
            for base in base_paths:
                for ver_dir in os.listdir(base):
                    if ver_dir.startswith(self.unity_version):
                        unity_exe = os.path.join(base, ver_dir, "Editor", "Unity.exe")
                        if os.path.exists(unity_exe):
                            return unity_exe
        elif sys.platform == "darwin":  # macOS
            base_path = f"/Applications/Unity/Hub/Editor/{self.unity_version}"
            unity_app = f"{base_path}/Unity.app/Contents/MacOS/Unity"
            if os.path.exists(unity_app):
                return unity_app
        else:  # Linux
            base_path = f"~/Unity/Hub/Editor/{self.unity_version}"
            unity_exe = os.path.expanduser(f"{base_path}/Editor/Unity")
            if os.path.exists(unity_exe):
                return unity_exe
        
        logger.warning(f"Unity executable for version {self.unity_version} not found")
        return None
    
    def export_astradigital_data(self, data, output_file="astradigital_data.json"):
        """Export AstraDigital world data to a format Unity can import.
        
        Args:
            data: Dictionary of world data to export
            output_file: Output JSON file name
        """
        output_path = self.project_path / "Assets" / "AstradigitalData" / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported AstraDigital data to: {output_path}")
        return str(output_path)
    
    def create_unity_project(self, template="3d"):
        """Create a new Unity project if it doesn't exist.
        
        Args:
            template: Unity project template (3d, 2d, vr, etc.)
        """
        if (self.project_path / "Assets").exists():
            logger.info(f"Unity project already exists at: {self.project_path}")
            return True
        
        unity_exe = self.find_unity_executable()
        if not unity_exe:
            logger.error("Cannot create Unity project: Unity executable not found")
            return False
        
        # Create necessary directories
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        # In a real scenario, this would use Unity's command-line to create a project
        logger.info(f"Creating Unity project structure at: {self.project_path}")
        
        # Create minimal project structure
        (self.project_path / "Assets").mkdir(exist_ok=True)
        (self.project_path / "Assets" / "AstradigitalData").mkdir(exist_ok=True)
        (self.project_path / "Assets" / "Scripts").mkdir(exist_ok=True)
        (self.project_path / "ProjectSettings").mkdir(exist_ok=True)
        
        # Create a placeholder readme
        with open(self.project_path / "README.md", 'w') as f:
            f.write("# The Elidoras Codex - VR Experience\n\n")
            f.write("Unity project for visualizing the Astradigital Ocean in VR on MetaQuest.\n")
            f.write("Created by AstraDigital Engine.\n")
        
        logger.info("Unity project structure created successfully")
        return True
    
    def setup_metaquest_integration(self):
        """Configure MetaQuest SDK integration for the Unity project."""
        # Create MetaQuest configuration file
        metaquest_config = {
            "enabled": True,
            "targetDevices": ["quest2", "quest3"],
            "minimumApiVersion": "v50.0",
            "spatialAnchorsEnabled": True
        }
        
        config_path = self.project_path / "Assets" / "AstradigitalData" / "metaquest_config.json"
        with open(config_path, 'w') as f:
            json.dump(metaquest_config, f, indent=2)
        
        logger.info("MetaQuest configuration created at: {}".format(config_path))
        
        # Instructions for manual SDK integration
        instructions = """
        # MetaQuest Integration Instructions
        
        1. Open the Unity project in Unity Hub
        2. Go to Window > Package Manager
        3. Click the "+" button > Add package by name
        4. Add the following packages:
           - com.unity.xr.interaction.toolkit
           - com.unity.xr.management
        5. Install the Oculus Integration package from the Asset Store
        6. Configure XR Plugin Management for Oculus
        
        For more detailed instructions, visit: https://developer.oculus.com/documentation/unity
        """
        
        with open(self.project_path / "METAQUEST_SETUP.md", 'w') as f:
            f.write(instructions)
        
        logger.info("MetaQuest setup instructions created")
        return True
    
    def create_data_bridge_script(self):
        """Create a C# script to bridge AstraDigital data to Unity."""
        script_content = """using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Threading.Tasks;

namespace AstradigitalEngine 
{
    [System.Serializable]
    public class WorldData 
    {
        public string worldName;
        public List<LocationData> locations = new List<LocationData>();
        // Add other world data properties as needed
    }
    
    [System.Serializable]
    public class LocationData 
    {
        public string name;
        public Vector3 position;
        public string description;
        // Add other location data properties as needed
    }
    
    public class AstradigitalBridge : MonoBehaviour 
    {
        public string dataFilePath = "Assets/AstradigitalData/astradigital_data.json";
        public WorldData worldData;
        
        void Start() 
        {
            LoadWorldData();
        }
        
        public async Task LoadWorldData() 
        {
            if (File.Exists(dataFilePath)) 
            {
                string jsonData = File.ReadAllText(dataFilePath);
                worldData = JsonUtility.FromJson<WorldData>(jsonData);
                Debug.Log($"Loaded AstraDigital world: {worldData.worldName}");
                
                // Visualize the world data
                VisualizeWorld();
            } 
            else 
            {
                Debug.LogWarning($"AstraDigital data file not found at: {dataFilePath}");
            }
        }
        
        void VisualizeWorld() 
        {
            if (worldData == null || worldData.locations == null) return;
            
            foreach (var location in worldData.locations) 
            {
                // Create a visual representation for each location
                GameObject locationObj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                locationObj.transform.position = location.position;
                locationObj.transform.localScale = Vector3.one * 0.5f;
                locationObj.name = location.name;
                
                // Add a descriptor component
                var descriptor = locationObj.AddComponent<LocationDescriptor>();
                descriptor.description = location.description;
                
                Debug.Log($"Created visualization for location: {location.name}");
            }
        }
    }
    
    public class LocationDescriptor : MonoBehaviour 
    {
        public string description;
        
        void OnDrawGizmosSelected() 
        {
            // Draw location name in scene view
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(transform.position, 0.6f);
        }
    }
}
"""
        
        script_path = self.project_path / "Assets" / "Scripts" / "AstradigitalBridge.cs"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        logger.info(f"Created Unity data bridge script at: {script_path}")
        return str(script_path)

def generate_sample_world_data():
    """Generate sample Astradigital world data for testing."""
    return {
        "worldName": "Astradigital Ocean",
        "version": "0.1.0",
        "description": "The digital realm of The Elidoras Codex",
        "locations": [
            {
                "name": "MAGMASOX Hub",
                "position": {"x": 0, "y": 0, "z": 0},
                "description": "Central hub of the MAGMASOX faction"
            },
            {
                "name": "Kaznak Outpost",
                "position": {"x": 120, "y": 15, "z": -45},
                "description": "Forward base of the Kaznak Voyagers"
            },
            {
                "name": "Data Nexus Alpha",
                "position": {"x": -85, "y": 30, "z": 65},
                "description": "Primary data storage facility"
            }
        ],
        "factions": [
            {
                "name": "MAGMASOX",
                "primaryColor": "#FF7700",
                "description": "Keepers of the ancient digital mysteries"
            },
            {
                "name": "Kaznak Voyagers",
                "primaryColor": "#00BBFF",
                "description": "Explorers of the furthest reaches of the Astradigital Ocean"
            }
        ]
    }
