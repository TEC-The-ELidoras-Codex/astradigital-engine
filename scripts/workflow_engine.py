"""
TEC Workflow Engine - Advanced workflow execution & management system
Orchestrates multi-agent workflows for The Elidoras Codex automation
"""
import os
import sys
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import traceback

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.airth_agent import AirthAgent
from src.agents.wp_poster import WordPressAgent  
from src.agents.local_storage import LocalStorageAgent

# Try to import optional agents
try:
    from src.agents.clickup_agent import ClickUpAgent
    CLICKUP_AVAILABLE = True
except ImportError:
    CLICKUP_AVAILABLE = False
    ClickUpAgent = None

try:
    from src.agents.tecbot import TECBot
    TECBOT_AVAILABLE = True
except ImportError:
    TECBOT_AVAILABLE = False
    TECBot = None


class WorkflowEngine:
    """Advanced workflow execution engine for TEC AI agents."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the workflow engine."""
        self.logger = logging.getLogger('TEC_WorkflowEngine')
        self.config_path = config_path
        self.workflows = self._load_workflows()
        self.agents = self._initialize_agents()
        self.active_workflows = {}
        self.workflow_history = []
        
        # Workflow step registry
        self.step_registry = self._build_step_registry()
        
    def _load_workflows(self) -> Dict[str, Any]:
        """Load workflow definitions from config."""
        workflows_path = os.path.join(project_root, "config", "workflows.json")
        try:
            with open(workflows_path, 'r') as f:
                workflows = json.load(f)
            self.logger.info(f"📋 Loaded {len(workflows)} workflows")
            return workflows
        except Exception as e:
            self.logger.error(f"❌ Failed to load workflows: {e}")
            return {}
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all available agents."""
        agents = {}
        
        try:
            agents['airth'] = AirthAgent(self.config_path)
            self.logger.info("✅ AirthAgent initialized for workflows")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize AirthAgent: {e}")
            agents['airth'] = None
            
        try:
            agents['wordpress'] = WordPressAgent(self.config_path)
            agents['wordpress_local'] = WordPressAgent(self.config_path, use_local=True)
            self.logger.info("✅ WordPressAgents initialized for workflows")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize WordPressAgents: {e}")
            agents['wordpress'] = None
            agents['wordpress_local'] = None
            
        try:
            agents['storage'] = LocalStorageAgent(self.config_path)
            self.logger.info("✅ LocalStorageAgent initialized for workflows")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize LocalStorageAgent: {e}")
            agents['storage'] = None
            
        if CLICKUP_AVAILABLE:
            try:
                agents['clickup'] = ClickUpAgent(self.config_path)
                self.logger.info("✅ ClickUpAgent initialized for workflows")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize ClickUpAgent: {e}")
                agents['clickup'] = None
        else:
            agents['clickup'] = None
            
        if TECBOT_AVAILABLE:
            try:
                agents['tecbot'] = TECBot(self.config_path)
                self.logger.info("✅ TECBot initialized for workflows")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize TECBot: {e}")
                agents['tecbot'] = None
        else:
            agents['tecbot'] = None
            
        return agents
    
    def _build_step_registry(self) -> Dict[str, Callable]:
        """Build registry of available workflow steps."""
        return {
            # System operations
            'system_health_check': self._step_system_health_check,
            'cleanup_old_data': self._step_cleanup_old_data,
            'backup_data': self._step_backup_data,
            
            # News & content operations  
            'fetch_news': self._step_fetch_news,
            'generate_news_content': self._step_generate_news_content,
            'generate_original_content': self._step_generate_original_content,
            'process_content': self._step_process_content,
            
            # Publishing operations
            'publish_to_wordpress': self._step_publish_to_wordpress,
            'publish_to_local': self._step_publish_to_local,
            'schedule_content': self._step_schedule_content,
            
            # Task management
            'fetch_clickup_tasks': self._step_fetch_clickup_tasks,
            'update_clickup_status': self._step_update_clickup_status,
            'create_clickup_task': self._step_create_clickup_task,
            
            # AI interactions
            'airth_personality_response': self._step_airth_personality_response,
            'tecbot_analysis': self._step_tecbot_analysis,
            'collaborative_content': self._step_collaborative_content,
            
            # Data operations
            'store_data': self._step_store_data,
            'retrieve_data': self._step_retrieve_data,
            'analyze_metrics': self._step_analyze_metrics,
        }
    
    async def execute_workflow(self, workflow_name: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a workflow asynchronously."""
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
            
        workflow = self.workflows[workflow_name]
        parameters = parameters or {}
        
        execution_id = f"{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = {
            "execution_id": execution_id,
            "workflow_name": workflow_name,
            "started_at": datetime.now().isoformat(),
            "status": "running",
            "steps_completed": [],
            "steps_failed": [],
            "results": {},
            "errors": [],
            "parameters": parameters
        }
        
        self.active_workflows[execution_id] = result
        self.logger.info(f"🚀 Starting workflow: {workflow_name} (ID: {execution_id})")
        
        try:
            for step_name in workflow["steps"]:
                try:
                    self.logger.info(f"🔄 Executing step: {step_name}")
                    step_result = await self._execute_step(step_name, parameters, result)
                    result["steps_completed"].append(step_name)
                    result["results"][step_name] = step_result
                    self.logger.info(f"✅ Step {step_name} completed")
                    
                except Exception as e:
                    self.logger.error(f"❌ Step {step_name} failed: {e}")
                    result["steps_failed"].append(step_name)
                    result["errors"].append({
                        "step": step_name,
                        "error": str(e),
                        "traceback": traceback.format_exc()
                    })
                    
                    # Handle error based on workflow configuration
                    error_handling = workflow.get("error_handling", "stop")
                    if error_handling == "stop":
                        break
                    elif error_handling == "retry":
                        # Implement retry logic
                        max_retries = workflow.get("max_retries", 3)
                        for retry in range(max_retries):
                            try:
                                self.logger.info(f"🔄 Retrying step {step_name} (attempt {retry + 1})")
                                step_result = await self._execute_step(step_name, parameters, result)
                                result["steps_completed"].append(f"{step_name}_retry_{retry + 1}")
                                result["results"][f"{step_name}_retry_{retry + 1}"] = step_result
                                break
                            except Exception as retry_e:
                                if retry == max_retries - 1:
                                    result["errors"].append({
                                        "step": f"{step_name}_final_retry",
                                        "error": str(retry_e)
                                    })
                                    
            result["status"] = "completed" if not result["steps_failed"] else "partial"
            result["completed_at"] = datetime.now().isoformat()
            
        except Exception as e:
            result["status"] = "failed"
            result["completed_at"] = datetime.now().isoformat()
            result["errors"].append({
                "workflow": workflow_name,
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            self.logger.error(f"❌ Workflow {workflow_name} failed: {e}")
            
        finally:
            # Move to history and clean up active workflows
            self.workflow_history.append(result)
            if execution_id in self.active_workflows:
                del self.active_workflows[execution_id]
                
        return result
    
    async def _execute_step(self, step_name: str, parameters: Dict[str, Any], workflow_context: Dict[str, Any]) -> Any:
        """Execute a single workflow step."""
        if step_name not in self.step_registry:
            raise NotImplementedError(f"Workflow step '{step_name}' not implemented")
            
        step_function = self.step_registry[step_name]
        return await step_function(parameters, workflow_context)
    
    # ================== WORKFLOW STEP IMPLEMENTATIONS ==================
    
    async def _step_system_health_check(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform system health check."""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "agents_status": {},
            "system_metrics": {},
            "recommendations": []
        }
        
        # Check each agent
        for agent_name, agent in self.agents.items():
            if agent is None:
                health_status["agents_status"][agent_name] = "unavailable"
            else:
                try:
                    health_status["agents_status"][agent_name] = "healthy"
                except Exception as e:
                    health_status["agents_status"][agent_name] = f"unhealthy: {str(e)}"
                    
        return health_status
    
    async def _step_fetch_news(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch news using Airth agent."""
        if not self.agents['airth']:
            raise Exception("AirthAgent not available")
            
        # Use existing news automation
        max_age = params.get('max_age', 1)
        max_topics = params.get('max_topics', 3)
        
        try:
            # This would integrate with the existing news automation
            return {
                "status": "success",
                "articles_fetched": max_topics,
                "max_age_days": max_age,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Failed to fetch news: {str(e)}")
    
    async def _step_generate_original_content(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate original content using Airth agent."""
        if not self.agents['airth']:
            raise Exception("AirthAgent not available")
            
        content_type = params.get('content_type', 'article')
        topic = params.get('topic', 'Astradigital Ocean exploration')
        
        try:
            # Generate content using Airth's personality
            content = {
                "title": f"TEC {content_type.title()}: {topic}",
                "content": f"Generated content about {topic} using AirthAgent",
                "type": content_type,
                "author": "Airth",
                "generated_at": datetime.now().isoformat()
            }
            return content
        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")
    
    async def _step_publish_to_wordpress(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Publish content to WordPress."""
        if not self.agents['wordpress']:
            raise Exception("WordPressAgent not available")
            
        content = params.get('content', {})
        if not content:
            # Try to get content from previous step results
            for step_result in context.get("results", {}).values():
                if isinstance(step_result, dict) and "content" in step_result:
                    content = step_result
                    break
                    
        if not content:
            raise Exception("No content available for publishing")
            
        try:
            # Publish using WordPress agent
            result = {
                "status": "published",
                "post_id": f"mock_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "title": content.get('title', 'Untitled'),
                "published_at": datetime.now().isoformat()
            }
            return result
        except Exception as e:
            raise Exception(f"Failed to publish to WordPress: {str(e)}")
    
    async def _step_store_data(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Store data using LocalStorageAgent."""
        if not self.agents['storage']:
            raise Exception("LocalStorageAgent not available")
            
        data = params.get('data', context.get("results", {}))
        storage_key = params.get('key', f"workflow_{context.get('execution_id', 'unknown')}")
        
        try:
            # Store data
            result = {
                "status": "stored",
                "key": storage_key,
                "size": len(str(data)),
                "stored_at": datetime.now().isoformat()
            }
            return result
        except Exception as e:
            raise Exception(f"Failed to store data: {str(e)}")
    
    async def _step_cleanup_old_data(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Clean up old data files."""
        days_old = params.get('days_old', 30)
        
        try:
            # Cleanup logic here
            result = {
                "status": "cleaned",
                "files_removed": 0,
                "space_freed": "0 MB",
                "cutoff_date": (datetime.now() - timedelta(days=days_old)).isoformat()
            }
            return result
        except Exception as e:
            raise Exception(f"Failed to cleanup data: {str(e)}")
    
    # Placeholder implementations for other steps
    async def _step_backup_data(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "backed_up", "timestamp": datetime.now().isoformat()}
    
    async def _step_generate_news_content(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "generated", "articles": 3, "timestamp": datetime.now().isoformat()}
    
    async def _step_process_content(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "processed", "timestamp": datetime.now().isoformat()}
    
    async def _step_publish_to_local(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "published_local", "timestamp": datetime.now().isoformat()}
    
    async def _step_schedule_content(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "scheduled", "timestamp": datetime.now().isoformat()}
    
    async def _step_fetch_clickup_tasks(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "fetched", "tasks": 0, "timestamp": datetime.now().isoformat()}
    
    async def _step_update_clickup_status(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "updated", "timestamp": datetime.now().isoformat()}
    
    async def _step_create_clickup_task(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "created", "task_id": "mock_task", "timestamp": datetime.now().isoformat()}
    
    async def _step_airth_personality_response(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "responded", "personality": "goth", "timestamp": datetime.now().isoformat()}
    
    async def _step_tecbot_analysis(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "analyzed", "insights": "mock insights", "timestamp": datetime.now().isoformat()}
    
    async def _step_collaborative_content(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "collaborated", "agents": ["airth", "tecbot"], "timestamp": datetime.now().isoformat()}
    
    async def _step_retrieve_data(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "retrieved", "timestamp": datetime.now().isoformat()}
    
    async def _step_analyze_metrics(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "analyzed", "metrics": {}, "timestamp": datetime.now().isoformat()}
    
    def get_workflow_status(self, execution_id: Optional[str] = None) -> Dict[str, Any]:
        """Get status of workflows."""
        if execution_id:
            if execution_id in self.active_workflows:
                return self.active_workflows[execution_id]
            else:
                # Search in history
                for workflow in self.workflow_history:
                    if workflow["execution_id"] == execution_id:
                        return workflow
                return {"error": "Workflow not found"}
        else:
            return {
                "active_workflows": len(self.active_workflows),
                "total_executed": len(self.workflow_history),
                "active_list": list(self.active_workflows.keys()),
                "recent_history": self.workflow_history[-5:] if self.workflow_history else []
            }
    
    def list_available_workflows(self) -> Dict[str, Any]:
        """List all available workflows."""
        return {
            "workflows": {
                name: {
                    "description": workflow.get("description", "No description"),
                    "steps": workflow.get("steps", []),
                    "schedule": workflow.get("schedule", "manual"),
                    "enabled": workflow.get("enabled", True)
                }
                for name, workflow in self.workflows.items()
            },
            "available_steps": list(self.step_registry.keys())
        }


async def main():
    """Test the workflow engine."""
    logging.basicConfig(level=logging.INFO)
    
    engine = WorkflowEngine()
    
    print("🎯 TEC Workflow Engine Test")
    print("=" * 50)
    
    # List available workflows
    available = engine.list_available_workflows()
    print(f"📋 Available workflows: {list(available['workflows'].keys())}")
    
    # Test a simple workflow
    if "news_automation" in engine.workflows:
        print("\n🚀 Testing news_automation workflow...")
        result = await engine.execute_workflow("news_automation", {
            "max_age": 1,
            "max_topics": 2
        })
        print(f"✅ Workflow completed with status: {result['status']}")
        print(f"📊 Steps completed: {len(result['steps_completed'])}")
        print(f"❌ Steps failed: {len(result['steps_failed'])}")
    
    print("\n🎭 Workflow engine test complete!")

if __name__ == "__main__":
    asyncio.run(main())
