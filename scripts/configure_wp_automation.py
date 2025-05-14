#!/usr/bin/env python3
"""
WordPress Configuration Update Script for Airth News Automation.
This utility helps configure and test WordPress integration for automated news publishing.
"""
import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv
import requests
import base64
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.WordPressSetup")

# Find project root and load environment
script_dir = Path(__file__).parent
proj_root = script_dir.parent
env_path = proj_root / "config" / ".env"

def update_env_file(app_password=None, url=None, username=None, app_password_name=None):
    """Update the WordPress configuration in the .env file."""
    if not any([app_password, url, username, app_password_name]):
        logger.error("No values provided to update")
        return False
        
    try:
        # Read current .env content
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Find the WordPress configuration section and update values
        wp_section_found = False
        new_lines = []
        
        for line in lines:
            # Start of WordPress section
            if "# WordPress Configuration" in line:
                wp_section_found = True
                new_lines.append(line)
                continue
                
            # We're in the WordPress section
            if wp_section_found:
                if url and line.strip().startswith("WP_URL="):
                    new_lines.append(f"WP_URL={url}\n")
                elif username and line.strip().startswith("WP_USERNAME="):
                    new_lines.append(f"WP_USERNAME={username}\n")
                elif app_password and line.strip().startswith("WP_PASSWORD="):
                    new_lines.append(f"WP_PASSWORD={app_password}\n")
                elif app_password_name and line.strip().startswith("WP_APP_PASSWORD_NAME="):
                    new_lines.append(f"WP_APP_PASSWORD_NAME={app_password_name}\n")
                else:
                    new_lines.append(line)
                    
                # If we detect a new section, stop processing WP section
                if line.startswith("#") and "WordPress Configuration" not in line and not line.strip().startswith("#"):
                    wp_section_found = False
            else:
                new_lines.append(line)
                
        # Write the updated content back to the file
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
        logger.info("WordPress configuration updated successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error updating .env file: {e}")
        return False

def test_wp_connection(wp_url=None, wp_username=None, wp_password=None):
    """Test the WordPress connection with provided or environment credentials."""
    # Use provided values or fall back to env vars
    wp_url = wp_url or os.getenv("WP_URL")
    wp_username = wp_username or os.getenv("WP_USERNAME")
    wp_password = wp_password or os.getenv("WP_PASSWORD")
    
    if not all([wp_url, wp_username, wp_password]):
        logger.error("Missing required WordPress credentials")
        return False
        
    # Make sure URL doesn't end with a slash
    wp_url = wp_url.rstrip('/')
    
    # REST API endpoint
    api_url = f"{wp_url}/wp-json/wp/v2/users/me"
    
    # Try application password with spaces
    auth_string = f"{wp_username}:{wp_password}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_encoded}',
        'Content-Type': 'application/json'
    }
    
    try:
        logger.info(f"Testing WordPress REST API connection to {api_url}")
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            logger.info(f"✅ WordPress authentication successful!")
            logger.info(f"Logged in as: {user_data.get('name', 'Unknown')}")
            logger.info(f"User role(s): {', '.join(user_data.get('roles', ['unknown']))}")
            
            # Check if user has posting capabilities
            if "administrator" in user_data.get('roles', []) or "editor" in user_data.get('roles', []) or "author" in user_data.get('roles', []):
                logger.info("✅ User has sufficient publishing permissions")
            else:
                logger.warning("⚠️ User may not have sufficient publishing permissions")
                
            # Now test XML-RPC if that path is available
            xmlrpc_path = os.getenv("WP_XMLRPC_PATH", "/xmlrpc.php")
            xmlrpc_url = f"{wp_url}{xmlrpc_path}"
            
            logger.info(f"Testing WordPress XML-RPC connection to {xmlrpc_url}")
            
            xmlrpc_data = {
                "methodName": "wp.getUsersBlogs",
                "params": [wp_username, wp_password]
            }
            
            xmlrpc_headers = {
                "Content-Type": "application/xml"
            }
            
            try:
                xmlrpc_response = requests.post(xmlrpc_url, data=json.dumps(xmlrpc_data), headers=xmlrpc_headers, timeout=10)
                if xmlrpc_response.status_code == 200:
                    logger.info("✅ XML-RPC connection successful")
                else:
                    logger.warning(f"⚠️ XML-RPC connection failed with status {xmlrpc_response.status_code}")
                    logger.warning("This is not critical as we will prefer REST API for publishing")
            except Exception as xmlrpc_err:
                logger.warning(f"⚠️ XML-RPC test failed: {str(xmlrpc_err)}")
                logger.warning("This is not critical as we will prefer REST API for publishing")
                
            return True
        else:
            logger.error(f"❌ WordPress authentication failed with status {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ WordPress connection error: {str(e)}")
        return False

def update_news_automation_configuration(max_age=None, max_topics=None, schedule_time=None):
    """Update the Airth News Automation configuration."""
    try:
        # Create a PowerShell command to set up the scheduled task
        ps_script = f"""
        $scriptPath = "c:\\Users\\Ghedd\\TEC_CODE\\astradigital-engine\\scripts\\airth_news_automation.py"
        $pythonExe = "python"
        
        # Set parameters
        $maxAge = {max_age if max_age else 2}
        $maxTopics = {max_topics if max_topics else 3}
        $triggerTime = "{schedule_time if schedule_time else '10:00'}"
        
        # Build the command
        $arguments = "$scriptPath --max-age $maxAge --max-topics $maxTopics --status draft"
        
        # Display configuration
        Write-Host "Airth News Automation Configuration:"
        Write-Host "=================================="
        Write-Host "Script Path: $scriptPath"
        Write-Host "Max Age: $maxAge days"
        Write-Host "Max Topics: $maxTopics"
        Write-Host "Schedule Time: $triggerTime"
        Write-Host "Status: draft"
        Write-Host "=================================="
        
        # Explain task registration (without actually doing it due to permissions issues)
        Write-Host "To register this task in Task Scheduler, run the following command as administrator:"
        Write-Host ""
        Write-Host "Register-ScheduledTask -TaskName 'AirthNewsAutomation' -Action (New-ScheduledTaskAction -Execute $pythonExe -Argument \\"$arguments\\") -Trigger (New-ScheduledTaskTrigger -Daily -At $triggerTime) -User \\"$env:USERNAME\\" -RunLevel Highest"
        """
        
        # Write the PowerShell script to a file
        ps_script_path = script_dir / "airth_news_config.ps1"
        with open(ps_script_path, 'w', encoding='utf-8') as f:
            f.write(ps_script)
        
        logger.info(f"Created PowerShell configuration script at {ps_script_path}")
        logger.info(f"Run this script as administrator to configure the scheduled task")
        
        return True
    except Exception as e:
        logger.error(f"Error updating automation configuration: {e}")
        return False

def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(description="Configure WordPress for Airth News Automation")
    
    parser.add_argument("--update-wp-config", action="store_true", 
                        help="Update WordPress configuration")
    parser.add_argument("--app-password", 
                        help="WordPress application password (with spaces)")
    parser.add_argument("--username", 
                        help="WordPress username")
    parser.add_argument("--url", 
                        help="WordPress site URL")
    parser.add_argument("--app-name", default="AirthNewsAutomation",
                        help="Name for the application password")
    
    parser.add_argument("--test-connection", action="store_true", 
                        help="Test WordPress connection")
    # Add an argument to directly pass the password for testing
    parser.add_argument("--test-password",
                        help="Directly provide password for connection test, bypassing .env for the test")
    
    parser.add_argument("--update-automation", action="store_true",
                        help="Update news automation configuration")
    parser.add_argument("--max-age", type=int, default=2,
                        help="Maximum age of news articles to fetch (days)")
    parser.add_argument("--max-topics", type=int, default=3, 
                        help="Maximum number of topics to generate")
    parser.add_argument("--schedule-time", default="10:00",
                        help="Time to run the automation (24-hour format)")
                        
    parser.add_argument("--instructions", action="store_true",
                        help="Show instructions for WordPress application password setup")
    
    args = parser.parse_args()
    
    # Load environment variables
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Loaded environment from {env_path}")
    else:
        logger.error(f"Could not find .env file at {env_path}")
        sys.exit(1)
    
    # Show instructions if requested
    if args.instructions:
        print("=" * 80)
        print("WORDPRESS APPLICATION PASSWORD SETUP")
        print("=" * 80)
        print("1. Log in to your WordPress admin panel")
        print("2. Go to Users → Profile (or Users → Your Profile)")
        print("3. Scroll down to the 'Application Passwords' section")
        print("4. Enter the name 'Airth News Automation'")
        print("5. Click 'Add New Application Password'")
        print("6. Copy the generated password (it will look like: xxxx xxxx xxxx xxxx xxxx xxxx)")
        print("7. Run this script with: --update-wp-config --app-password 'your new password'")
        print("=" * 80)
        print("IMPORTANT: Make sure your WordPress site is using HTTPS")
        print("           Application passwords require a secure connection.")
        print("=" * 80)
        return
    
    # Update WordPress configuration if requested
    if args.update_wp_config:
        if update_env_file(args.app_password, args.url, args.username, args.app_name):
            logger.info("WordPress configuration updated successfully")
        else:
            logger.error("Failed to update WordPress configuration")
    
    # Test WordPress connection if requested
    if args.test_connection:
        # If test_password is provided, use it directly for the test
        password_to_test = args.test_password if args.test_password else None
        if test_wp_connection(args.url, args.username, password_to_test):
            logger.info("WordPress connection test succeeded")
        else:
            logger.error("WordPress connection test failed")
    
    # Update automation configuration if requested
    if args.update_automation:
        if update_news_automation_configuration(args.max_age, args.max_topics, args.schedule_time):
            logger.info("News automation configuration updated successfully")
        else:
            logger.error("Failed to update news automation configuration")

if __name__ == "__main__":
    main()
