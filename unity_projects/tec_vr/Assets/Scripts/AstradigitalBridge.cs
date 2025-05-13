using System.Collections;
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
