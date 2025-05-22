"""
AirthAgent response method for handling user requests
"""
import logging
from typing import Dict, Any, List, Optional, Union

def respond(self, user_input: str, history: Optional[List[List[str]]] = None) -> str:
    """
    Respond to user input, optionally taking into account conversation history.
    This is the primary interface method for the Gradio app.
    
    Args:
        user_input: The user's message or request
        history: Optional list of previous [user, assistant] message pairs
        
    Returns:
        Airth's response as a string
    """
    self.logger.info(f"Airth responding to: {user_input[:50]}...")
    
    # Check for special commands or intents
    lower_input = user_input.lower()
    
    # Timer-related commands
    if any(keyword in lower_input for keyword in ["timer", "countdown", "pomodoro"]):
        result = self.respond_to_timer_command(user_input)
        return result.get("airth_response", "I'll help you manage your time.")
    
    # Blog-related commands
    elif any(keyword in lower_input for keyword in ["post to blog", "create blog post", "publish article"]):
        # Extract the topic from the command
        import re
        topic_match = re.search(r'(about|on|for)\s+["\']?([^"\']+)["\']?', lower_input)
        if topic_match:
            topic = topic_match.group(2)
            result = self.generate_blog_post(topic)
            if result.get("success"):
                return f"I've created a blog post titled '{result.get('title')}'. Would you like me to post it to WordPress?"
            else:
                return f"I couldn't generate a blog post: {result.get('error', 'Unknown error')}"
        else:
            return "What would you like me to blog about? Please provide a topic."
    
    # General conversational response
    else:
        # Prepare the prompt with Airth's personality and the user's input
        prompt_base = self.profile.get("base_prompt_elements", {}).get("prefix", "")
        prompt = f"{prompt_base}\n\nUser: {user_input}"
        
        # Include conversation history if available
        if history and len(history) > 0:
            context = "Previous conversation:\n"
            # Include up to 3 previous exchanges (or fewer if not available)
            for i in range(max(0, len(history) - 3), len(history)):
                context += f"User: {history[i][0]}\nAirth: {history[i][1]}\n"
            prompt = f"{prompt_base}\n\n{context}\nUser: {user_input}"
        
        # Generate response with the LLM
        response = self._interact_llm(prompt, max_tokens=1000)
        
        if not response or "Error: LLM API call failed" in response:
            self.logger.error(f"Failed to generate response for: {user_input}")
            return "I'm having trouble connecting to my thoughts right now. Can we try again in a moment?"
        
        return response
