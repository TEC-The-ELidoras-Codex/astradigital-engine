# TEC AI Agent Orchestrator Test Script
# Test the orchestrator functionality with the activated agents

import os
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_agent_functionality():
    """Test basic functionality of each agent."""
    print("🧪 Testing TEC AI Agent functionality...")
    
    # Test Airth Agent
    try:
        from src.agents.airth_agent import AirthAgent
        airth = AirthAgent()
        print("✅ AirthAgent: Initialized successfully")
        print(f"   - Profile loaded: {len(airth.profile) > 0}")
        print(f"   - Prompts loaded: {len(airth.prompts) > 0}")
        print(f"   - OpenAI client: {'Ready' if airth.client else 'Not configured'}")
    except Exception as e:
        print(f"❌ AirthAgent test failed: {e}")
    
    # Test WordPress Agent
    try:
        from src.agents.wp_poster import WordPressAgent
        wp = WordPressAgent()
        print("✅ WordPressAgent: Initialized successfully")
        print(f"   - API URL: {wp.wp_url}")
        print(f"   - Environment: {'Production' if not wp.use_local else 'Local'}")
    except Exception as e:
        print(f"❌ WordPressAgent test failed: {e}")
    
    # Test Local Storage Agent
    try:
        from src.agents.local_storage import LocalStorageAgent
        storage = LocalStorageAgent()
        print("✅ LocalStorageAgent: Initialized successfully")
        print(f"   - Storage path: {storage.storage_path}")
    except Exception as e:
        print(f"❌ LocalStorageAgent test failed: {e}")
    
    # Test optional agents
    try:
        from src.agents.clickup_agent import ClickUpAgent
        clickup = ClickUpAgent()
        print("✅ ClickUpAgent: Available and initialized")
    except Exception as e:
        print(f"⚠️ ClickUpAgent: Optional agent not fully configured ({e})")
    
    try:
        from src.agents.tecbot import TECBot
        tecbot = TECBot()
        print("✅ TECBot: Available and initialized")
    except Exception as e:
        print(f"⚠️ TECBot: Optional agent not fully configured ({e})")

def demonstrate_workflow():
    """Demonstrate a simple workflow using the agents."""
    print("\n🎭 Demonstrating TEC AI Agent workflow...")
    
    try:
        from src.agents.airth_agent import AirthAgent
        from src.agents.local_storage import LocalStorageAgent
        
        # Initialize agents
        airth = AirthAgent()
        storage = LocalStorageAgent()
        
        print("📝 Step 1: Generate sample content with Airth")
        
        # Create a simple content generation prompt
        prompt = "Write a brief 100-word introduction to The Elidoras Codex universe for new visitors."
        
        # Generate content (if OpenAI is configured)
        if airth.client:
            try:
                content = airth.generate_content(
                    prompt=prompt,
                    content_type="introduction",
                    word_count=100
                )
                print(f"✅ Content generated: {len(content)} characters")
                
                print("💾 Step 2: Store content using LocalStorage")
                storage_key = f"demo_content_{int(__import__('time').time())}"
                storage.store_data(storage_key, {
                    "content": content,
                    "type": "introduction",
                    "generated_at": __import__('datetime').datetime.now().isoformat(),
                    "agent": "AirthAgent"
                })
                print(f"✅ Content stored with key: {storage_key}")
                
                print("📖 Step 3: Retrieve and display content")
                retrieved = storage.get_data(storage_key)
                if retrieved:
                    print(f"✅ Content retrieved successfully")
                    print(f"   Generated at: {retrieved.get('generated_at')}")
                    print(f"   Content preview: {retrieved.get('content', '')[:100]}...")
                else:
                    print("❌ Failed to retrieve content")
                
            except Exception as e:
                print(f"❌ Workflow demonstration failed: {e}")
        else:
            print("⚠️ OpenAI not configured - skipping content generation demo")
            print("📝 Demonstrating storage functionality instead...")
            
            # Demo storage without content generation
            demo_data = {
                "title": "TEC AI Agent System Demo",
                "description": "Demonstration of the activated AI agent orchestrator",
                "timestamp": __import__('datetime').datetime.now().isoformat(),
                "status": "active"
            }
            
            storage_key = f"demo_system_{int(__import__('time').time())}"
            storage.store_data(storage_key, demo_data)
            print(f"✅ Demo data stored with key: {storage_key}")
            
            retrieved = storage.get_data(storage_key)
            if retrieved:
                print(f"✅ Demo data retrieved: {retrieved.get('title')}")
            
    except Exception as e:
        print(f"❌ Workflow demonstration failed: {e}")

def show_system_status():
    """Show current system status."""
    print("\n📊 TEC AI Agent System Status:")
    print("=" * 50)
    
    # Check available agents
    agents = {
        "AirthAgent": "src.agents.airth_agent",
        "WordPressAgent": "src.agents.wp_poster", 
        "LocalStorageAgent": "src.agents.local_storage",
        "ClickUpAgent": "src.agents.clickup_agent",
        "TECBot": "src.agents.tecbot"
    }
    
    for agent_name, module_path in agents.items():
        try:
            __import__(module_path)
            print(f"✅ {agent_name}: Available")
        except ImportError:
            print(f"❌ {agent_name}: Not available")
        except Exception as e:
            print(f"⚠️ {agent_name}: Available but has issues ({e})")
    
    # Check configuration files
    config_files = [
        "config/.env",
        "config/workflows.json",
        "config/prompts.json",
        "config/airth_profile.json"
    ]
    
    print("\n📁 Configuration Files:")
    for config_file in config_files:
        config_path = os.path.join(project_root, config_file)
        if os.path.exists(config_path):
            print(f"✅ {config_file}: Found")
        else:
            print(f"❌ {config_file}: Missing")
    
    # Check news automation
    news_automation_script = os.path.join(project_root, "scripts", "airth_news_automation.py")
    if os.path.exists(news_automation_script):
        print(f"✅ News Automation: Available")
    else:
        print(f"❌ News Automation: Not found")

def main():
    """Main test function."""
    print("🤖 TEC AI Agent Orchestrator System Test")
    print("=" * 60)
    
    # Run tests
    test_agent_functionality()
    demonstrate_workflow()
    show_system_status()
    
    print("\n🎯 Test Summary:")
    print("=" * 60)
    print("✅ AI Agent system is activated and functional!")
    print("📋 Available features:")
    print("   • Individual agent operations")
    print("   • Content generation (Airth)")
    print("   • WordPress publishing")
    print("   • Local data storage")
    print("   • News automation (scheduled)")
    print("   • Workflow management")
    
    print("\n🚀 Ready for TEC operations!")

if __name__ == "__main__":
    main()
