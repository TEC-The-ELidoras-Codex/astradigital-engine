import argparse
import json
import os
import sys

# Add the project root to the Python path to allow importing from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.agents.wp_poster import WordPressAgent

def main():
    parser = argparse.ArgumentParser(description="Post an article from a JSON file to WordPress.")
    parser.add_argument("json_file", help="Path to the JSON file containing the article data.")
    parser.add_argument("--status", default="draft", help="Status of the post (e.g., 'draft', 'publish'). Default is 'draft'.")
    args = parser.parse_args()

    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {args.json_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {args.json_file}")
        return

    title = article_data.get("title")
    content = article_data.get("content")
    tags = article_data.get("keywords")  # Use 'keywords' as 'tags'
    category = article_data.get("category") # This will be a string

    if not title or not content:
        print("Error: JSON file must contain 'title' and 'content' fields.")
        return

    wp_agent = WordPressAgent()

    post_payload = {
        "title": title,
        "content": content,
        "status": args.status
    }

    if category:
        post_payload["categories"] = [category] # wp_poster handles slug to ID conversion
    
    if tags and isinstance(tags, list):
        post_payload["tags"] = tags # wp_poster handles tag name to ID conversion/creation

    print(f"Attempting to post article: '{title}' with status '{args.status}'...")
    result = wp_agent.create_post(post_payload)

    if result.get("success"):
        print("Article posted successfully!")
        print(f"Post ID: {result.get('id')}")
        print(f"Post URL: {result.get('link')}")
    else:
        print("Failed to post article.")
        print(f"Error: {result.get('error')}")
        if result.get('status_code'):
            print(f"Status Code: {result.get('status_code')}")

if __name__ == "__main__":
    main()
