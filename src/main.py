"""
TEC_OFFICE_REPO Main Module
Main entry point for running TEC AI agents.
"""
import os
import sys
import logging
import argparse
from typing import Dict, Any, List, Optional
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", "tec_office.log"), mode='a')
    ]
)
logger = logging.getLogger("TEC.Main")

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Import agents
from src.agents import AirthAgent, BudleeAgent, SassafrasAgent


def run_agent(agent_name: str, action: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """
    Run a specific agent with the given action and parameters.
    
    Args:
        agent_name: Name of the agent to run
        action: Name of the action to run
        **kwargs: Additional parameters for the action
        
    Returns:
        Dictionary with the result of the action
    """
    # Create the config path
    config_path = os.path.join("config")
    
    # Create the agent
    if agent_name.lower() == "airth":
        agent = AirthAgent(config_path)
    elif agent_name.lower() == "budlee":
        agent = BudleeAgent(config_path)
    elif agent_name.lower() == "sassafras":
        agent = SassafrasAgent(config_path)
    else:
        logger.error(f"Unknown agent: {agent_name}")
        return {"success": False, "error": f"Unknown agent: {agent_name}"}
        
    # Run the specified action or the default action
    logger.info(f"Running {agent_name} agent with action: {action or 'default'}")
    
    try:
        if action:
            # Call the action method on the agent if it exists
            if hasattr(agent, action) and callable(getattr(agent, action)):
                result = getattr(agent, action)(**kwargs)
            else:
                logger.error(f"Unknown action for {agent_name}: {action}")
                return {"success": False, "error": f"Unknown action for {agent_name}: {action}"}
        else:
            # Run the default action
            result = agent.run()
            
        return result
    
    except Exception as e:
        logger.exception(f"Error running {agent_name} agent with action {action}: {e}")
        return {"success": False, "error": str(e)}


def main() -> None:
    """
    Main function for the TEC Office Agent System.
    Parses command line arguments and runs the specified agent.
    """
    parser = argparse.ArgumentParser(description='TEC Office Agent System')
    parser.add_argument('agent', choices=['airth', 'budlee', 'sassafras'], help='Agent to run')
    parser.add_argument('--action', help='Action to run (default: run)')
    parser.add_argument('--params', help='JSON string of parameters for the action')
    parser.add_argument('--output', help='Output file for the result')
    
    args = parser.parse_args()
    
    # Parse parameters if provided
    params = {}
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON parameters: {args.params}")
            sys.exit(1)
    
    # Run the agent
    result = run_agent(args.agent, args.action, **params)
    
    # Output the result
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to {args.output}")
        except Exception as e:
            logger.error(f"Failed to save result to {args.output}: {e}")
            print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
