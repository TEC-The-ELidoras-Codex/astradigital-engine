"""
TEC Workflow Manager - Control & execute workflows for The Elidoras Codex
Run individual workflows, schedule automated execution, monitor status
"""
import asyncio
import argparse
import logging
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.workflow_engine import WorkflowEngine


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(project_root, 'logs', 'workflows.log')),
            logging.StreamHandler()
        ]
    )


async def run_workflow(workflow_name: str, parameters: dict = None, verbose: bool = False):
    """Run a single workflow."""
    setup_logging(verbose)
    logger = logging.getLogger('TEC_WorkflowManager')
    
    print(f"🚀 Starting TEC Workflow: {workflow_name}")
    print("=" * 60)
    
    try:
        engine = WorkflowEngine()
        
        # Check if workflow exists
        if workflow_name not in engine.workflows:
            available = list(engine.workflows.keys())
            print(f"❌ Workflow '{workflow_name}' not found!")
            print(f"📋 Available workflows: {', '.join(available)}")
            return False
            
        # Execute workflow
        result = await engine.execute_workflow(workflow_name, parameters)
        
        # Display results
        print(f"\n🎯 Workflow Execution Summary:")
        print(f"   ID: {result['execution_id']}")
        print(f"   Status: {result['status'].upper()}")
        print(f"   Duration: {result['started_at']} → {result.get('completed_at', 'running')}")
        print(f"   Steps Completed: {len(result['steps_completed'])}")
        print(f"   Steps Failed: {len(result['steps_failed'])}")
        
        if result['steps_completed']:
            print(f"\n✅ Completed Steps:")
            for step in result['steps_completed']:
                print(f"   • {step}")
                
        if result['steps_failed']:
            print(f"\n❌ Failed Steps:")
            for step in result['steps_failed']:
                print(f"   • {step}")
                
        if result['errors'] and verbose:
            print(f"\n🔍 Error Details:")
            for error in result['errors']:
                print(f"   • Step: {error.get('step', 'unknown')}")
                print(f"     Error: {error.get('error', 'unknown error')}")
                
        # Save execution report
        reports_dir = os.path.join(project_root, 'data', 'workflow_reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        report_file = os.path.join(reports_dir, f"{result['execution_id']}.json")
        with open(report_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n📊 Execution report saved: {report_file}")
        
        return result['status'] in ['completed', 'partial']
        
    except Exception as e:
        logger.error(f"❌ Workflow execution failed: {e}")
        print(f"❌ Workflow execution failed: {e}")
        return False


async def list_workflows():
    """List all available workflows."""
    print("📋 TEC Available Workflows")
    print("=" * 60)
    
    try:
        engine = WorkflowEngine()
        available = engine.list_available_workflows()
        
        for name, workflow in available['workflows'].items():
            enabled = "🟢" if workflow['enabled'] else "🔴"
            schedule = workflow['schedule']
            description = workflow['description']
            steps = len(workflow['steps'])
            
            print(f"\n{enabled} {name.upper()}")
            print(f"   Description: {description}")
            print(f"   Schedule: {schedule}")
            print(f"   Steps: {steps}")
            print(f"   Steps: {' → '.join(workflow['steps'])}")
            
        print(f"\n🔧 Available Workflow Steps ({len(available['available_steps'])}):")
        for i, step in enumerate(available['available_steps']):
            if i % 4 == 0:
                print("   ", end="")
            print(f"{step:<25}", end="")
            if (i + 1) % 4 == 0:
                print()
        if len(available['available_steps']) % 4 != 0:
            print()
            
    except Exception as e:
        print(f"❌ Failed to list workflows: {e}")


async def monitor_workflows():
    """Monitor active workflows."""
    print("📊 TEC Workflow Monitor")
    print("=" * 60)
    
    try:
        engine = WorkflowEngine()
        status = engine.get_workflow_status()
        
        print(f"Active Workflows: {status['active_workflows']}")
        print(f"Total Executed: {status['total_executed']}")
        
        if status['active_list']:
            print(f"\n🔄 Currently Running:")
            for workflow_id in status['active_list']:
                print(f"   • {workflow_id}")
                
        if status['recent_history']:
            print(f"\n📜 Recent History:")
            for workflow in status['recent_history'][-3:]:
                status_icon = "✅" if workflow['status'] == 'completed' else "❌" if workflow['status'] == 'failed' else "⚠️"
                print(f"   {status_icon} {workflow['workflow_name']} - {workflow['status']} - {workflow.get('completed_at', 'running')}")
                
    except Exception as e:
        print(f"❌ Failed to monitor workflows: {e}")


async def test_workflow_engine():
    """Test the workflow engine with a simple workflow."""
    print("🧪 Testing TEC Workflow Engine")
    print("=" * 60)
    
    try:
        engine = WorkflowEngine()
        
        # Test system health check
        print("🏥 Testing system health check...")
        result = await engine.execute_workflow("system_maintenance", {
            "days_old": 7
        })
        
        print(f"✅ Test completed with status: {result['status']}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main workflow manager function."""
    parser = argparse.ArgumentParser(description='TEC Workflow Manager')
    parser.add_argument('action', choices=['run', 'list', 'monitor', 'test'], 
                       help='Action to perform')
    parser.add_argument('--workflow', '-w', help='Workflow name to run')
    parser.add_argument('--params', '-p', help='JSON parameters for workflow')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    print("🤖 TEC Workflow Manager")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Ensure logs directory exists
    os.makedirs(os.path.join(project_root, 'logs'), exist_ok=True)
    
    if args.action == 'run':
        if not args.workflow:
            print("❌ Please specify a workflow name with --workflow")
            return False
            
        parameters = {}
        if args.params:
            try:
                parameters = json.loads(args.params)
            except json.JSONDecodeError:
                print("❌ Invalid JSON parameters")
                return False
                
        return asyncio.run(run_workflow(args.workflow, parameters, args.verbose))
        
    elif args.action == 'list':
        asyncio.run(list_workflows())
        return True
        
    elif args.action == 'monitor':
        asyncio.run(monitor_workflows())
        return True
        
    elif args.action == 'test':
        return asyncio.run(test_workflow_engine())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
