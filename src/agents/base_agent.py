"""
Base Agent Implementation for AstraDigital Engine
"""
import os
import logging
from typing import Dict, Any, Optional
import yaml
from pathlib import Path
import json

class BaseAgent:
    """
    Base class for all AstraDigital agents.
    Provides common functionality and configuration handling.
    """
    
    def __init__(
        self, 
        name: str, 
        config_path: Optional[str] = None,
        debug: bool = False
    ):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            config_path: Path to configuration file (optional)
            debug: Whether to enable debug logging
        """
        self.name = name
        self.logger = logging.getLogger(f"astradigital.{name}")
        
        if debug:
            self.logger.setLevel(logging.DEBUG)
        
        # Load configuration
        self.config = {}
        if config_path:
            self.config = self._load_config(config_path)
        else:
            # Try default config location
            default_config = Path(os.path.dirname(os.path.dirname(__file__))) / "config" / "config.yaml"
            if default_config.exists():
                self.config = self._load_config(default_config)
        
        self.logger.info(f"{self.name} initialized")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dictionary containing configuration
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.logger.debug(f"Loaded configuration from {config_path}")
                return config or {}
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {config_path}: {e}")
            return {}
    
    def save_data(self, data: Dict[str, Any], filename: str) -> bool:
        """
        Save data to a JSON file in the data directory.
        
        Args:
            data: Data to save
            filename: Name of the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create data directory if it doesn't exist
            data_dir = Path(os.path.dirname(os.path.dirname(__file__))) / "data"
            data_dir.mkdir(exist_ok=True)
            
            # Save data
            file_path = data_dir / filename
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            self.logger.debug(f"Saved data to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save data to {filename}: {e}")
            return False
    
    def load_data(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load data from a JSON file in the data directory.
        
        Args:
            filename: Name of the file
            
        Returns:
            Dictionary containing data, or None if the file doesn't exist
        """
        try:
            file_path = Path(os.path.dirname(os.path.dirname(__file__))) / "data" / filename
            
            if not file_path.exists():
                return None
                
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            self.logger.debug(f"Loaded data from {file_path}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to load data from {filename}: {e}")
            return None
