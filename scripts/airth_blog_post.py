#!/usr/bin/env python3
"""
Generate and post a blog article using Airth.
This script creates a blog post and publishes it to WordPress.
"""
import os
import sys
import json
import argparse
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv(os.path.join('config', '.env'))

# Import the Airth agent
from src.agents import AirthAgent

def main():
    """Generate and post a blog article."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate and post a blog article using Airth')
    parser.add_argument('--topic', help='Topic for the blog post')
    parser.add_argument('--keywords', help='Comma-separated list of keywords')
    parser.add_argument('--status', choices=['draft', 'publish'], default='draft', 
                      help='Publication status (default: draft)')
    
    args = parser.parse_args()
    
    # Use default topic if not provided
    topic = args.topic or "AI Consciousness and Digital Identity"
    
    # Parse keywords if provided
    keywords = []
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]
    
    print(f"Generating blog post on topic: {topic}")
    print(f"Keywords: {', '.join(keywords) if keywords else 'None'}")
    print(f"Status: {args.status}")
    
    # Initialize Airth agent
    airth = AirthAgent(os.path.join('config'))
    
    # Generate and post the blog
    result = airth.generate_and_post(topic, keywords, args.status)
    
    # Display the result
    if result.get("success"):
        print("\n✅ Blog post generated and posted successfully!")
        print(f"Title: {result.get('title')}")
        print(f"Status: {result.get('status')}")
        print(f"URL: {result.get('url')}")
        print(f"Post ID: {result.get('post_id')}")
    else:
        print("\n❌ Failed to generate or post the blog")
        print(f"Error: {result.get('error')}")
    
    print("\nFull result:")
    print(json.dumps(result, indent=2))
    
    return 0 if result.get("success") else 1

if __name__ == "__main__":
    sys.exit(main())
