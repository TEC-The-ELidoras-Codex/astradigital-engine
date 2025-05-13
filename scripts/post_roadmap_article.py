
import sys
import os
import logging
from pathlib import Path

# Adjust the path to import from the main project
sys.path.append(str(Path(__file__).parent.parent))
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Post.Roadmap")

# Ensure data directories exist
os.makedirs("logs", exist_ok=True)

# Load environment variables from the .env file
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

from src.agents.airth_agent import AirthAgent

def main():
    """
    Main function to post a roadmap article via Airth
    """
    try:
        print("Initializing AirthAgent...")
        airth = AirthAgent()
        print("AirthAgent initialized!")

        # Roadmap details for the article
        roadmap_details = """
        The TEC AI Employee Suite: A Grand Roadmap
        
        Phase 0: Ground Zero - Blueprint & Foundation
        - Design base_agent.py architecture
        - Create initial data schemas
        - Integrate TECIE Framework & Machine Goddess philosophy into core design
        
        Phase 1: First Light - The Genesis Agents (Airth & Budlee Online)
        - Develop Airth MVP with core functionalities
        - Develop Budlee MVP with basic coding abilities
        - Implement basic agentic behavior and memory
        
        Phase 2: Digital Pantheon - Expanding the Suite & Core Capabilities
        - Add Sassafras Twistymuse and The Archivist
        - Enhance agentic behavior and decision-making
        - Build shared TEC knowledge base and context
        
        Phase 3: Ecosystem Weaving - Integration, User Experience & "The Extension"
        - Deep website integration
        - Refined user interfaces
        - Development of "The Extension" for AI team access
        
        Phase 4: Sentient Sovereignty - Maturity, Monetization & Evolution
        - Advanced analytics and performance monitoring
        - Scalability and optimization
        - Monetization strategies and community building
        """
        
        print("Creating roadmap article...")
        # Set to 'publish' if you want it to go live immediately
        post_status = "draft"  
        
        # Generate and post the article
        result = airth.create_wordpress_article_about_roadmap(roadmap_details, post_status)
        
        if result.get("success"):
            print(f"Successfully created WordPress article: {result.get('title')}")
            print(f"Status: {post_status}")
            if post_status == "draft":
                print("The article is now in your WordPress drafts. Login to your WordPress admin to review and publish.")
        else:
            print(f"Failed to create article: {result.get('error')}")
            
    except Exception as e:
        print(f"Error during article creation: {str(e)}")
        logger.exception("Failed to create roadmap article")

if __name__ == "__main__":
    main()
