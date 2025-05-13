"""
Configuration utilities for TEC_OFFICE_REPO
"""
import os
import yaml
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger("TEC.Config")

class Config:
    """Configuration handler for TEC_OFFICE_REPO"""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize configuration handler
        
        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = config_dir
        self._config = {}
        
        # Load .env file
        self._load_env()
        
        # Load configuration files
        self._load_yaml_config()
        self._load_json_prompts()
        
    def _load_env(self) -> None:
        """Load environment variables from .env file"""
        env_path = os.path.join(self.config_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)
            logger.info(f"Loaded environment variables from {env_path}")
        else:
            logger.warning(f"No .env file found at {env_path}")
            
    def _load_yaml_config(self) -> None:
        """Load YAML configuration file"""
        yaml_path = os.path.join(self.config_dir, 'config.yaml')
        if os.path.exists(yaml_path):
            try:
                with open(yaml_path, 'r') as f:
                    self._config.update(yaml.safe_load(f) or {})
                logger.info(f"Loaded configuration from {yaml_path}")
            except Exception as e:
                logger.error(f"Error loading YAML configuration: {e}")
        else:
            logger.warning(f"No YAML configuration found at {yaml_path}")
            
    def _load_json_prompts(self) -> None:
        """Load JSON prompts file"""
        json_path = os.path.join(self.config_dir, 'prompts.json')
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    self._config['prompts'] = json.load(f)
                logger.info(f"Loaded prompts from {json_path}")
            except Exception as e:
                logger.error(f"Error loading JSON prompts: {e}")
        else:
            logger.warning(f"No JSON prompts found at {json_path}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        
        Args:
            key: Configuration key (can be nested with dots e.g. 'agents.airth.temperature')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        parts = key.split('.')
        value = self._config
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
                
        return value
        
    def get_prompt(self, prompt_name: str, default: str = "") -> str:
        """
        Get a prompt template by name
        
        Args:
            prompt_name: Name of the prompt template
            default: Default prompt if not found
            
        Returns:
            Prompt template string
        """
        prompts = self._config.get('prompts', {})
        return prompts.get(prompt_name, default)
        
    def get_env(self, key: str, default: str = None) -> Optional[str]:
        """
        Get environment variable
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)
