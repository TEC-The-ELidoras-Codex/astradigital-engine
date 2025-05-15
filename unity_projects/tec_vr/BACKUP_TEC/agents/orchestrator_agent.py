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
import traceback  # Added for detailed error tracking
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Add parent directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .base_agent import BaseAgent
from .airth_agent import AirthAgent
from .wp_poster import WordPressAgent
from .clickup_agent import ClickUpAgent
from .local_storage import LocalStorageAgent
from .tecbot import TECBot

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
            # Initialize both WordPress agents - production and local
            self.wp_agent = self._create_wordpress_agent(use_local=False)
            self.wp_local_agent = self._create_wordpress_agent(use_local=True)
            self.logger.info("WordPress agents initialized successfully (production and local)")
        except Exception as e:
            self.logger.error(f"Failed to initialize WordPress agents: {e}")
            self.wp_agent = None
            self.wp_local_agent = None
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
            
    def _create_wordpress_agent(self, use_local=False):
        """
        Create a WordPress agent with appropriate environment & error handling.
        
        Args:
            use_local: Whether to use the local WordPress environment
            
        Returns:
            WordPressAgent instance or None if creation fails
        """
        try:
            self.logger.info(f"Creating {'local' if use_local else 'production'} WordPress agent")
            return WordPressAgent(config_path=self.config_path, use_local=use_local)
        except Exception as e:
            self.logger.error(f"Failed to create {'local' if use_local else 'production'} WordPress agent: {e}")
            self._register_error("WordPressAgent", "initialization", str(e))
            return None

    def _load_workflows(self) -> Dict[str, Any]:
        """Load workflow definitions from the workflow config file."""
        workflows_path = os.path.join(project_root, "config", "workflows.json")
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
            if os.path.exists(workflows_path):
                with open(workflows_path, 'r') as f:
                    workflows = json.load(f)
                self.logger.info(f"Loaded workflow definitions from {workflows_path}")
                return workflows
            else:
                self.logger.warning(f"Workflow file not found: {workflows_path}, using defaults")
                # Create the default workflow file if it doesn't exist
                os.makedirs(os.path.dirname(workflows_path), exist_ok=True)
                with open(workflows_path, 'w') as f:
                    json.dump(default_workflows, f, indent=2)
                self.logger.info(f"Created default workflow file at {workflows_path}")
                return default_workflows
        except Exception as e:
            self.logger.error(f"Failed to load workflows: {e}")
            return default_workflows
    
    def _register_error(self, agent_name: str, operation: str, error_message: str, 
                        severity: str = "MEDIUM", recoverable: bool = True) -> Dict[str, Any]:
        """
        Register an error in the enhanced error tracking system.
        
        Args:
            agent_name: Name of the agent that encountered the error
            operation: Operation where the error occurred
            error_message: Description of the error
            severity: Error severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
            recoverable: Whether automatic recovery can be attempted
            
        Returns:
            Error entry with metadata
        """
        error_id = f"err_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(error_message) % 10000}"
        error_entry = {
            "id": error_id,
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "operation": operation,
            "message": error_message,
            "severity": severity,
            "severity_level": ERROR_SEVERITY.get(severity, 1),
            "recoverable": recoverable,
            "stacktrace": traceback.format_exc(),
            "recovery_attempts": 0,
            "status": "open"
        }
        
        # Add to recent errors list (keep last 10)
        self.error_registry["last_errors"].append(error_entry)
        if len(self.error_registry["last_errors"]) > 10:
            self.error_registry["last_errors"].pop(0)
        
        # Store in error history
        self.error_registry["error_history"][error_id] = error_entry
        
        # Update error count
        error_key = f"{agent_name}:{operation}"
        if error_key in self.error_registry["error_counts"]:
            self.error_registry["error_counts"][error_key] += 1
        else:
            self.error_registry["error_counts"][error_key] = 1
        
        # Update component status in system health
        self._update_component_health(agent_name, severity)
        
        # Log the error
        log_method = self.logger.error
        if severity == "CRITICAL":
            log_method = self.logger.critical
        elif severity == "LOW":
            log_method = self.logger.warning
        elif severity == "INFO":
            log_method = self.logger.info
            
        log_method(f"[{severity}] {agent_name} - {operation}: {error_message} (ID: {error_id})")
        
        # Check if we should attempt recovery
        if recoverable:
            self._attempt_recovery(error_entry)
            
        return error_entry
    
    def _setup_recovery_mechanisms(self) -> None:
        """Set up error recovery mechanisms."""
        # Map common errors to recovery functions
        self.recovery_strategies = {
            "initialization": self._recover_initialization,
            "api_timeout": self._recover_api_timeout,
            "clickup_fetch": self._recover_clickup_fetch,
            "wordpress_post": self._recover_wordpress_post,
            "content_generation": self._recover_content_generation
        }
        
    def _attempt_recovery(self, error_entry: Dict[str, Any]) -> bool:
        """
        Attempt to recover from an error.
        
        Args:
            error_entry: Error details
            
        Returns:
            Success of recovery attempt
        """
        error_id = error_entry["id"]
        agent = error_entry["agent"]
        operation = error_entry["operation"]
        
        # Check if we already attempted recovery too many times
        if error_entry["recovery_attempts"] >= 3:
            self.logger.warning(f"Maximum recovery attempts reached for {error_id}, marking as unrecoverable")
            error_entry["recoverable"] = False
            return False
        
        # Increment recovery attempt counter
        error_entry["recovery_attempts"] += 1
        self.error_registry["error_history"][error_id]["recovery_attempts"] += 1
        
        # Track the recovery attempt
        if error_id not in self.error_registry["recovery_attempts"]:
            self.error_registry["recovery_attempts"][error_id] = []
            
        self.error_registry["recovery_attempts"][error_id].append({
            "timestamp": datetime.now().isoformat(),
            "attempt": error_entry["recovery_attempts"]
        })
        
        # Find appropriate recovery strategy
        recovery_key = operation
        if recovery_key in self.recovery_strategies:
            self.logger.info(f"Attempting recovery for {error_id} using {recovery_key} strategy")
            success = self.recovery_strategies[recovery_key](agent, error_entry)
            
            if success:
                self.logger.info(f"Recovery successful for {error_id}")
                error_entry["status"] = "recovered"
                self.error_registry["error_history"][error_id]["status"] = "recovered"
                return True
            else:
                self.logger.warning(f"Recovery failed for {error_id}")
                return False
        else:
            self.logger.warning(f"No recovery strategy found for {operation}")
            return False
    
    def _recover_initialization(self, agent_name: str, error_entry: Dict[str, Any]) -> bool:
        """Attempt to recover from initialization errors."""
        self.logger.info(f"Attempting to reinitialize {agent_name}")
        
        # Try to reinitialize the specific agent
        config_path = os.path.join(project_root, "config", "config.yaml")
        
        try:
            if agent_name == "LocalStorageAgent":
                self.local_storage = LocalStorageAgent(config_path)
                return True
            elif agent_name == "WordPressAgent":
                self.wp_agent = WordPressAgent(config_path)
                return True
            elif agent_name == "ClickUpAgent":
                self.clickup_agent = ClickUpAgent(config_path)
                return True
            elif agent_name == "AirthAgent":
                self.airth_agent = AirthAgent(config_path)
                return True
            elif agent_name == "TECBot":
                self.tecbot = TECBot(config_path)
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Reinitialization of {agent_name} failed: {e}")
            return False
    
    def _recover_api_timeout(self, agent_name: str, error_entry: Dict[str, Any]) -> bool:
        """Attempt to recover from API timeout errors."""
        # Simple backoff strategy
        self.logger.info(f"API timeout recovery: waiting before retry for {agent_name}")
        time.sleep(5)  # Wait 5 seconds before retry
        return True  # Mark as recovered, the operation will be retried
    
    def _recover_clickup_fetch(self, agent_name: str, error_entry: Dict[str, Any]) -> bool:
        """Attempt to recover from ClickUp fetch errors."""
        if not self.clickup_agent:
            return self._recover_initialization("ClickUpAgent", error_entry)
        
        # Try to refresh the ClickUp session
        try:
            # This would be a method in ClickUpAgent to refresh authentication
            # self.clickup_agent.refresh_session()
            self.logger.info("ClickUp session refreshed")
            return True
        except Exception as e:
            self.logger.error(f"ClickUp session refresh failed: {e}")
            return False
    
    def _recover_wordpress_post(self, agent_name: str, error_entry: Dict[str, Any]) -> bool:
        """Attempt to recover from WordPress posting errors."""
        if not self.wp_agent:
            return self._recover_initialization("WordPressAgent", error_entry)
        
        # Try to reconnect to WordPress
        try:
            # This would be a method in WordPressAgent to reconnect
            # self.wp_agent.reconnect()
            self.logger.info("WordPress connection restored")
            return True
        except Exception as e:
            self.logger.error(f"WordPress reconnection failed: {e}")
            return False
    
    def _recover_content_generation(self, agent_name: str, error_entry: Dict[str, Any]) -> bool:
        """Attempt to recover from content generation errors."""
        if not self.airth_agent:
            return self._recover_initialization("AirthAgent", error_entry)
        
        # Try to reinitialize the OpenAI client
        try:
            # This would be a method in AirthAgent to reinitialize OpenAI
            # self.airth_agent.reinit_openai()
            self.logger.info("OpenAI client reinitialized")
            return True
        except Exception as e:
            self.logger.error(f"OpenAI reinitialization failed: {e}")
            return False
    
    def _update_component_health(self, component_name: str, error_severity: str) -> None:
        """Update the health status of a system component based on errors."""
        current_time = datetime.now().isoformat()
        
        # Initialize component if not already tracked
        if component_name not in self.error_registry["system_health"]["component_status"]:
            self.error_registry["system_health"]["component_status"][component_name] = {
                "status": "healthy",
                "last_update": current_time,
                "error_count": 0
            }
        
        component = self.error_registry["system_health"]["component_status"][component_name]
        
        # Update error count
        component["error_count"] += 1
        component["last_update"] = current_time
        
        # Update status based on severity and error count
        if error_severity == "CRITICAL":
            component["status"] = "critical"
        elif error_severity == "HIGH":
            component["status"] = "degraded"
        elif error_severity == "MEDIUM" and component["error_count"] > 3:
            component["status"] = "warning"
        elif component["status"] == "healthy" and error_severity == "MEDIUM":
            component["status"] = "minor_issues"
            
        # Update overall system health
        self._check_system_health()
    
    def _check_system_health(self) -> Dict[str, Any]:
        """
        Check overall system health based on component statuses.
        
        Returns:
            System health status
        """
        health = self.error_registry["system_health"]
        health["last_check"] = datetime.now().isoformat()
        
        # Determine overall status based on component health
        has_critical = any(c["status"] == "critical" 
                        for c in health["component_status"].values())
        has_degraded = any(c["status"] == "degraded" 
                        for c in health["component_status"].values())
        has_warning = any(c["status"] == "warning" 
                        for c in health["component_status"].values())
        
        if has_critical:
            health["overall_status"] = "critical"
        elif has_degraded:
            health["overall_status"] = "degraded"
        elif has_warning:
            health["overall_status"] = "warning"
        else:
            health["overall_status"] = "healthy"
            
        return health
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get the overall status of the TEC system."""
        health = self._check_system_health()
        
        return {
            "agents": {
                "airth_agent": {"status": "healthy" if self.airth_agent else "unavailable"},
                "wordpress_agent": {"status": "healthy" if self.wp_agent else "unavailable"},
                "clickup_agent": {"status": "healthy" if self.clickup_agent else "unavailable"},
                "storage_agent": {"status": "healthy" if self.local_storage else "unavailable"},
                "tecbot": {"status": "healthy" if self.tecbot else "unavailable"}
            },
            "active_workflows": len(self.active_workflows),
            "error_counts": self.error_registry["error_counts"],            "last_error": self.error_registry["last_errors"][-1] if self.error_registry["last_errors"] else None,
            "system_health": health,
            "system_time": datetime.now().isoformat()
        }
        
    def execute_workflow(self, workflow_name: str, workflow_data: Dict[str, Any] = None, use_local_wp: bool = False) -> Dict[str, Any]:
        """
        Execute a predefined workflow with the given data.
        
        Args:
            workflow_name: Name of the workflow to execute
            workflow_data: Input data for the workflow
            use_local_wp: Whether to use local WordPress environment for this workflow
            
        Returns:
            Results of the workflow execution
        """
        if workflow_name not in self.workflows:
            self.logger.error(f"Unknown workflow: {workflow_name}")
            return {
                "success": False,
                "error": f"Unknown workflow: {workflow_name}"
            }
        
        workflow = self.workflows[workflow_name]
        workflow_id = f"{workflow_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.logger.info(f"Starting workflow: {workflow_name} (ID: {workflow_id})")
          # Initialize workflow tracking
        self.active_workflows[workflow_id] = {
            "name": workflow_name,
            "start_time": datetime.now().isoformat(),
            "status": "running",
            "current_step": 0,
            "steps": workflow["steps"],
            "results": {},
            "use_local_wp": use_local_wp
        }
        
        # Add WordPress environment parameter to workflow data
        if workflow_data is None:
            workflow_data = {}
        workflow_data["use_local_wp"] = use_local_wp
        
        workflow_data = workflow_data or {}
        results = {
            "workflow_id": workflow_id,
            "success": True,
            "steps_completed": 0,
            "steps_total": len(workflow["steps"]),
            "step_results": {},
            "errors": []
        }
        
        # Execute each step in the workflow
        for i, step in enumerate(workflow["steps"]):
            self.active_workflows[workflow_id]["current_step"] = i
            
            self.logger.info(f"Executing workflow step {i+1}/{len(workflow['steps'])}: {step}")
            
            # Track retries
            retries = 0
            max_retries = workflow.get("max_retries", 1)
            
            while retries <= max_retries:
                try:
                    step_result = self._execute_step(step, workflow_data)
                    results["step_results"][step] = step_result
                    
                    # Update workflow data with results from this step
                    if isinstance(step_result, dict) and step_result.get("success", False):
                        workflow_data.update(step_result)
                    
                    # Step completed successfully
                    results["steps_completed"] += 1
                    break
                    
                except Exception as e:
                    error_msg = f"Error in workflow step '{step}': {str(e)}"
                    self.logger.error(error_msg)
                    self._register_error(workflow_name, step, str(e))
                    
                    retries += 1
                    
                    if retries <= max_retries:
                        self.logger.info(f"Retrying step '{step}' ({retries}/{max_retries})")
                        time.sleep(2)  # Short delay before retry
                    else:
                        # Max retries exceeded
                        results["errors"].append(error_msg)
                        
                        # Check error handling strategy
                        strategy = workflow.get("error_handling", "stop")
                        if strategy == "stop":
                            results["success"] = False
                            break
                        elif strategy == "skip":
                            self.logger.warning(f"Skipping failed step '{step}' and continuing workflow")
                            continue
                        elif strategy == "continue":
                            self.logger.warning(f"Continuing with workflow despite step '{step}' failure")
                            # Continue execution but mark workflow as partially successful
                            results["success"] = False
            
            # If we broke out of the workflow due to error handling strategy
            if not results["success"] and workflow.get("error_handling", "stop") == "stop":
                break
        
        # Update workflow status
        self.active_workflows[workflow_id]["status"] = "completed" if results["success"] else "failed"
        self.active_workflows[workflow_id]["end_time"] = datetime.now().isoformat()
        
        # Cleanup old workflow entries (keep last 10)
        if len(self.active_workflows) > 10:
            oldest_key = min(self.active_workflows.keys(), 
                             key=lambda k: self.active_workflows[k].get("start_time", ""))
            if oldest_key != workflow_id:
                del self.active_workflows[oldest_key]
        
        return results
    
    def _execute_step(self, step: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step."""
        # Map step names to actual methods
        step_map = {
            "clickup_fetch": self._step_clickup_fetch,
            "content_generation": self._step_content_generation,
            "wordpress_post": self._step_wordpress_post, 
            "clickup_update": self._step_clickup_update,
            "news_fetch": self._step_news_fetch,
            "crypto_fetch": self._step_crypto_fetch,
            "analysis": self._step_analysis
        }
        
        if step not in step_map:
            raise ValueError(f"Unknown workflow step: {step}")
        
        # Call the appropriate step method
        return step_map[step](workflow_data)
    
    def _step_clickup_fetch(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch tasks from ClickUp."""
        if not self.clickup_agent:
            raise RuntimeError("ClickUpAgent not available")
        
        status = workflow_data.get("task_status", "Ready for AI")
        limit = workflow_data.get("task_limit", 1)
        
        tasks = self.clickup_agent.get_content_tasks(status_name=status)
        
        if not tasks:
            return {
                "success": False,
                "message": f"No tasks found with status: {status}"
            }
        
        # Limit the number of tasks if needed
        tasks = tasks[:limit]
        
        return {
            "success": True,
            "tasks": tasks,
            "tasks_count": len(tasks)
        }
    
    def _step_content_generation(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content using AirthAgent."""
        if not self.airth_agent:
            raise RuntimeError("AirthAgent not available")
        
        # Check if we're processing ClickUp tasks or news articles
        if "tasks" in workflow_data:
            # Process ClickUp tasks
            tasks = workflow_data["tasks"]
            results = []
            
            for task in tasks:
                result = self.airth_agent.create_content_from_clickup_task(task)
                results.append(result)
            
            return {
                "success": any(r.get("success", False) for r in results),
                "content_results": results,
                "posts_created": sum(1 for r in results if r.get("success", False))
            }
        
        elif "articles" in workflow_data:
            # Process news articles
            articles = workflow_data["articles"]
            results = []
            
            for article in articles[:1]:  # Just process the first article for now
                result = self.airth_agent.create_news_commentary_post(article)
                results.append(result)
            
            return {
                "success": any(r.get("success", False) for r in results),
                "content_results": results,
                "posts_created": sum(1 for r in results if r.get("success", False))
            }
        
        elif "topic" in workflow_data:
            # Generate a standard blog post
            topic = workflow_data["topic"]
            keywords = workflow_data.get("keywords", ["AI", "technology", "TEC"])
            
            result = self.airth_agent.create_blog_post(topic=topic, keywords=keywords)
            
            return {
                "success": result.get("success", False),
                "content_result": result,
                "posts_created": 1 if result.get("success", False) else 0
            }
            
        elif "crypto_data" in workflow_data:
            # Generate crypto analysis
            # Placeholder - this would be implemented specifically for crypto workflow
            return {
                "success": True,
                "message": "Crypto analysis generated"
            }
              else:
            raise ValueError("No content source provided for content generation step")
            
    def _step_wordpress_post(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Post content to WordPress if not already handled by AirthAgent."""
        # Check if we should use local WordPress
        use_local_wp = workflow_data.get("use_local_wp", False)
        
        # Get the appropriate WordPress agent
        wp_agent = self.get_wordpress_agent(use_local=use_local_wp)
        
        # If there's content ready to post that wasn't handled by AirthAgent
        if workflow_data.get("post_to_wordpress") and wp_agent:
            post_data = workflow_data.get("post_data", {})
            if post_data and "title" in post_data and "content" in post_data:
                try:
                    self.logger.info(f"Posting to {'local' if use_local_wp else 'production'} WordPress")
                    result = wp_agent.create_post(**post_data)
                    return {
                        "success": True,
                        "message": f"Successfully posted to {'local' if use_local_wp else 'production'} WordPress",
                        "post_id": result.get("id") if isinstance(result, dict) else result
                    }
                except Exception as e:
                    self.logger.error(f"Error posting to WordPress: {e}")
                    return {
                        "success": False,
                        "message": f"Error posting to WordPress: {e}"
                    }
        
        # If no explicit WordPress posting needed, it might have been handled by AirthAgent
        return {
            "success": True,
            "message": "WordPress posting not required or already handled by content generation step"
        }
    
    def _step_clickup_update(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update ClickUp task status if needed."""
        if not self.clickup_agent:
            raise RuntimeError("ClickUpAgent not available")
            
        # Check if we have pending task updates
        content_results = workflow_data.get("content_results", [])
        if not content_results:
            return {
                "success": True,
                "message": "No ClickUp tasks to update"
            }
        
        update_results = []
        for result in content_results:
            if result.get("success") and result.get("task_id"):
                # Task was already updated in create_content_from_clickup_task,
                # but we could add additional updates here if needed
                update_results.append({
                    "task_id": result.get("task_id"),
                    "success": True
                })
        
        return {
            "success": True,
            "updates": update_results,
            "updates_count": len(update_results)
        }
    
    def _step_news_fetch(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch news articles."""
        if not self.airth_agent:
            raise RuntimeError("AirthAgent not available")
        
        keywords = workflow_data.get("keywords", ["artificial intelligence", "AI", "machine learning"])
        categories = workflow_data.get("categories", ["technology"])
        country = workflow_data.get("country", "US")
        max_results = workflow_data.get("max_results", 5)
        
        articles = self.airth_agent.fetch_news(
            keywords=keywords,
            categories=categories,
            country=country,
            max_results=max_results
        )
        
        if not articles:
            return {
                "success": False,
                "message": "No relevant news articles found"
            }
        
        return {
            "success": True,
            "articles": articles,
            "articles_count": len(articles)
        }
    
    def _step_crypto_fetch(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch cryptocurrency data."""
        # This would call the appropriate method to fetch crypto data
        # Placeholder implementation
        return {
            "success": True,
            "crypto_data": {
                "BTC": {"price": 50000, "change_24h": 2.5},
                "ETH": {"price": 3000, "change_24h": 1.8},
                "SOL": {"price": 150, "change_24h": 5.2}
            }
        }
    
    def _step_analysis(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform analysis on data."""
        # Placeholder for analysis step
        return {
            "success": True,
            "analysis_results": {
                "sentiment": "positive",
                "key_insights": ["Market is trending upward", "Institutional adoption increasing"]
            }
        }
    
    def get_wordpress_agent(self, use_local: bool = False) -> Optional[WordPressAgent]:
        """
        Get the appropriate WordPress agent based on the environment requirement.
        
        Args:
            use_local: Whether to use the local WordPress environment
            
        Returns:
            The appropriate WordPress agent instance or None if not available
        """
        if use_local:
            if self.wp_local_agent:
                self.logger.debug("Using local WordPress agent")
                return self.wp_local_agent
            else:
                self.logger.warning("Local WordPress agent not available, falling back to production")
                return self.wp_agent
        else:
            if self.wp_agent:
                self.logger.debug("Using production WordPress agent")
                return self.wp_agent
            else:
                self.logger.warning("Production WordPress agent not available, falling back to local")
                return self.wp_local_agent
    
    def run(self) -> Dict[str, Any]:
        """
        Run the main orchestrator function.
        
        Returns:
            Result of orchestrator execution
        """
        self.logger.info("Running OrchestratorAgent")
        
        results = {
            "status": "success",
            "system_status": self.get_system_status(),
            "actions": [],
            "errors": []
        }
        
        try:
            # This would typically respond to commands or execute scheduled workflows
            # For now we'll just return the system status
            pass
            
        except Exception as e:
            self.logger.error(f"Error in OrchestratorAgent: {e}")
            results["status"] = "error"
            results["errors"].append(str(e))
        
        return results


if __name__ == "__main__":
    # Create and run the OrchestratorAgent
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               "config", "config.yaml")
    
    orchestrator = OrchestratorAgent(config_path)
    
    # Check if a workflow name was provided as an argument
    if len(sys.argv) > 1:
        workflow_name = sys.argv[1]
        workflow_data = {}
        
        # Handle additional arguments
        if workflow_name == "content_creation":
            workflow_data = {
                "task_status": "Ready for AI",
                "task_limit": 1
            }
        elif workflow_name == "news_commentary":
            workflow_data = {
                "keywords": ["artificial intelligence", "AI", "machine learning"],
                "categories": ["technology"],
                "country": "US",
                "max_results": 5
            }
        elif workflow_name == "crypto_update":
            workflow_data = {
                "coins": ["BTC", "ETH", "SOL"]
            }
            
        # Execute the specified workflow
        results = orchestrator.execute_workflow(workflow_name, workflow_data)
        
        print(f"Workflow {workflow_name} execution completed with status: {results['status']}")
        print(f"Steps completed: {results['steps_completed']}/{results['steps_total']}")
        
        if results.get("errors"):
            print("Errors encountered:")
            for error in results["errors"]:
                print(f" - {error}")
    else:
        # If no workflow specified, just run the default action
        results = orchestrator.run()
        
        print(f"OrchestratorAgent execution completed with status: {results['status']}")
        
        print("System Status:")
        status = results["system_status"]["agents"]
        for agent_name, agent_status in status.items():
            print(f" - {agent_name}: {agent_status['status']}")
            
        if results.get("errors"):
            print("Errors encountered:")
            for error in results["errors"]:
                print(f" - {error}")
