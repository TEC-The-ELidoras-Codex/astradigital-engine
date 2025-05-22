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
def airth_interface(prompt, history):  # Added history parameter
    """Interface for Airth agent with history."""
    logger.info(f"Airth received prompt: {prompt[:50]}... with history length: {len(history)}")
    
    if not AGENTS_LOADED or not hasattr(airth_agent, 'respond'):
        # Fallback response if agent not loaded
        logger.warning("Using fallback response for Airth")
        agent_response = f"Airth, the AI oracle, contemplates: {prompt}\\n\\nResponse will be integrated when agent implementation is complete."
    else:
        try:
            # Convert history format from Gradio's [[user, bot], ...] to what Airth expects
            conversation_history = history if history else []
            
            # Pass the history to Airth's respond method
            agent_response = airth_agent.respond(prompt, conversation_history)
            logger.info(f"Airth response generated successfully: {len(agent_response)} characters")
        except Exception as e:
            logger.error(f"Error in Airth agent: {e}")
            agent_response = f"Error processing your request: {str(e)}"
    
    history.append([prompt, agent_response])
    return history, history, "" # history for chatbot, history for state, "" for clearing input textbox

def post_to_blog(history):
    """Post the last Airth response to WordPress as a blog draft."""
    if not history or len(history) == 0:
        return "No conversation history to post!"
    
    last_exchange = history[-1]
    prompt = last_exchange[0]
    response = last_exchange[1]
    
    logger.info(f"Posting to blog from chat history. Prompt: {prompt[:50]}...")
    
    try:
        # Access the WordPress agent through Airth
        if not AGENTS_LOADED or not hasattr(airth_agent, 'wp_agent'):
            logger.warning("WordPress agent not available.")
            return "WordPress posting capability not available. Please check agent configuration."
        
        # Generate a title from the prompt
        title = f"Airth's Wisdom: {prompt[:50]}..." if len(prompt) > 50 else f"Airth's Wisdom: {prompt}"
        
        # Format the content with both prompt and response
        content = f"<h2>Question</h2>\n<p>{prompt}</p>\n\n<h2>Airth's Response</h2>\n<p>{response}</p>"
        
        # Create post data
        post_data = {
            'title': title,
            'content': content,
            'status': 'draft'  # Always post as draft first for review
        }
        
        # Post to WordPress
        result = airth_agent.wp_agent.create_post(post_data, category="airths_codex")
        
        if result.get("success"):
            post_id = result.get("id", "unknown")
            post_url = result.get("link", "#")
            logger.info(f"Successfully posted to blog. Post ID: {post_id}")
            return f"✅ Successfully posted to WordPress as draft!\nPost ID: {post_id}\nYou can view and edit it at: {post_url}"
        else:
            error = result.get("error_message", "Unknown error")
            logger.error(f"Failed to post to blog: {error}")
            return f"❌ Failed to post to WordPress: {error}"
            
    except Exception as e:
        logger.error(f"Error in post_to_blog: {e}")
        return f"❌ Error processing blog post: {str(e)}"

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
            airth_chatbot = gr.Chatbot(label="Airth's Conversation", elem_id="airth_chatbot") # Changed from Markdown
            airth_history = gr.State([]) # Added state for history

            with gr.Row():
                with gr.Column(scale=1, min_width=200): # Adjusted scale for image
                    gr.Image(value="assets/TEC_Image_profile_MOSTW_notups_ADE.png", label="MOSTW", interactive=False, height=200) # Added height
                with gr.Column(scale=4): # Adjusted scale for input/button
                    airth_input = gr.Textbox(placeholder="Ask Airth for wisdom or a story...", label="Your Request", elem_id="airth_input")
                    with gr.Row():
                        airth_button = gr.Button("Consult Airth", variant="primary")
                        post_blog_button = gr.Button("Post Last Response to Blog", variant="secondary")
            
            # Updated click handler
            airth_button.click(
                fn=airth_interface, 
                inputs=[airth_input, airth_history], 
                outputs=[airth_chatbot, airth_history, airth_input] # Chatbot, State, and clear Textbox
            )
            
            # Add post to blog handler
            post_blog_output = gr.Textbox(label="Blog Post Result", visible=True)
            post_blog_button.click(
                fn=post_to_blog,
                inputs=[airth_history],
                outputs=[post_blog_output]
            )
            
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
