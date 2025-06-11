"""
Orchestrator Agent for The Elidoras Codex.
This agent is responsible for coordinating all other agents and managing workflows.
It serves as the central hub of the TEC AI employee system.
"""
import os
import sys
import logging
import json
import time
import traceback
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agents.base_agent import BaseAgent
from src.agents.tecbot import TECBot
from src.agents.local_storage import LocalStorageAgent
from src.agents.clickup_agent import ClickUpAgent
from src.agents.wp_poster import WordPressAgent
from src.agents.airth_agent import AirthAgent

# Define error severity levels
ERROR_SEVERITY = {
    "CRITICAL": 4,  # System cannot continue, requires immediate attention
    "HIGH": 3,      # Feature is broken, requires prompt attention
    "MEDIUM": 2,    # Degraded functionality, should be fixed soon
    "LOW": 1,       # Minor issue, can be fixed in regular maintenance
    "INFO": 0       # Not an error, just informational
}


class OrchestratorAgent(BaseAgent):
    """
    OrchestratorAgent is the central coordinator for all TEC AI agents.
    It manages workflows, delegates tasks, and ensures proper coordination
    between different specialized agents in the system.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the orchestrator with all required sub-agents."""
        super().__init__("OrchestratorAgent", config_path)
        
        # Set up logging
        self.logger = logging.getLogger(f"astradigital.OrchestratorAgent")
        self.logger.info("Initializing OrchestratorAgent - central coordinator for TEC")

        # Load workflow configurations
        self.workflows = self._load_workflows()

        # Initialize all sub-agents
        self._init_agents(config_path)

        # Track active workflows
        self.active_workflows = {}

        # Initialize enhanced error tracking
        self.error_registry = {
            "last_errors": [],
            "error_counts": {},
            "error_history": {},
            "recovery_attempts": {},
            "system_health": {
                "overall_status": "healthy",
                "last_check": datetime.now().isoformat(),
                "component_status": {}
            }
        }

        # Set up recovery mechanisms
        self._setup_recovery_mechanisms()

        # Perform initial system health check
        self._check_system_health()

    def _init_agents(self, config_path: Optional[str] = None) -> None:
        """Initialize all sub-agents with proper error handling."""
        self.logger.info("Initializing all sub-agents")

        # Agent initialization with error tracking
        try:
            self.local_storage = LocalStorageAgent(config_path)
            self.logger.info("LocalStorageAgent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize LocalStorageAgent: {e}")
            self.local_storage = None
            self._register_error("LocalStorageAgent", "initialization", str(e))

        try:
            # Initialize WordPress agent
            self.wp_agent = WordPressAgent(config_path)
            self.logger.info("WordPress agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize WordPress agent: {e}")
            self.wp_agent = None
            self._register_error("WordPressAgent", "initialization", str(e))

        try:
            self.clickup_agent = ClickUpAgent(config_path)
            self.logger.info("ClickUpAgent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize ClickUpAgent: {e}")
            self.clickup_agent = None
            self._register_error("ClickUpAgent", "initialization", str(e))

        try:
            self.airth_agent = AirthAgent(config_path)
            self.logger.info("AirthAgent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize AirthAgent: {e}")
            self.airth_agent = None
            self._register_error("AirthAgent", "initialization", str(e))

        try:
            self.tecbot = TECBot(config_path)
            self.logger.info("TECBot initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize TECBot: {e}")
            self.tecbot = None
            self._register_error("TECBot", "initialization", str(e))

    def _load_workflows(self) -> Dict[str, Any]:
        """Load workflow definitions from the workflow config file."""
        workflows_path = project_root / "config" / "workflows.json"
        default_workflows = {
            "content_creation": {
                "steps": ["clickup_fetch", "content_generation", "wordpress_post", "clickup_update"],
                "error_handling": "retry",
                "max_retries": 3
            },
            "news_commentary": {
                "steps": ["news_fetch", "content_generation", "wordpress_post"],
                "error_handling": "continue",
                "max_retries": 2
            },
            "crypto_update": {
                "steps": ["crypto_fetch", "analysis", "wordpress_post"],
                "error_handling": "skip",
                "max_retries": 2
            }
        }

        try:
            if workflows_path.exists():
                with open(workflows_path, 'r') as f:
                    workflows = json.load(f)
                self.logger.info(f"Loaded workflow definitions from {workflows_path}")
                return workflows
            else:
                self.logger.warning(f"Workflow file not found: {workflows_path}, using defaults")
                # Create the default workflow file if it doesn't exist
                workflows_path.parent.mkdir(exist_ok=True)
                with open(workflows_path, 'w') as f:
                    json.dump(default_workflows, f, indent=2)
                self.logger.info(f"Created default workflow file at {workflows_path}")
                return default_workflows
        except Exception as e:
            self.logger.error(f"Failed to load workflows: {e}")
            return default_workflows

    def _register_error(self, agent_name: str, operation: str, error_message: str,
                        severity: str = "MEDIUM", recoverable: bool = True) -> Dict[str, Any]:
        """Register an error in the enhanced error tracking system."""
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "operation": operation,
            "message": error_message,
            "severity": severity,
            "severity_level": ERROR_SEVERITY.get(severity, 2),
            "recoverable": recoverable,
            "error_id": f"{agent_name}_{operation}_{int(time.time())}"
        }

        # Add to recent errors
        self.error_registry["last_errors"].append(error_record)
        if len(self.error_registry["last_errors"]) > 50:
            self.error_registry["last_errors"].pop(0)

        # Update error counts
        error_key = f"{agent_name}_{operation}"
        if error_key not in self.error_registry["error_counts"]:
            self.error_registry["error_counts"][error_key] = 0
        self.error_registry["error_counts"][error_key] += 1

        # Log the error
        if ERROR_SEVERITY.get(severity, 2) >= 3:
            self.logger.error(f"HIGH/CRITICAL ERROR in {agent_name}.{operation}: {error_message}")
        else:
            self.logger.warning(f"Error in {agent_name}.{operation}: {error_message}")

        return error_record

    def _setup_recovery_mechanisms(self) -> None:
        """Set up automatic recovery mechanisms for common errors."""
        self.logger.info("Setting up error recovery mechanisms")
        # This will be expanded with specific recovery strategies

    def _check_system_health(self) -> Dict[str, Any]:
        """Perform a comprehensive system health check."""
        self.logger.info("Performing system health check")
        
        health_status = {
            "overall_status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "errors": len(self.error_registry["last_errors"]),
            "critical_errors": len([e for e in self.error_registry["last_errors"] 
                                   if e.get("severity") == "CRITICAL"])
        }

        # Check each agent
        agents = {
            "local_storage": self.local_storage,
            "wp_agent": self.wp_agent,
            "clickup_agent": self.clickup_agent,
            "airth_agent": self.airth_agent,
            "tecbot": self.tecbot
        }

        for name, agent in agents.items():
            if agent is not None:
                health_status["components"][name] = "operational"
            else:
                health_status["components"][name] = "failed"
                health_status["overall_status"] = "degraded"

        # Update system health
        self.error_registry["system_health"] = health_status
        
        if health_status["overall_status"] == "healthy":
            self.logger.info("✅ System health check passed - all systems operational")
        else:
            self.logger.warning(f"⚠️ System health check shows degraded status: {health_status}")

        return health_status

    def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a named workflow with the provided parameters."""
        if workflow_name not in self.workflows:
            error_msg = f"Workflow '{workflow_name}' not found in available workflows"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        workflow = self.workflows[workflow_name]
        self.logger.info(f"🚀 Starting workflow: {workflow_name}")

        workflow_id = f"{workflow_name}_{int(time.time())}"
        self.active_workflows[workflow_id] = {
            "name": workflow_name,
            "status": "running",
            "start_time": datetime.now().isoformat(),
            "current_step": 0,
            "results": {}
        }

        try:
            results = {"success": True, "workflow_id": workflow_id, "steps": {}}
            
            for i, step in enumerate(workflow["steps"]):
                self.active_workflows[workflow_id]["current_step"] = i
                self.logger.info(f"📋 Executing step {i+1}/{len(workflow['steps'])}: {step}")
                
                step_result = self._execute_step(step, **kwargs)
                results["steps"][step] = step_result
                
                if not step_result.get("success", False):
                    self.logger.error(f"❌ Step {step} failed: {step_result.get('error', 'Unknown error')}")
                    
                    # Handle errors based on workflow configuration
                    error_handling = workflow.get("error_handling", "stop")
                    if error_handling == "stop":
                        results["success"] = False
                        break
                    elif error_handling == "retry":
                        # Implement retry logic here
                        pass
                    # Continue to next step if error_handling is "continue"

            # Update workflow status
            self.active_workflows[workflow_id]["status"] = "completed" if results["success"] else "failed"
            self.active_workflows[workflow_id]["end_time"] = datetime.now().isoformat()

            if results["success"]:
                self.logger.info(f"✅ Workflow {workflow_name} completed successfully")
            else:
                self.logger.error(f"❌ Workflow {workflow_name} failed")

            return results

        except Exception as e:
            self.logger.error(f"💥 Workflow {workflow_name} crashed: {str(e)}")
            self.active_workflows[workflow_id]["status"] = "crashed"
            self.active_workflows[workflow_id]["error"] = str(e)
            return {"success": False, "error": str(e), "workflow_id": workflow_id}

    def _execute_step(self, step_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a single workflow step."""
        try:
            if step_name == "news_fetch":
                return self._execute_news_fetch(**kwargs)
            elif step_name == "content_generation":
                return self._execute_content_generation(**kwargs)
            elif step_name == "wordpress_post":
                return self._execute_wordpress_post(**kwargs)
            elif step_name == "clickup_fetch":
                return self._execute_clickup_fetch(**kwargs)
            elif step_name == "clickup_update":
                return self._execute_clickup_update(**kwargs)
            else:
                return {"success": False, "error": f"Unknown step: {step_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_news_fetch(self, **kwargs) -> Dict[str, Any]:
        """Execute news fetching step."""
        if self.airth_agent:
            try:
                # Call Airth agent's news fetching capability
                result = self.airth_agent.fetch_news()
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": "AirthAgent not available"}

    def _execute_content_generation(self, **kwargs) -> Dict[str, Any]:
        """Execute content generation step."""
        if self.airth_agent:
            try:
                # Generate content using Airth agent
                content_source = kwargs.get("content_source", "news")
                result = self.airth_agent.generate_content(source=content_source)
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": "AirthAgent not available"}

    def _execute_wordpress_post(self, **kwargs) -> Dict[str, Any]:
        """Execute WordPress posting step."""
        if self.wp_agent:
            try:
                content = kwargs.get("content", {})
                result = self.wp_agent.publish_post(content)
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": "WordPressAgent not available"}

    def _execute_clickup_fetch(self, **kwargs) -> Dict[str, Any]:
        """Execute ClickUp task fetching step."""
        if self.clickup_agent:
            try:
                result = self.clickup_agent.get_tasks()
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": "ClickUpAgent not available"}

    def _execute_clickup_update(self, **kwargs) -> Dict[str, Any]:
        """Execute ClickUp task update step."""
        if self.clickup_agent:
            try:
                task_id = kwargs.get("task_id")
                updates = kwargs.get("updates", {})
                result = self.clickup_agent.update_task(task_id, updates)
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": "ClickUpAgent not available"}

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            "orchestrator": {
                "status": "operational",
                "active_workflows": len(self.active_workflows),
                "total_errors": len(self.error_registry["last_errors"])
            },
            "agents": {},
            "workflows": list(self.workflows.keys()),
            "system_health": self.error_registry["system_health"],
            "recent_errors": self.error_registry["last_errors"][-5:] if self.error_registry["last_errors"] else []
        }

        # Check agent status
        agents = {
            "local_storage": self.local_storage,
            "wordpress": self.wp_agent,
            "clickup": self.clickup_agent,
            "airth": self.airth_agent,
            "tecbot": self.tecbot
        }

        for name, agent in agents.items():
            status["agents"][name] = "operational" if agent else "unavailable"

        return status

    def shutdown(self) -> None:
        """Gracefully shutdown the orchestrator and all agents."""
        self.logger.info("🔄 Shutting down OrchestratorAgent...")
        
        # Cancel active workflows
        for workflow_id in self.active_workflows:
            if self.active_workflows[workflow_id]["status"] == "running":
                self.active_workflows[workflow_id]["status"] = "cancelled"
        
        self.logger.info("✅ OrchestratorAgent shutdown complete")


# Convenience function for quick testing
def test_orchestrator():
    """Test function to verify orchestrator functionality."""
    try:
        print("🧪 Testing OrchestratorAgent...")
        orchestrator = OrchestratorAgent()
        
        print("📊 Getting system status...")
        status = orchestrator.get_system_status()
        print(f"System Status: {status['orchestrator']['status']}")
        print(f"Available Agents: {list(status['agents'].keys())}")
        print(f"Available Workflows: {status['workflows']}")
        
        print("🏥 System health check...")
        health = orchestrator._check_system_health()
        print(f"Overall Health: {health['overall_status']}")
        
        print("✅ Orchestrator test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False


if __name__ == "__main__":
    test_orchestrator()
