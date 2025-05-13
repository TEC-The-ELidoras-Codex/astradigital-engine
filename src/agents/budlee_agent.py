"""
Budlee Agent - Automation specialist and backend operations agent for The Elidoras Codex.
Handles system automation, setup, and site integrations.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables first
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', '.env')
load_dotenv(env_path, override=True)

from .base_agent import BaseAgent
from .wp_poster import WordPressAgent
from .local_storage import LocalStorageAgent

class BudleeAgent(BaseAgent):
    """
    BudleeAgent is an automation-focused agent that handles backend operations.
    It manages system setup, integrations, and technical operations.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__("BudleeAgent", config_path)
        self.logger.info("BudleeAgent initialized")
        
        # Initialize WordPress agent for site operations
        self.wp_agent = WordPressAgent(config_path)
        
        # Initialize LocalStorage agent for file operations
        self.storage_agent = LocalStorageAgent(config_path)
        
        # Load configuration
        self.automations = self._load_automations()
    
    def _load_automations(self) -> Dict[str, Any]:
        """
        Load automation configurations.
        
        Returns:
            Dictionary of automation configurations
        """
        try:
            # Default automations if file doesn't exist
            default_automations = {
                "wordpress_backup": {
                    "enabled": True,
                    "schedule": "daily",
                    "retention_days": 7
                },
                "system_health_check": {
                    "enabled": True,
                    "schedule": "hourly",
                    "metrics": ["disk_space", "memory_usage", "api_health"]
                },
                "wordpress_post_scheduler": {
                    "enabled": True,
                    "schedule": "weekly",
                    "target_day": "Monday",
                    "topics": ["AI technology", "digital consciousness", "automation"]
                }
            }
            
            # Try to load from file if it exists
            config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
            automations_path = os.path.join(config_dir, 'automations.json')
            
            if os.path.exists(automations_path):
                with open(automations_path, 'r') as f:
                    automations = json.load(f)
                self.logger.info(f"Loaded automations from {automations_path}")
                return automations
            else:
                self.logger.info(f"Automations file not found at {automations_path}, using defaults")
                # Create the file with default values
                os.makedirs(os.path.dirname(automations_path), exist_ok=True)
                with open(automations_path, 'w') as f:
                    json.dump(default_automations, f, indent=2)
                return default_automations
                
        except Exception as e:
            self.logger.error(f"Failed to load automations: {e}")
            return {}
    
    def check_system_health(self) -> Dict[str, Any]:
        """
        Check system health metrics.
        
        Returns:
            Dictionary with system health metrics
        """
        try:
            # Get disk space
            import shutil
            disk = shutil.disk_usage("/")
            disk_total = disk.total / (1024**3)  # Convert to GB
            disk_used = disk.used / (1024**3)
            disk_free = disk.free / (1024**3)
            disk_percent = disk.used / disk.total * 100
            
            # Get memory usage (simple version)
            import psutil
            memory = psutil.virtual_memory()
            memory_total = memory.total / (1024**3)  # Convert to GB
            memory_used = memory.used / (1024**3)
            memory_free = memory.available / (1024**3)
            memory_percent = memory.percent
            
            # Check API health
            api_status = self._check_api_health()
            
            self.logger.info(f"System health check complete")
            return {
                "timestamp": datetime.now().isoformat(),
                "disk": {
                    "total_gb": round(disk_total, 2),
                    "used_gb": round(disk_used, 2),
                    "free_gb": round(disk_free, 2),
                    "percent_used": round(disk_percent, 2)
                },
                "memory": {
                    "total_gb": round(memory_total, 2),
                    "used_gb": round(memory_used, 2),
                    "free_gb": round(memory_free, 2),
                    "percent_used": round(memory_percent, 2)
                },
                "apis": api_status
            }
            
        except ImportError:
            self.logger.error("Required modules not found for system health check")
            return {
                "error": "Required modules not found. Please install psutil: pip install psutil"
            }
        except Exception as e:
            self.logger.error(f"Failed to check system health: {e}")
            return {"error": str(e)}
    
    def _check_api_health(self) -> Dict[str, Any]:
        """
        Check the health of various APIs used by TEC.
        
        Returns:
            Dictionary with API health status
        """
        import requests
        
        apis = {
            "wordpress": self.wp_agent.api_base_url if hasattr(self.wp_agent, 'api_base_url') else None,
            "openai": "https://api.openai.com/v1/engines"
        }
        
        results = {}
        for name, url in apis.items():
            if not url:
                results[name] = {"status": "not_configured"}
                continue
                
            try:
                if name == "openai":
                    # For OpenAI, just check if the API key is configured
                    api_key = os.getenv("OPENAI_API_KEY")
                    if api_key:
                        results[name] = {"status": "configured"}
                    else:
                        results[name] = {"status": "no_api_key"}
                else:
                    # For other APIs, try to make a simple GET request
                    response = requests.head(url, timeout=5)
                    results[name] = {
                        "status": "online" if response.status_code < 400 else "error",
                        "status_code": response.status_code
                    }
            except Exception as e:
                results[name] = {"status": "error", "message": str(e)}
                
        return results
    
    def backup_wordpress_content(self) -> Dict[str, Any]:
        """
        Backup WordPress content using the WordPress agent.
        This is a placeholder for WordPress backup functionality.
        
        Returns:
            Dictionary with backup status
        """
        # This is a placeholder for WordPress backup functionality
        self.logger.info("WordPress backup initiated")
        
        # Example of what a real implementation might do:
        # 1. Get list of posts from WordPress
        # 2. Save them to local storage
        # 3. Backup media files
        
        # For now, just simulate the backup
        backup_file = f"wordpress_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = os.path.join(self.storage_agent.storage_dir, "backups", backup_file)
        
        # Create a dummy backup with metadata
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "backup_type": "wordpress_content",
            "status": "simulated"
        }
        
        # Save to the backup location
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)
            
        return {
            "success": True,
            "backup_file": backup_file,
            "backup_path": backup_path,
            "timestamp": datetime.now().isoformat()
        }
    
    def run(self) -> Dict[str, Any]:
        """
        Run the Budlee agent's default action - system health check.
        
        Returns:
            Dictionary containing the result of the operation
        """
        self.logger.info("Running Budlee agent's default action")
        results = {
            "system_health": self.check_system_health()
        }
        
        # Check if WordPress backup is enabled
        wp_backup = self.automations.get("wordpress_backup", {}).get("enabled", False)
        if wp_backup:
            results["wordpress_backup"] = self.backup_wordpress_content()
            
        return results

# For testing the agent standalone
if __name__ == "__main__":
    budlee = BudleeAgent()
    result = budlee.run()
    print(json.dumps(result, indent=2))
