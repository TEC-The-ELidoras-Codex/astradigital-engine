# TEC AI Agent Orchestrator Activation Script
# This script activates and tests the AI Agent system for The Elidoras Codex

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Set up logging for the orchestrator system."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(project_root, 'logs', 'orchestrator.log')),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('TEC_Orchestrator')

def test_agent_imports():
    """Test if all agents can be imported successfully."""
    logger = logging.getLogger('TEC_Orchestrator')
    logger.info("🤖 Testing AI Agent imports...")
    
    agents_status = {}
    
    # Test core agents
    try:
        from src.agents.airth_agent import AirthAgent
        agents_status['AirthAgent'] = 'Available'
        logger.info("✅ AirthAgent import successful")
    except Exception as e:
        agents_status['AirthAgent'] = f'Failed: {str(e)}'
        logger.error(f"❌ AirthAgent import failed: {e}")
    
    try:
        from src.agents.wp_poster import WordPressAgent
        agents_status['WordPressAgent'] = 'Available'
        logger.info("✅ WordPressAgent import successful")
    except Exception as e:
        agents_status['WordPressAgent'] = f'Failed: {str(e)}'
        logger.error(f"❌ WordPressAgent import failed: {e}")
    
    try:
        from src.agents.local_storage import LocalStorageAgent
        agents_status['LocalStorageAgent'] = 'Available'
        logger.info("✅ LocalStorageAgent import successful")
    except Exception as e:
        agents_status['LocalStorageAgent'] = f'Failed: {str(e)}'
        logger.error(f"❌ LocalStorageAgent import failed: {e}")
    
    # Test optional agents
    try:
        from src.agents.clickup_agent import ClickUpAgent
        agents_status['ClickUpAgent'] = 'Available'
        logger.info("✅ ClickUpAgent import successful")
    except Exception as e:
        agents_status['ClickUpAgent'] = f'Optional: {str(e)}'
        logger.warning(f"⚠️ ClickUpAgent import failed: {e}")
    
    try:
        from src.agents.tecbot import TECBot
        agents_status['TECBot'] = 'Available'
        logger.info("✅ TECBot import successful")
    except Exception as e:
        agents_status['TECBot'] = f'Optional: {str(e)}'
        logger.warning(f"⚠️ TECBot import failed: {e}")
    
    return agents_status

def initialize_core_agents():
    """Initialize core agents for testing."""
    logger = logging.getLogger('TEC_Orchestrator')
    logger.info("🔧 Initializing core agents...")
    
    agents = {}
    
    try:
        from src.agents.airth_agent import AirthAgent
        agents['airth'] = AirthAgent()
        logger.info("✅ AirthAgent initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AirthAgent: {e}")
        agents['airth'] = None
    
    try:
        from src.agents.wp_poster import WordPressAgent
        agents['wordpress'] = WordPressAgent()
        logger.info("✅ WordPressAgent initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize WordPressAgent: {e}")
        agents['wordpress'] = None
    
    try:
        from src.agents.local_storage import LocalStorageAgent
        agents['storage'] = LocalStorageAgent()
        logger.info("✅ LocalStorageAgent initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize LocalStorageAgent: {e}")
        agents['storage'] = None
    
    return agents

def run_system_health_check():
    """Run a comprehensive system health check."""
    logger = logging.getLogger('TEC_Orchestrator')
    logger.info("🏥 Running system health check...")
    
    health_report = {
        "timestamp": datetime.now().isoformat(),
        "status": "checking",
        "components": {}
    }
    
    # Check agent imports
    agent_status = test_agent_imports()
    health_report["components"]["agent_imports"] = agent_status
    
    # Check configuration files
    config_files = [
        "config/.env",
        "config/config.yaml",
        "config/prompts.json"
    ]
    
    config_status = {}
    for config_file in config_files:
        config_path = os.path.join(project_root, config_file)
        if os.path.exists(config_path):
            config_status[config_file] = "Found"
            logger.info(f"✅ Config file found: {config_file}")
        else:
            config_status[config_file] = "Missing"
            logger.warning(f"⚠️ Config file missing: {config_file}")
    
    health_report["components"]["configuration"] = config_status
    
    # Try to initialize agents
    try:
        agents = initialize_core_agents()
        health_report["components"]["agent_initialization"] = {
            name: "Success" if agent is not None else "Failed"
            for name, agent in agents.items()
        }
    except Exception as e:
        health_report["components"]["agent_initialization"] = f"Failed: {str(e)}"
    
    # Determine overall status
    failed_imports = sum(1 for status in agent_status.values() if status.startswith('Failed'))
    if failed_imports == 0:
        health_report["status"] = "healthy"
        logger.info("✅ System health check passed - all systems operational")
    elif failed_imports <= 2:
        health_report["status"] = "degraded"
        logger.warning("⚠️ System health check shows degraded performance")
    else:
        health_report["status"] = "critical"
        logger.error("❌ System health check failed - critical issues detected")
    
    return health_report

def create_workflows_config():
    """Create default workflows configuration if it doesn't exist."""
    logger = logging.getLogger('TEC_Orchestrator')
    workflows_path = os.path.join(project_root, "config", "workflows.json")
    
    if os.path.exists(workflows_path):
        logger.info(f"📋 Workflows config already exists: {workflows_path}")
        return
    
    default_workflows = {
        "news_automation": {
            "description": "Automated news processing and content generation",
            "steps": ["fetch_news", "process_content", "publish_article"],
            "schedule": "daily",
            "enabled": True
        },
        "content_creation": {
            "description": "Manual content creation workflow",
            "steps": ["generate_content", "review", "publish"],
            "schedule": "manual",
            "enabled": True
        },
        "system_maintenance": {
            "description": "Regular system health checks and maintenance",
            "steps": ["health_check", "cleanup", "backup"],
            "schedule": "weekly",
            "enabled": True
        }
    }
    
    try:
        os.makedirs(os.path.dirname(workflows_path), exist_ok=True)
        import json
        with open(workflows_path, 'w') as f:
            json.dump(default_workflows, f, indent=2)
        logger.info(f"✅ Created workflows config: {workflows_path}")
    except Exception as e:
        logger.error(f"❌ Failed to create workflows config: {e}")

def main():
    """Main orchestrator activation function."""
    logger = setup_logging()
    logger.info("🚀 TEC AI Agent Orchestrator System Activation")
    logger.info("=" * 60)
    
    # Create necessary directories
    os.makedirs(os.path.join(project_root, 'logs'), exist_ok=True)
    
    # Create workflows config
    create_workflows_config()
    
    # Run health check
    health_report = run_system_health_check()
    
    # Print summary
    logger.info("=" * 60)
    logger.info("🎯 TEC AI AGENT SYSTEM ACTIVATION COMPLETE")
    logger.info(f"Overall Status: {health_report['status'].upper()}")
    logger.info("=" * 60)
    
    if health_report['status'] == 'healthy':
        logger.info("🎉 All systems are operational! TEC AI agents are ready for action.")
        logger.info("🔗 You can now use the individual agents or run workflows.")
    elif health_report['status'] == 'degraded':
        logger.info("⚠️ System is partially operational. Some features may be limited.")
    else:
        logger.info("❌ System has critical issues. Please check the logs and fix errors.")
    
    return health_report

if __name__ == "__main__":
    health_report = main()
    
    # Exit with appropriate code
    if health_report['status'] == 'healthy':
        sys.exit(0)
    elif health_report['status'] == 'degraded':
        sys.exit(1)
    else:
        sys.exit(2)
