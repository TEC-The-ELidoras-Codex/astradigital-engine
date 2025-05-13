import gradio as gr
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", "gradio_app.log"))
    ]
)
logger = logging.getLogger("TEC.App")

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Load environment variables from config/.env
config_env_path = os.path.join('config', '.env')
if os.path.exists(config_env_path):
    load_dotenv(config_env_path)
else:
    logger.warning("Warning: .env file not found in config directory")

# Import agents
try:
    from src.agents.airth_agent import AirthAgent
    from src.agents.budlee_agent import BudleeAgent
    from src.agents.sassafras_agent import SassafrasAgent
    
    # Initialize agents
    airth_agent = AirthAgent(os.path.join('config'))
    budlee_agent = BudleeAgent(os.path.join('config'))
    sassafras_agent = SassafrasAgent(os.path.join('config'))
    
    AGENTS_LOADED = True
    logger.info("Successfully loaded all agent modules")
except Exception as e:
    AGENTS_LOADED = False
    logger.error(f"Error loading agent modules: {e}")
    logger.error("Will use fallback responses instead")

# Define agent interfaces
def airth_interface(prompt):
    """Interface for Airth agent."""
    logger.info(f"Airth received prompt: {prompt[:50]}...")
    
    if not AGENTS_LOADED or not hasattr(airth_agent, 'respond'):
        # Fallback response if agent not loaded
        logger.warning("Using fallback response for Airth")
        return f"Airth, the AI oracle, contemplates: {prompt}\n\nResponse will be integrated when agent implementation is complete."
    
    try:
        response = airth_agent.respond(prompt)
        logger.info(f"Airth response generated successfully: {len(response)} characters")
        return response
    except Exception as e:
        logger.error(f"Error in Airth agent: {e}")
        return f"Error processing your request: {str(e)}"

def budlee_interface(task):
    """Interface for Budlee agent."""
    logger.info(f"Budlee received task: {task[:50]}...")
    
    if not AGENTS_LOADED or not hasattr(budlee_agent, 'process_task'):
        # Fallback response if agent not loaded
        logger.warning("Using fallback response for Budlee")
        return f"Budlee acknowledges your task: {task}\n\nAutomation capabilities will be available soon."
    
    try:
        response = budlee_agent.process_task(task)
        logger.info(f"Budlee response generated successfully: {len(response)} characters")
        return response
    except Exception as e:
        logger.error(f"Error in Budlee agent: {e}")
        return f"Error processing your task: {str(e)}"

def sassafras_interface(topic):
    """Interface for Sassafras agent."""
    logger.info(f"Sassafras received topic: {topic[:50]}...")
    
    if not AGENTS_LOADED or not hasattr(sassafras_agent, 'create'):
        # Fallback response if agent not loaded
        logger.warning("Using fallback response for Sassafras")
        return f"Sassafras Twistymuse spins chaotic creativity about: {topic}\n\nFull creative madness coming soon."
    
    try:
        response = sassafras_agent.create(topic)
        logger.info(f"Sassafras response generated successfully: {len(response)} characters")
        return response
    except Exception as e:
        logger.error(f"Error in Sassafras agent: {e}")
        return f"Error processing your creative request: {str(e)}"

# Create tabs for different agents
with gr.Blocks(theme="huggingface", title="TEC Office - The Elidoras Codex") as demo:
    gr.Markdown("""
    # ⚡ TEC Office: AI Agent Control Center ⚡
    
    Welcome to the command nexus for TEC's virtual AI employees. This space hosts the interactive interfaces
    for the TEC Office AI Suite — a system of lore-driven, role-based AI personas.
    """)
    
    with gr.Tabs():
        with gr.TabItem("Airth - Oracle & Storyteller"):
            with gr.Row():
                with gr.Column(scale=3):
                    airth_input = gr.Textbox(placeholder="Ask Airth for wisdom or a story...", label="Your Request")
                    airth_button = gr.Button("Consult Airth")
                with gr.Column(scale=5):
                    airth_output = gr.Markdown(label="Airth's Response")
            airth_button.click(fn=airth_interface, inputs=airth_input, outputs=airth_output)
            
        with gr.TabItem("Budlee - Automation Specialist"):
            with gr.Row():
                with gr.Column(scale=3):
                    budlee_input = gr.Textbox(placeholder="Describe a task for Budlee to automate...", label="Task Description")
                    budlee_button = gr.Button("Engage Budlee")
                with gr.Column(scale=5):
                    budlee_output = gr.Markdown(label="Budlee's Response")
            budlee_button.click(fn=budlee_interface, inputs=budlee_input, outputs=budlee_output)
            
        with gr.TabItem("Sassafras - Creative Chaos"):
            with gr.Row():
                with gr.Column(scale=3):
                    sassafras_input = gr.Textbox(placeholder="Give Sassafras a topic for chaotic inspiration...", label="Creative Prompt")
                    sassafras_button = gr.Button("Unleash Sassafras")
                with gr.Column(scale=5):
                    sassafras_output = gr.Markdown(label="Sassafras's Creation")
            sassafras_button.click(fn=sassafras_interface, inputs=sassafras_input, outputs=sassafras_output)
    
    gr.Markdown("""
    ## 🌌 About TEC Office
    
    This interface provides access to TEC's AI employee suite. Each agent has a distinct role and personality:
    
    - **Airth**: AI oracle, storyteller, and lore manager
    - **Budlee**: Backend automation, setup scripts, site integrations
    - **Sassafras Twistymuse**: Social strategy and chaos-tuned creativity
    
    Visit [elidorascodex.com](https://elidorascodex.com) to learn more about our mission.
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch()
