"""
Base Agent class for all TEC agents.
This serves as the foundation for all agent types in the TEC ecosystem.
"""
import os
import sys
import logging
import time
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

# Add site-packages to path to help find modules
python_path = sys.executable
site_packages = os.path.join(os.path.dirname(os.path.dirname(python_path)), 'lib', 'site-packages')
if os.path.exists(site_packages):
    sys.path.append(site_packages)

# Get the project root folder
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv
from utils.logging import get_logger

class BaseAgent:
    """Base class for all TEC agents to inherit from."""
    
    def __init__(self, name: str, config_path: Optional[str] = None):
        """
        Initialize the base agent with a name and optional configuration.
        
        Args:
            name: Name of the agent
            config_path: Optional path to a configuration file
        """
        self.name = name
        self.logger = get_logger(name)
        self.logger.info(f"Initializing {name} agent")
        
        # Performance metrics tracking
        self.metrics = {
            "operations": {},
            "api_calls": {},
            "errors": {},
            "latency": {}
        }
        
        # Load environment variables from the specific path
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
        load_dotenv(env_path, override=True)
          # Load configuration if provided
        self.config = {}
        if config_path:
            self._load_config(config_path)
    
    def track_operation(self, operation_name: str, success: bool, duration_ms: int) -> None:
        """
        Track operation metrics.
        
        Args:
            operation_name: Name of the operation
            success: Whether the operation was successful
            duration_ms: Duration of the operation in milliseconds
        """
        if operation_name not in self.metrics["operations"]:
            self.metrics["operations"][operation_name] = {
                "total": 0,
                "success": 0,
                "failure": 0,
                "total_duration_ms": 0,
                "avg_duration_ms": 0
            }
        
        metrics = self.metrics["operations"][operation_name]
        metrics["total"] += 1
        if success:
            metrics["success"] += 1
        else:
            metrics["failure"] += 1
        
        metrics["total_duration_ms"] += duration_ms
        metrics["avg_duration_ms"] = metrics["total_duration_ms"] / metrics["total"]
        
        # Log the operation
        if success:
            self.logger.debug(f"Operation {operation_name} completed successfully in {duration_ms}ms")
        else:
            self.logger.warning(f"Operation {operation_name} failed after {duration_ms}ms")
    
    def track_api_call(self, service_name: str, endpoint: str, 
                       success: bool, duration_ms: int, status_code: Optional[int] = None) -> None:
        """
        Track API call metrics.
        
        Args:
            service_name: Name of the service (e.g., 'OpenAI', 'WordPress')
            endpoint: API endpoint called
            success: Whether the call was successful
            duration_ms: Duration of the call in milliseconds
            status_code: HTTP status code if applicable
        """
        key = f"{service_name}:{endpoint}"
        
        if key not in self.metrics["api_calls"]:
            self.metrics["api_calls"][key] = {
                "total": 0,
                "success": 0,
                "failure": 0,
                "total_duration_ms": 0,
                "avg_duration_ms": 0,
                "status_codes": {}
            }
        
        metrics = self.metrics["api_calls"][key]
        metrics["total"] += 1
        if success:
            metrics["success"] += 1
        else:
            metrics["failure"] += 1
        
        metrics["total_duration_ms"] += duration_ms
        metrics["avg_duration_ms"] = metrics["total_duration_ms"] / metrics["total"]
        
        # Track status code
        if status_code:
            if str(status_code) not in metrics["status_codes"]:
                metrics["status_codes"][str(status_code)] = 0
            metrics["status_codes"][str(status_code)] += 1
        
        # Log the API call
        if success:
            self.logger.debug(f"API call to {service_name}:{endpoint} completed with status {status_code} in {duration_ms}ms")
        else:
            self.logger.warning(f"API call to {service_name}:{endpoint} failed with status {status_code} after {duration_ms}ms")
    
    def timed_operation(self, operation_name: str):
        """
        Decorator for tracking operation metrics automatically.
        
        Args:
            operation_name: Name of the operation to track
            
        Returns:
            Decorated function that tracks timing and success
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    duration_ms = int((end_time - start_time) * 1000)
                    self.track_operation(operation_name, True, duration_ms)
                    return result
                except Exception as e:
                    end_time = time.time()
                    duration_ms = int((end_time - start_time) * 1000)
                    self.track_operation(operation_name, False, duration_ms)
                    # Re-raise the exception
                    raise
            return wrapper
        return decorator
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current agent metrics.
        
        Returns:
            Dictionary of agent metrics
        """
        return {
            "name": self.name,
            "metrics": self.metrics,
            "success_rate": self._calculate_success_rate()
        }
    
    def _calculate_success_rate(self) -> float:
        """
        Calculate overall operation success rate.
        
        Returns:
            Success rate as a percentage
        """
        total_ops = 0
        total_success = 0
        
        for op_metrics in self.metrics["operations"].values():
            total_ops += op_metrics["total"]
            total_success += op_metrics["success"]
        
        if total_ops == 0:
            return 100.0  # No operations yet, return 100%
        
        return (total_success / total_ops) * 100
        
    def _load_config(self, config_path: str) -> None:
        """
        Load configuration from a file.
        
        Args:
            config_path: Path to the configuration file or directory
        """
        try:
            # Import yaml with error handling
            try:
                import yaml
            except ImportError:
                self.logger.error("PyYAML not found. Please run 'pip install pyyaml'")
                return
            
            # If the path is a directory, look for config.yaml
            if os.path.isdir(config_path):
                config_file = os.path.join(config_path, "config.yaml")
                if not os.path.exists(config_file):
                    self.logger.info(f"No config.yaml found in {config_path}, skipping configuration")
                    return
                config_path = config_file
                
            # Load the YAML file
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.config = yaml.safe_load(f)
                self.logger.info(f"Loaded configuration from {config_path}")
            else:
                self.logger.warning(f"Configuration file not found: {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            # Continue without configuration rather than failing
    
    def run(self) -> Dict[str, Any]:
        """
        Run the agent's main functionality.
        This method should be overridden by subclasses.
        
        Returns:
            Dict containing the result of the agent's execution
        """
        self.logger.warning("Base run method called - should be overridden by subclass")
        return {"status": "not_implemented", "message": "This method should be overridden"}