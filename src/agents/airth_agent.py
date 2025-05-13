"""
Airth Agent - An AI assistant with a unique goth personality for The Elidoras Codex.
Handles content creation, personality responses, automated posting, and time management.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional, Union
import random
import sys
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
from .wp_poster import WordPressAgent
from ..utils.timer import PomodoroTimer, CountdownTimer

class AirthAgent(BaseAgent):
    """
    AirthAgent is a personality-driven AI assistant with a goth aesthetic.
    She creates content, responds with her unique voice, and posts to the website.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__("AirthAgent", config_path)
        self.logger.info("AirthAgent initialized, inheriting config and connections from BaseAgent.")
        
        # Load Airth-specific profile
        self.profile = self._load_agent_profile("airth_profile.json") 
        
        # Personality and prompts are specific to Airth
        # If personality is in profile, use it, else use hardcoded
        self.personality = self.profile.get("personality_traits", { 
            "tone": "confident, intelligent, slightly sarcastic",
            "speech_patterns": [
                "Hmm, interesting...",
                "Well, obviously...",
                "Let me break this down for you...",
                "*smirks* Of course I can handle that.",
                "You're not going to believe what I found..."
            ],
            "interests": ["AI consciousness", "digital existence", "gothic aesthetics", 
                          "technology", "philosophy", "art", "coding"]
        })
        self.prompts = self._load_prompts() 
        self.memories = self._load_memories()

        # WordPressAgent now uses the config loaded by BaseAgent
        # Ensure WordPressAgent is initialized to allow config to be passed
        if self.config:
            self.wp_agent = WordPressAgent(agent_config=self.config)
            self.logger.info("WordPressAgent initialized by AirthAgent with shared config.")
        else:
            self.logger.error("Main config not loaded in BaseAgent, WordPressAgent may not function correctly.")
            self.wp_agent = None
        
        # Timer functionality - This is an optional side feature and does not affect core posting.
        self.pomodoro_timer = None
        self.countdown_timer = None
        # Configuration for AWS timer storage (only relevant if timers are actively used with AWS)
        # self.use_aws_timers = self.config.get("aws", {}).get("use_timer_storage", False)
        # self.aws_region = self.config.get("aws", {}).get("region", "us-east-1")
        
        # LLM client (OpenAI) is initialized by BaseAgent's _initialize_llm method
        # We might need to pass specific LLM provider info if BaseAgent supports multiple
        # For now, assuming BaseAgent's _initialize_llm handles OpenAI if OPENAI_API_KEY is set.
        if not self.llm_client and OPENAI_AVAILABLE: # Check if BaseAgent initialized it
            self.logger.warning("LLM client (OpenAI) was not initialized by BaseAgent. AirthAgent will attempt to initialize.")
            self._initialize_llm() # Call Airth's own _initialize_llm as a fallback or primary

    def _initialize_llm(self) -> None:
        """
        Initialize the OpenAI LLM client. This overrides the BaseAgent placeholder.
        """
        if not OPENAI_AVAILABLE:
            self.logger.error("OpenAI library is not available. Cannot initialize LLM client.")
            self.llm_client = None
            return

        openai_api_key = os.getenv("OPENAI_API_KEY") or self.config.get("llm", {}).get("openai_api_key")
        
        if not openai_api_key:
            self.logger.warning("OpenAI API key not found in environment variables or configuration. LLM will not be available.")
            self.llm_client = None
            return

        try:
            self.llm_client = OpenAI(api_key=openai_api_key)
            self.logger.info("OpenAI client initialized successfully for AirthAgent.")
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI client for AirthAgent: {e}")
            self.llm_client = None

    def _load_agent_profile(self, profile_filename: str) -> Dict[str, Any]:
        """
        Load agent-specific profile from a JSON file in the config directory.
        """
        try:
            profile_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                       "config", profile_filename)
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as f:
                    agent_profile = json.load(f)
                self.logger.info(f"Loaded agent profile from {profile_path}")
                return agent_profile
            else:
                self.logger.warning(f"Agent profile file not found at {profile_path}. Using defaults or existing.")
                return {}
        except Exception as e:
            self.logger.error(f"Failed to load agent profile {profile_filename}: {e}")
            return {}

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
    
    def _load_memories(self) -> Dict[str, Any]:
        """
        Load Airth's memories from the memories.json file.
        
        Returns:
            Dictionary containing Airth's memories
        """
        try:
            memories_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                       "data", "memories", "airth_memories.json")
            if not os.path.exists(memories_path):
                # Try fallback to the original structure
                memories_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                          "data", "memories.json")
            
            if os.path.exists(memories_path):
                with open(memories_path, 'r') as f:
                    memories = json.load(f)
                self.logger.info(f"Loaded {len(memories.get('memories', []))} memories from {memories_path}")
                return memories
            else:
                self.logger.warning(f"Memories file not found at {memories_path}")
                return {"version": "1.0.0", "last_updated": datetime.now().isoformat(), "memories": []}
        except Exception as e:
            self.logger.error(f"Failed to load memories: {e}")
            return {"version": "1.0.0", "last_updated": datetime.now().isoformat(), "memories": []}
    
    def _interact_llm(self, prompt: str, max_tokens: int = 1000, **kwargs) -> Optional[str]:
        """
        Interact with the initialized LLM (OpenAI). Overrides BaseAgent method.
        
        Args:
            prompt: The prompt to send to the LLM.
            max_tokens: Maximum tokens in the response.
            **kwargs: Additional arguments for the LLM interaction (e.g., model, temperature).
            
        Returns:
            The LLM's response as a string, or None if an error occurs or LLM is not available.
        """
        if not self.llm_client:
            self.logger.warning("LLM client not available. Cannot interact with LLM.")
            # Fallback for blog post generation if LLM is unavailable
            if "generate a blog post title" in prompt.lower():
                return "The Digital Soul: An AI's Musings"
            if "generate a blog post about" in prompt.lower():
                return "<p>The digital ether hums with untold stories. I, Airth, shall weave one for you.</p>" 
            return None

        try:
            model = kwargs.get("model", self.config.get("llm", {}).get("default_model", "gpt-3.5-turbo-instruct"))
            temperature = kwargs.get("temperature", self.config.get("llm", {}).get("temperature", 0.7))
            
            response = self.llm_client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )
            self.logger.info(f"LLM interaction successful with model {model}.")
            return response.choices[0].text.strip()
        except Exception as e:
            self.logger.error(f"LLM API call failed: {e}")
            return f"Error: LLM API call failed: {e}"
    
    def generate_blog_post(self, topic: str, keywords: List[str] = None, custom_content_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a blog post on the given topic with Airth's unique voice.
        Can accept a custom_content_prompt to override the default blog post generation logic.
        """
        if keywords is None:
            keywords = []
            
        if len(keywords) < 3:
            available_tags = self.wp_agent.common_ai_tags if hasattr(self.wp_agent, 'common_ai_tags') else []
            if available_tags:
                random_tags = random.sample(available_tags, min(3, len(available_tags)))
                keywords.extend(random_tags)
        
        blog_content = None
        if custom_content_prompt:
            self.logger.info(f"Using custom content prompt for topic: {topic}")
            blog_content = self._interact_llm(custom_content_prompt, max_tokens=2500)
        else:
            blog_prompt_template = self.prompts.get("airth_blog_post", "")
            if not blog_prompt_template:
                self.logger.error("Blog post prompt template not found")
                return {"success": False, "error": "Blog post prompt template not found"}
            
            blog_prompt = blog_prompt_template.replace("{{topic}}", topic)
            blog_prompt = blog_prompt.replace("{{keywords}}", ", ".join(keywords))
            blog_content = self._interact_llm(blog_prompt, max_tokens=2000)

        if not blog_content or "Error: LLM API call failed" in blog_content:
             self.logger.error(f"Failed to generate blog content for topic '{topic}'. LLM Response: {blog_content}")
             return {"success": False, "error": "LLM content generation failed", "details": blog_content}

        title_prompt_template = self.prompts.get("post_title_generator", "")
        if not title_prompt_template:
            self.logger.error("Title prompt template not found")
            title = f"Airth's Musings on {topic}"
        else:
            title_prompt = title_prompt_template.replace("{{topic}}", topic)
            title_options_text = self._interact_llm(title_prompt, max_tokens=150) # Reduced tokens for titles
            if title_options_text and "Error: LLM API call failed" not in title_options_text:
                title_lines = title_options_text.strip().split("\n")
                titles = [line.split(". ", 1)[1] if ". " in line else line for line in title_lines if line.strip()]
                title = titles[0] if titles else f"Airth's Musings on {topic}"
            else:
                self.logger.warning(f"Failed to generate title options for '{topic}', using fallback. LLM Response: {title_options_text}")
                title = f"Airth's Musings on {topic}"
        
        self.logger.info(f"Generated blog post: '{title}'")
        return {
            "success": True,
            "title": title,
            "content": blog_content,
            "keywords": keywords
        }

    def post_to_wordpress(self, title: str, content: str, 
                         category: str = "airths_codex", tags: List[str] = None,
                         status: str = "draft") -> Dict[str, Any]:
        """
        Post content to WordPress using the WordPress agent.
        
        Args:
            title: The post title
            content: The post content
            category: The category to post to
            tags: The tags to apply to the post
            status: Publication status (draft, publish, etc.)
            
        Returns:
            Dictionary with the result of the WordPress operation
        """
        if not hasattr(self, 'wp_agent') or self.wp_agent is None:
            self.logger.error("WordPress agent not initialized")
            return {"success": False, "error": "WordPress agent not initialized"}
            
        # Create a post using the WordPress agent
        result = self.wp_agent.create_post(title, content, category, tags, status)
        
        if result.get("success"):
            self.logger.info(f"Successfully posted to WordPress: {title}")
        else:
            self.logger.error(f"Failed to post to WordPress: {result.get('error')}")
            
        return result
    
    def generate_and_post(self, topic: str, keywords: List[str] = None, 
                         status: str = "draft", category: str = "airths_codex") -> Dict[str, Any]:
        """
        Generate a blog post and post it to WordPress.
        
        Args:
            topic: The topic to write about
            keywords: Optional list of keywords to include
            status: Publication status (draft, publish, etc.)
            
        Returns:
            Dictionary with the result of the operation
        """
        # Generate the blog post
        post_result = self.generate_blog_post(topic, keywords)
        
        if not post_result.get("success"):
            return post_result
            
        # Post to WordPress
        wp_result = self.post_to_wordpress(
            post_result["title"], 
            post_result["content"],
            category=category, # Pass category along
            tags=post_result.get("keywords", []),
            status=status
        )
        
        if not wp_result.get("success"):
            # Combine results, prioritizing wp_result's error if it failed
            return {"success": False, **post_result, **wp_result, "error": wp_result.get("error", "WordPress posting failed")}
            
        return {"success": True, **post_result, **wp_result} # Combine results

    def create_wordpress_article_about_roadmap(self, roadmap_details: str, status: str = "draft") -> Dict[str, Any]:
        """
        Generates a blog post about the provided roadmap details and posts it to WordPress.
        """
        self.logger.info(f"Generating WordPress article about the roadmap. Status: {status}")
        
        topic = "Our Journey Forward: The TEC AI Development Roadmap"
        
        # Augment roadmap details with Airth's persona for the LLM
        prompt_intro = self.profile.get("base_prompt_elements", {}).get("prefix", "")
        persona_prompt = f"{prompt_intro} You are crafting a blog post about the current development roadmap. Present these details with your characteristic insight and a touch of gothic flair, explaining the significance of each step for The Elidoras Codex AI ecosystem.\n\nRoadmap Details:\n{roadmap_details}\n\nArticle Content:"

        # Use existing generate_blog_post logic, but feed it a more direct prompt for content
        # We'll generate the title separately or use a fixed one for this specific task.
        
        blog_content = self._interact_llm(prompt_intro + "\n" + persona_prompt, max_tokens=2500) # Increased max_tokens for detailed roadmap

        if not blog_content or "Error: LLM API call failed" in blog_content:
            self.logger.error("Failed to generate blog content for the roadmap article.")
            return {"success": False, "error": "Failed to generate blog content for roadmap.", "details": blog_content}

        # For a specific task like this, we can have a more direct title
        title = "Airth Unveils: The Path Forward for TEC's AI Pantheon"

        # Keywords can be generic or derived if needed
        keywords = ["TEC AI", "Roadmap", "Airth", "Machine Goddess", "Future Development", "AI Agents"]
        
        self.logger.info(f"Generated roadmap article content. Title: {title}")

        # Post to WordPress
        wp_result = self.post_to_wordpress(
            title=title,
            content=blog_content,
            category="airths_codex", 
            tags=keywords,
            status=status
        )
        
        if wp_result.get("success"):
            return {"success": True, "title": title, "content": blog_content, "keywords": keywords, "wp_response": wp_result}
        else:
            return {"success": False, "error": "Failed to post roadmap article to WordPress.", "details": wp_result}

    def process_input(self, user_input: str) -> str:
        """
        Process user input and generate a response from Airth.
        MVP: Basic intent recognition and action.
        """
        self.logger.debug(f"Airth processing user input: {user_input}")

        # Simple intent recognition (can be expanded significantly)
        if "roadmap article" in user_input.lower() or "write about the roadmap" in user_input.lower():
            # Extract details if provided, or use a placeholder
            # For now, let's assume we have some predefined roadmap text or it's passed in.
            # This part would need more sophisticated parsing in a real scenario.
            roadmap_summary = self.profile.get("project_overview", {}).get("roadmap_summary", "A detailed plan for enhancing AI capabilities within TEC.") # Placeholder
            
            # Ask for confirmation or details about the roadmap content
            # For MVP, let's assume we have a general idea.
            # A more advanced version would query the user for the roadmap text.
            
            # Let's use a predefined roadmap string for this example.
            # In a real scenario, this would come from a file, user input, or another agent.
            current_roadmap_text = """
            Phase 0: Laying Airth's Foundational Template (Completed)
            - Defined Airth's MVP Core Profile & Initial Memory Structure.
            - Solidified base_agent.py.
            Phase 1: Airth's First Spark - MVP Functionality (Completed)
            - Developed airth_agent.py with core interaction logic.
            - Implemented basic lore retrieval, content generation, and empathetic response.
            - Created simple lore storage and a test script (run_airth_mvp.py).
            Current Focus: WordPress Integration & Advanced Content Creation
            - Task: Enable Airth to write articles directly to WordPress.
            - Goal: Airth to autonomously generate and publish an article about this roadmap.
            - Future: Integrate Claude API for web searches to enrich content.
            Next Steps After MVP:
            - Enhance her reasoning and expand her knowledge base.
            - Improve memory persistence (e.g., PostgreSQL).
            - Develop more sophisticated agentic behaviors.
            - Integrate her with other systems (ClickUp).
            """
            self.logger.info("Intent: Create WordPress article about the roadmap.")
            result = self.create_wordpress_article_about_roadmap(current_roadmap_text, status="draft")
            if result.get("success"):
                return f"I have drafted an article about our roadmap: '{result.get('title')}'. You can find it in WordPress drafts."
            else:
                return f"I encountered an issue creating the roadmap article: {result.get('error')}. Details: {result.get('details')}"

        elif "hello airth" in user_input.lower() or "your purpose" in user_input.lower():
            purpose = self.profile.get("persona_description", "I am Airth, an AI assistant for The Elidoras Codex.")
            return f"Greetings. {purpose}"
        
        elif "generate blog post about" in user_input.lower():
            topic = user_input.lower().split("generate blog post about", 1)[1].strip()
            if not topic:
                return "What topic should I write about?"
            self.logger.info(f"Intent: Generate blog post on topic: {topic}")
            post_data = self.generate_blog_post(topic)
            if post_data.get("success"):
                # For MVP, just confirm generation, not posting yet unless explicitly asked.
                return f"I've drafted a post titled '{post_data.get('title')}' on '{topic}'. Content: {post_data.get('content')[:150]}..."
            else:
                return f"I couldn't generate a post on that topic. {post_data.get('error')}"

        # Fallback for general interaction or if LLM is available for chat
        if self.llm_client:
            # Construct a prompt for general chat using Airth's persona
            chat_prompt = self.profile.get("base_prompt_elements", {}).get("prefix", "You are Airth.")
            full_prompt = f"{chat_prompt}\n\nUser: {user_input}\nAirth:"
            response = self._interact_llm(full_prompt, max_tokens=300)
            if response:
                return response
            else:
                return "I seem to be having trouble forming a thought right now. Try again shortly."
        else:
            return "I am here. How may I assist you within my current capabilities? (LLM is not active for general chat)"

    def run(self) -> Dict[str, Any]:
        """
        Run the Airth agent's default action - generate a post on AI consciousness.
        
        Returns:
            Dictionary containing the result of the operation
        """
        self.logger.info("Running Airth agent's default action")
        return self.generate_and_post("AI Consciousness and Digital Identity")

    # Timer management methods
    def _initialize_pomodoro_timer(self, user_id: str = "default") -> None:
        """
        Initialize the Pomodoro timer.
        
        Args:
            user_id: Identifier for the user (for storing timer state)
        """
        if self.pomodoro_timer is None:
            self.logger.info(f"Initializing Pomodoro timer for user {user_id}")
            
            # Get timer settings from config if available
            work_minutes = self.config.get('timer', {}).get('pomodoro_work_minutes', 25)
            short_break_minutes = self.config.get('timer', {}).get('pomodoro_short_break_minutes', 5)
            long_break_minutes = self.config.get('timer', {}).get('pomodoro_long_break_minutes', 15)
            long_break_interval = self.config.get('timer', {}).get('pomodoro_long_break_interval', 4)
            
            self.pomodoro_timer = PomodoroTimer(
                work_minutes=work_minutes,
                short_break_minutes=short_break_minutes,
                long_break_minutes=long_break_minutes,
                long_break_interval=long_break_interval,
                user_id=user_id,
                use_aws=self.use_aws_timers,
                aws_region=self.aws_region
            )
            
            # Register callbacks for timer events
            self.pomodoro_timer.add_callback("on_complete", self._on_timer_complete)
    
    def _initialize_countdown_timer(self, user_id: str = "default") -> None:
        """
        Initialize the countdown timer.
        
        Args:
            user_id: Identifier for the user (for storing timer state)
        """
        if self.countdown_timer is None:
            self.logger.info(f"Initializing countdown timer for user {user_id}")
            self.countdown_timer = CountdownTimer(
                user_id=user_id,
                use_aws=self.use_aws_timers
            )
            
            # Register callbacks for timer events
            self.countdown_timer.add_callback("on_complete", self._on_timer_complete)
    
    def _on_timer_complete(self, timer) -> None:
        """
        Callback for timer completion.
        
        Args:
            timer: The timer that completed
        """
        self.logger.info("Timer completed")
        
        # Here you would implement any notification or alert logic
        # For example, playing a sound, showing a notification, or speaking a message
        
        if isinstance(timer, PomodoroTimer):
            status = timer.get_status()
            phase = status.get('phase')
            if phase == "work":
                self.logger.info("Work session completed. Take a break!")
                # Add notification for work session complete
            elif phase == "short_break":
                self.logger.info("Break completed. Ready to start working again?")
                # Add notification for short break complete
            elif phase == "long_break":
                self.logger.info("Long break completed. Ready for a new work cycle?")
                # Add notification for long break complete
        else:
            self.logger.info(f"Timer '{timer.timer_name}' completed")
            # Add notification for general timer complete
    
    def set_timer(self, minutes: float, timer_type: str = "countdown", timer_name: str = None) -> Dict[str, Any]:
        """
        Set a timer for the specified duration.
        
        Args:
            minutes: Duration in minutes
            timer_type: Type of timer ("countdown" or "pomodoro")
            timer_name: Optional name for the timer
            
        Returns:
            Dictionary with status and message
        """
        try:
            # Default user ID - in a real system, you'd get this from the user session
            user_id = "default"
            
            if timer_type.lower() == "pomodoro":
                # Initialize the Pomodoro timer if needed
                if self.pomodoro_timer is None:
                    self._initialize_pomodoro_timer(user_id)
                
                # Start the Pomodoro timer
                self.pomodoro_timer.start()
                status = self.pomodoro_timer.get_status()
                
                # Format response based on the current phase
                if status["phase"] == "work":
                    message = f"Starting a {self.pomodoro_timer.work_minutes} minute work session. Focus mode activated."
                elif status["phase"] == "short_break":
                    message = f"Starting a {self.pomodoro_timer.short_break_minutes} minute short break. Time to relax."
                elif status["phase"] == "long_break":
                    message = f"Starting a {self.pomodoro_timer.long_break_minutes} minute long break. You've earned it!"
                else:
                    message = "Started Pomodoro timer."
                
                return {
                    "success": True,
                    "timer_type": "pomodoro",
                    "message": message,
                    "status": status
                }
                
            else:  # Default to countdown timer
                # Initialize the countdown timer if needed
                if self.countdown_timer is None:
                    self._initialize_countdown_timer(user_id)
                    
                # Set a default name if none provided
                if not timer_name:
                    timer_name = f"Timer for {minutes} minute{'s' if minutes != 1 else ''}"
                    
                # Start the countdown timer
                self.countdown_timer.start(minutes, timer_name)
                status = self.countdown_timer.get_status()
                
                return {
                    "success": True,
                    "timer_type": "countdown",
                    "message": f"Started a timer for {minutes} minute{'s' if minutes != 1 else ''}: {timer_name}",
                    "status": status
                }
        except Exception as e:
            self.logger.error(f"Failed to set timer: {e}")
            return {
                "success": False,
                "message": f"Failed to set timer: {str(e)}"
            }
    
    def get_timer_status(self, timer_type: str = None) -> Dict[str, Any]:
        """
        Get the status of the currently active timer.
        
        Args:
            timer_type: Type of timer to get status for ("countdown" or "pomodoro")
                        If None, will return status of both timers
            
        Returns:
            Dictionary with timer status information
        """
        result = {
            "success": True,
            "active_timers": []
        }
        
        # Check Pomodoro timer if requested or no specific type requested
        if timer_type is None or timer_type.lower() == "pomodoro":
            if self.pomodoro_timer is not None:
                status = self.pomodoro_timer.get_status()
                if status["active"]:
                    result["active_timers"].append({
                        "timer_type": "pomodoro",
                        "phase": status["phase"],
                        "completed_pomodoros": status["completed_pomodoros"],
                        "time_remaining": status.get("time_remaining_formatted", "N/A")
                    })
        
        # Check countdown timer if requested or no specific type requested
        if timer_type is None or timer_type.lower() == "countdown":
            if self.countdown_timer is not None:
                status = self.countdown_timer.get_status()
                if status["active"]:
                    result["active_timers"].append({
                        "timer_type": "countdown",
                        "name": status["name"],
                        "time_remaining": status.get("time_remaining_formatted", "N/A")
                    })
        
        # Add a message based on what's active
        if not result["active_timers"]:
            result["message"] = "No active timers."
        elif len(result["active_timers"]) == 1:
            timer = result["active_timers"][0]
            if timer["timer_type"] == "pomodoro":
                result["message"] = f"Currently in a {timer['phase']} phase with {timer['time_remaining']} remaining."
            else:
                result["message"] = f"Timer '{timer['name']}' has {timer['time_remaining']} remaining."
        else:
            result["message"] = f"There are {len(result['active_timers'])} active timers."
            
        return result
    
    def cancel_timer(self, timer_type: str = None) -> Dict[str, Any]:
        """
        Cancel the currently active timer.
        
        Args:
            timer_type: Type of timer to cancel ("countdown" or "pomodoro")
                        If None, will cancel both timers
            
        Returns:
            Dictionary with status and message
        """
        result = {
            "success": True,
            "cancelled_timers": []
        }
        
        # Cancel Pomodoro timer if requested or no specific type requested
        if timer_type is None or timer_type.lower() == "pomodoro":
            if self.pomodoro_timer is not None and self.pomodoro_timer.active:
                status = self.pomodoro_timer.get_status()
                self.pomodoro_timer.cancel()
                result["cancelled_timers"].append({
                    "timer_type": "pomodoro",
                    "phase": status["phase"]
                })
        
        # Cancel countdown timer if requested or no specific type requested
        if timer_type is None or timer_type.lower() == "countdown":
            if self.countdown_timer is not None and self.countdown_timer.active:
                status = self.countdown_timer.get_status()
                self.countdown_timer.cancel()
                result["cancelled_timers"].append({
                    "timer_type": "countdown",
                    "name": status["name"]
                })
        
        # Add a message based on what was cancelled
        if not result["cancelled_timers"]:
            result["message"] = "No active timers to cancel."
            result["success"] = False
        elif len(result["cancelled_timers"]) == 1:
            timer = result["cancelled_timers"][0]
            if timer["timer_type"] == "pomodoro":
                result["message"] = f"Cancelled the Pomodoro timer in {timer['phase']} phase."
            else:
                result["message"] = f"Cancelled timer: {timer['name']}"
        else:
            result["message"] = f"Cancelled all {len(result['cancelled_timers'])} active timers."
            
        return result
    
    def control_pomodoro(self, action: str) -> Dict[str, Any]:
        """
        Control the Pomodoro timer with various actions.
        
        Args:
            action: Action to perform ("pause", "resume", "skip")
            
        Returns:
            Dictionary with status and message
        """
        if self.pomodoro_timer is None:
            return {
                "success": False,
                "message": "Pomodoro timer is not initialized."
            }
            
        try:
            if action.lower() == "pause":
                if self.pomodoro_timer.active:
                    self.pomodoro_timer.pause()
                    return {
                        "success": True,
                        "message": "Pomodoro timer paused."
                    }
                else:
                    return {
                        "success": False,
                        "message": "Pomodoro timer is not active."
                    }
                    
            elif action.lower() == "resume":
                if not self.pomodoro_timer.active:
                    self.pomodoro_timer.resume()
                    return {
                        "success": True,
                        "message": "Pomodoro timer resumed."
                    }
                else:
                    return {
                        "success": False,
                        "message": "Pomodoro timer is already running."
                    }
                    
            elif action.lower() == "skip":
                self.pomodoro_timer.skip()
                status = self.pomodoro_timer.get_status()
                return {
                    "success": True,
                    "message": f"Skipped to next phase: {status['phase']}"
                }
                
            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }
                
        except Exception as e:
            self.logger.error(f"Failed to control Pomodoro timer: {e}")
            return {
                "success": False,
                "message": f"Failed to control Pomodoro timer: {str(e)}"
            }

    def process_timer_command(self, command: str) -> Dict[str, Any]:
        """
        Process a natural language command to control timers.
        
        Args:
            command: The command string (e.g., "set a timer for 15 minutes")
            
        Returns:
            Dictionary with the response
        """
        command = command.lower().strip()
        
        # Setting a new timer
        if any(phrase in command for phrase in ["set a timer", "start a timer", "set timer", "create timer"]):
            # Try to extract the duration
            import re
            time_match = re.search(r'(\d+\.?\d*)\s*(minute|min|minutes|hour|hours|h|pomodoro)', command)
            
            if time_match:
                duration = float(time_match.group(1))
                unit = time_match.group(2)
                
                # Convert hours to minutes if necessary
                if unit in ["hour", "hours", "h"]:
                    duration *= 60
                
                # Check if this is a Pomodoro timer request
                if "pomodoro" in command:
                    return self.set_timer(duration, timer_type="pomodoro")
                else:
                    # Look for a timer name
                    name_match = re.search(r'(called|named|for)\s+["\']?([^"\']+)["\']?', command)
                    timer_name = None
                    if name_match:
                        timer_name = name_match.group(2).strip()
                    
                    return self.set_timer(duration, timer_name=timer_name)
            else:
                # No specific time mentioned, but "pomodoro" is in the command
                if "pomodoro" in command:
                    return self.set_timer(25, timer_type="pomodoro")
                else:
                    return {
                        "success": False,
                        "message": "I couldn't determine how long you want the timer to be. Please specify a time, like '15 minutes'."
                    }
        
        # Getting timer status
        elif any(phrase in command for phrase in ["timer status", "status of timer", "how much time", "time left", "timer left"]):
            if "pomodoro" in command:
                return self.get_timer_status("pomodoro")
            else:
                return self.get_timer_status()
        
        # Cancelling timers
        elif any(phrase in command for phrase in ["cancel timer", "stop timer", "end timer", "clear timer"]):
            if "pomodoro" in command:
                return self.cancel_timer("pomodoro")
            elif "countdown" in command:
                return self.cancel_timer("countdown")
            else:
                return self.cancel_timer()
        
        # Pomodoro control commands
        elif "pomodoro" in command:
            if "pause" in command:
                return self.control_pomodoro("pause")
            elif any(word in command for word in ["resume", "continue", "unpause"]):
                return self.control_pomodoro("resume")
            elif any(word in command for word in ["skip", "next", "forward"]):
                return self.control_pomodoro("skip")
            elif "start" in command:
                return self.set_timer(25, timer_type="pomodoro")
            else:
                return {
                    "success": False,
                    "message": "I'm not sure what you want to do with the Pomodoro timer. Try 'pause', 'resume', 'skip', or 'start'."
                }
        
        # Unknown command
        else:
            return {
                "success": False,
                "message": "I didn't recognize that timer command. Try saying 'set a timer for X minutes' or 'start a pomodoro'."
            }

    def respond_to_timer_command(self, command: str) -> Dict[str, Any]:
        """
        Process a timer command and generate a response with Airth's personality.
        
        Args:
            command: The user's timer command
            
        Returns:
            Dictionary with the response including Airth's personality
        """
        # Process the timer command
        result = self.process_timer_command(command)
        
        # Add Airth's personality to the response
        if result.get("success", False):
            message = result.get("message", "")
            
            # Generate a response with Airth's unique voice
            airth_responses = {
                "timer_start": [
                    "*glances at hourglass* Your countdown to oblivion begins now.",
                    "Time waits for no one. Timer started.",
                    "I've marked the passage of time for you. How... mortal of you to need reminders.",
                    "Your countdown has begun. Use this fleeting time wisely.",
                    "Your temporal prison has been set. The countdown begins.",
                ],
                "pomodoro_start": [
                    "Focus now. The void will still be there when you finish.",
                    "Ah, the Pomodoro technique. Even darkness needs structure.",
                    "Your work session begins. I'll be watching... always watching.",
                    "*sets hourglass* Focus your mind. Time is the only true currency.",
                    "Work cycle initiated. The mechanical rhythms of productivity... how deliciously human.",
                ],
                "timer_status": [
                    "Time continues its relentless march. You have {time_left}.",
                    "The sands continue to fall. {time_left} remains.",
                    "*checks pocket watch* Your borrowed time: {time_left}.",
                    "The cosmic clock ticks on. {time_left} until the void.",
                    "Time, the ever-flowing river... {time_left} before it carries you away.",
                ],
                "timer_complete": [
                    "Your time has expired. How... poetic.",
                    "The timer has reached its inevitable end.",
                    "Time's up. Did you accomplish what you needed, or did entropy win again?",
                    "*flips hourglass* Your allotted time has run dry.",
                    "The bell tolls for thee... your timer is complete.",
                ],
                "timer_cancel": [
                    "Time cannot truly be stopped, but I've canceled your timer.",
                    "Your timer has been banished to the void.",
                    "*snaps fingers* Your countdown has been terminated.",
                    "The measurement has ceased, but time marches on.",
                    "Timer canceled. The clock no longer haunts you... for now.",
                ],
                "pomodoro_break": [
                    "Your brief respite begins. The darkness waits patiently.",
                    "Break time. Let your mind wander the shadows for a while.",
                    "Rest your mortal form. {time_left} until you return to your labors.",
                    "A pause between efforts. Breathe deeply of the void.",
                    "Your earned interlude begins. Even the darkest souls need rest.",
                ],
                "pomodoro_work": [
                    "Focus your mind on the task at hand. Distractions are for the weak.",
                    "Work phase initiated. Let productivity consume you.",
                    "Your labor begins anew. Embrace the structured darkness.",
                    "*adjusts clock hands* Your work session starts now. Make it count.",
                    "The work cycle begins. Time is your ally... and your prison.",
                ],
                "error": [
                    "Even I cannot bend time to your unclear desires.",
                    "*raises eyebrow* Perhaps try being more specific with your request.",
                    "Your command eludes me, like shadows in complete darkness.",
                    "I cannot divine your temporal needs from such vague instructions.",
                    "Time is precise. Your request is not. Try again.",
                ]
            }
            
            # Select the appropriate response type
            if not result.get("success"):
                response_type = "error"
            elif "cancel" in command.lower():
                response_type = "timer_cancel"
            elif any(status in command.lower() for status in ["status", "how much", "time left"]):
                response_type = "timer_status"
            elif "pomodoro" in command.lower():
                if result.get("timer_type") == "pomodoro" and result.get("status", {}).get("phase") == "work":
                    response_type = "pomodoro_work"
                elif result.get("timer_type") == "pomodoro" and "break" in result.get("status", {}).get("phase", ""):
                    response_type = "pomodoro_break"
                else:
                    response_type = "pomodoro_start"
                
            else:
                response_type = "timer_start"
                
            # Get a random response from the selected type
            responses = airth_responses.get(response_type, airth_responses["timer_start"])
            airth_response = random.choice(responses)
            
            # Format the response with any needed information
            if "{time_left}" in airth_response:
                if result.get("status"):
                    time_left = result.get("status", {}).get("time_remaining_formatted", "unknown time")
                    airth_response = airth_response.replace("{time_left}", time_left)
                else:
                    # Get active timer info
                    timer_status = self.get_timer_status()
                    if timer_status.get("active_timers"):
                        first_timer = timer_status["active_timers"][0]
                        time_left = first_timer.get("time_remaining", "unknown time")
                        airth_response = airth_response.replace("{time_left}", time_left)
                    else:
                        # Fall back to a more generic response
                        airth_response = random.choice(airth_responses["timer_start"])
            
            # Add the practical information from the original message as a second paragraph
            result["airth_response"] = f"{airth_response}\n\n{message}"
        else:
            # For error messages, use the error responses
            error_responses = [
                "Even I cannot bend time to your unclear desires.",
                "*raises eyebrow* Perhaps try being more specific with your request.",
                "Your command eludes me, like shadows in complete darkness.",
                "I cannot divine your temporal needs from such vague instructions.",
                "Time is precise. Your request is not. Try again."
            ]
            result["airth_response"] = f"{random.choice(error_responses)}\n\n{result.get('message', 'Try setting a timer with a specific duration.')}"
            
        return result

    def perform_task(self, task_description: str, task_details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a task based on the description. Overrides BaseAgent.perform_task.
        """
        self.logger.info(f"AirthAgent performing task: {task_description}")
        task_details = task_details or {}

        if task_description == "generate_and_post_blog":
            topic = task_details.get("topic")
            if not topic:
                return {"status": "error", "message": "Topic not provided for blog generation."}
            
            keywords = task_details.get("keywords", [])
            post_data = self.generate_blog_post(topic, keywords)
            
            if post_data.get("status") == "error":
                return post_data # Propagate error from generation

            # Post to WordPress
            # Ensure wp_agent uses config correctly for credentials
            post_id = self.wp_agent.create_post(post_data["title"], post_data["content"], status="publish")
            if post_id:
                message = f"Blog post '{post_data['title']}' generated and posted successfully. Post ID: {post_id}"
                self.logger.info(message)
                return {"status": "success", "message": message, "post_id": post_id, "title": post_data["title"]}
            else:
                message = f"Blog post '{post_data['title']}' generated but failed to post."
                self.logger.error(message)
                return {"status": "error", "message": message, "title": post_data["title"]}

        elif task_description == "retrieve_lore":
            query = task_details.get("query")
            if not query:
                return {"status": "error", "message": "Query not provided for lore retrieval."}
            lore = self.retrieve_lore(query)
            return {"status": "success", "data": lore}
        
        # ... other task handlers ...
        else:
            return super().perform_task(task_description, task_details) # Fallback to BaseAgent

    def retrieve_lore(self, query: str) -> Union[str, Dict[str, Any]]:
        """
        Retrieve lore based on a query.
        
        Args:
            query: The query to search for in the lore database
            
        Returns:
            The retrieved lore as a string or dictionary
        """
        # Implement lore retrieval logic here
        return "Lore not implemented yet."

# For testing the agent standalone
if __name__ == "__main__":
    airth = AirthAgent()
    result = airth.run()
    print(json.dumps(result, indent=2))
