#!/bin/bash
# Script to securely create .env file with proper permissions

# Navigate to the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/config/.env"
ENV_TEMPLATE="$PROJECT_ROOT/config/.env.template"

# Check if .env file already exists
if [ -f "$ENV_FILE" ]; then
    read -p "The .env file already exists. Do you want to overwrite it? (y/n): " overwrite
    if [[ "$overwrite" != "y" && "$overwrite" != "Y" ]]; then
        echo "Operation cancelled."
        exit 0
    fi
fi

# Check if template exists
if [ ! -f "$ENV_TEMPLATE" ]; then
    echo "Error: .env.template file not found at $ENV_TEMPLATE"
    exit 1
fi

# Copy template to .env
cp "$ENV_TEMPLATE" "$ENV_FILE"

# Set restrictive permissions
chmod 600 "$ENV_FILE"

# Function to update a variable in the .env file
update_env_var() {
    local var_name="$1"
    local var_prompt="$2"
    local is_sensitive="${3:-false}"
    
    local current_value=$(grep -oP "^$var_name=\K.*" "$ENV_FILE" || echo "")
    
    # If it's a sensitive value, don't show the current value in the prompt
    if [ "$is_sensitive" = "true" ] && [ ! -z "$current_value" ] && [ "$current_value" != "your_"* ]; then
        echo -n "$var_prompt [currently set - press Enter to keep]: "
        read -s new_value
        echo
    else
        echo -n "$var_prompt [current: $current_value]: "
        if [ "$is_sensitive" = "true" ]; then
            read -s new_value
            echo
        else
            read new_value
        fi
    fi
    
    # Only update if a new value was provided
    if [ ! -z "$new_value" ]; then
        # Replace existing value or add new variable
        if grep -q "^$var_name=" "$ENV_FILE"; then
            sed -i "s|^$var_name=.*|$var_name=$new_value|" "$ENV_FILE"
        else
            echo "$var_name=$new_value" >> "$ENV_FILE"
        fi
        echo "Updated $var_name."
    else
        echo "Kept existing value for $var_name."
    fi
}

echo "Configuring WordPress Settings..."
update_env_var "WP_URL" "WordPress URL (e.g., https://yourdomain.com)"
update_env_var "WP_USERNAME" "WordPress Username"
update_env_var "WP_PASSWORD" "WordPress Application Password (create in WordPress admin)" "true"
update_env_var "WP_XMLRPC_PATH" "WordPress XMLRPC Path (default: /xmlrpc.php)"

echo -e "\nConfiguring AI Providers..."
update_env_var "OPENAI_API_KEY" "OpenAI API Key" "true"
update_env_var "OPENAI_MODEL" "OpenAI Model (default: gpt-4-turbo)"
update_env_var "ANTHROPIC_API_KEY" "Anthropic API Key (optional)" "true"

echo -e "\nConfiguring Logging..."
update_env_var "LOG_LEVEL" "Log Level (INFO, DEBUG, WARNING, ERROR)"
update_env_var "DEBUG" "Debug Mode (true/false)"

echo -e "\nEnvironment configuration complete!"
echo "Your .env file has been created at: $ENV_FILE"
echo "IMPORTANT: This file contains sensitive information. Do not commit it to version control."
