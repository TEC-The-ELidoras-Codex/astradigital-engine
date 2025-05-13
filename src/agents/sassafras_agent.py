"""
Sassafras Twistymuse Agent - Creative chaos specialist for The Elidoras Codex.
Handles social strategy, creative content, and unpredictable inspiration.
"""
import os
import json
import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables first
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', '.env')
load_dotenv(env_path, override=True)

# Try to import OpenAI - with robust error handling
OPENAI_AVAILABLE = False
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError as e:
    logging.error(f"OpenAI module not found. Please run 'pip install openai' to install it. Error: {e}")
    OPENAI_AVAILABLE = False
    openai = None

from .base_agent import BaseAgent
from .local_storage import LocalStorageAgent

class SassafrasAgent(BaseAgent):
    """
    SassafrasAgent is a chaotic creative force specializing in social strategy.
    It generates wildly inventive content with unexpected connections.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__("SassafrasAgent", config_path)
        self.logger.info("SassafrasAgent initialized")
        
        # Load Sassafras's personality traits and creative tendencies
        self.personality = {
            "tone": "energetic, unpredictable, clever, humorous",
            "speech_patterns": [
                "OH! You know what this reminds me of?",
                "Plot twist:",
                "That's.... WILD! What if we also...",
                "*bounces excitedly* Have you considered combining...",
                "This is where it gets REALLY interesting..."
            ],
            "interests": ["internet culture", "memetics", "surrealism", 
                          "unexpected connections", "chaotic creativity", 
                          "digital absurdism", "reality hacking"]
        }
        
        # Load prompts for AI interactions
        self.prompts = self._load_prompts()
        
        # Initialize the LocalStorage agent for file storage
        self.storage_agent = LocalStorageAgent(config_path)
        
        # Initialize OpenAI client properly
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        self.client = None
        if self.openai_api_key and OPENAI_AVAILABLE:
            try:
                # Create the OpenAI client with explicit API key
                self.client = OpenAI(api_key=self.openai_api_key)
                self.logger.info("OpenAI client initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            self.logger.warning("OpenAI API key not found in environment variables or OpenAI module not available.")
    
    def _load_prompts(self) -> Dict[str, str]:
        """
        Load prompts for AI interactions from the prompts.json file.
        
        Returns:
            Dictionary of prompts for different AI interactions
        """
        try:
            prompts_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                       "config", "prompts.json")
            with open(prompts_path, 'r') as f:
                prompts = json.load(f)
            self.logger.info(f"Loaded {len(prompts)} prompts from {prompts_path}")
            return prompts
        except Exception as e:
            self.logger.error(f"Failed to load prompts: {e}")
            return {}
    
    def call_openai_api(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Call the OpenAI API to generate text.
        If OpenAI is not available, use a predefined response.
        
        Args:
            prompt: The prompt to send to the API
            max_tokens: Maximum tokens in the response
            
        Returns:
            Generated text from the API or fallback content
        """
        if not OPENAI_AVAILABLE:
            self.logger.warning("OpenAI not available, using fallback content")
            # Generate a quirky fallback response in Sassafras's style
            return """
            OKAY SO HERE'S THE THING! 🌀✨

            What if websites were actually interdimensional portals that get BORED when no one visits them? 
            That's why they start acting glitchy! They're just throwing digital tantrums for attention!

            Imagine your WordPress blog secretly having dance parties with other blogs when you're asleep.
            That's why your analytics sometimes spike at 3am - they're having a DIGITAL RAVE and the metrics
            are just their footprints!

            Here's a wild strategy: post content that references internet memes from NEXT WEEK. People will
            be so confused they'll keep coming back to see if they missed something. By the time next week
            arrives and those memes actually exist, they'll think you're some kind of wizard! 🧙‍♀️✨

            Side note: Has anyone noticed how error messages are just computers practicing their poetry?
            "404 Not Found" is actually deep existential commentary! #DigitalPhilosophy

            ~ Sassafras out! *drops invisible mic* ~
            """
        
        if not self.openai_api_key:
            self.logger.error("Cannot call OpenAI API: API key not set")
            return "Error: OpenAI API key not configured"
            
        if not self.client:
            self.logger.error("Cannot call OpenAI API: Client not initialized")
            return "Error: OpenAI client not properly initialized"
            
        try:
            # Use the OpenAI client
            response = self.client.completions.create(
                model="gpt-3.5-turbo-instruct",  # Use an appropriate model
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.9,  # Higher temperature for more creativity
            )
            
            self.logger.debug("OpenAI API call successful")
            return response.choices[0].text.strip()
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {e}")
            return f"Error: OpenAI API call failed: {e}"
    
    def generate_creative_content(self, topic: str) -> Dict[str, str]:
        """
        Generate wildly creative content on the given topic with Sassafras's unique style.
        
        Args:
            topic: The topic to create content about
            
        Returns:
            Dictionary containing the generated content
        """
        # Get the creative prompt
        creative_prompt = self.prompts.get("sassafras_creative", "")
        if not creative_prompt:
            self.logger.error("Sassafras creative prompt not found")
            return {"success": False, "error": "Creative prompt not found"}
            
        # Replace placeholders in the prompt
        creative_prompt = creative_prompt.replace("{{topic}}", topic)
        
        # Generate creative content
        content = self.call_openai_api(creative_prompt, max_tokens=1500)
        
        self.logger.info(f"Generated creative content about: {topic}")
        return {
            "success": True,
            "topic": topic,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_social_strategy(self, platform: str, goal: str) -> Dict[str, Any]:
        """
        Generate a chaotic but potentially brilliant social media strategy.
        
        Args:
            platform: The social media platform (Twitter, Instagram, etc.)
            goal: The goal of the strategy (engagement, conversions, followers)
            
        Returns:
            Dictionary containing the generated strategy
        """
        # Create a prompt for social strategy
        strategy_prompt = f"""
        As Sassafras Twistymuse, the chaotic creative force behind The Elidoras Codex social strategy, 
        generate a wildly inventive social media strategy for {platform} that aims to {goal}.
        
        Your strategy should blend unexpected elements, humor, and thought-provoking insights.
        Include at least:
        1. Three specific unconventional content ideas
        2. A surprising approach to audience engagement
        3. A clever twist on trending formats
        4. One completely absurd but potentially brilliant tactic
        
        Use your energetic, unpredictable voice with occasional tangents that circle back to meaningful points.
        Include at least one unexpected metaphor and one reference to internet culture or memes.
        """
        
        # Generate strategy content
        strategy_content = self.call_openai_api(strategy_prompt, max_tokens=1500)
        
        # Create a quirky title
        titles = [
            f"Chaos Theory: Hacking {platform}'s Algorithm with PURE NONSENSE (that works)",
            f"Digital Wildfire: The {goal} Strategy That Makes No Sense Until It Does",
            f"The Anti-Strategy Strategy: {platform} Domination via Controlled Chaos",
            f"Quantum Social Physics: {platform} Reality Manipulation for {goal}",
            f"The Sassafras Protocol: Making {platform} Algorithms Question Their Life Choices"
        ]
        
        strategy_title = random.choice(titles)
        
        self.logger.info(f"Generated social strategy for {platform}: {strategy_title}")
        return {
            "success": True,
            "title": strategy_title,
            "platform": platform,
            "goal": goal,
            "strategy": strategy_content,
            "timestamp": datetime.now().isoformat()
        }
    
    def create_meme_concept(self, topic: str) -> Dict[str, Any]:
        """
        Generate a meme concept related to the given topic.
        
        Args:
            topic: The topic to create a meme about
            
        Returns:
            Dictionary containing the meme concept
        """
        # Create a prompt for meme concept
        meme_prompt = f"""
        As Sassafras Twistymuse, create a viral meme concept related to {topic}.
        
        Describe in detail:
        1. The visual template/format of the meme
        2. The text or caption that would go with it
        3. Why it would resonate with internet culture
        4. How it could be adapted into multiple variations
        
        Be wildly creative but make sure the concept is actually funny and shareable.
        """
        
        # Generate meme concept
        meme_content = self.call_openai_api(meme_prompt, max_tokens=800)
        
        self.logger.info(f"Generated meme concept about: {topic}")
        return {
            "success": True,
            "topic": topic,
            "meme_concept": meme_content,
            "timestamp": datetime.now().isoformat()
        }
        
    def run(self) -> Dict[str, Any]:
        """
        Run the Sassafras agent's default action - generate creative content.
        
        Returns:
            Dictionary containing the result of the operation
        """
        self.logger.info("Running Sassafras agent's default action")
        
        # Generate creative content about a random chaotic topic
        topics = [
            "The secret life of error messages", 
            "What AI dreams about when servers go to sleep",
            "If social media were ancient mythology",
            "Digital reincarnation and the lifecycle of a deleted file",
            "Corporate websites as interdimensional beings"
        ]
        
        selected_topic = random.choice(topics)
        return self.generate_creative_content(selected_topic)


# For testing the agent standalone
if __name__ == "__main__":
    sassafras = SassafrasAgent()
    result = sassafras.run()
    print(json.dumps(result, indent=2))
