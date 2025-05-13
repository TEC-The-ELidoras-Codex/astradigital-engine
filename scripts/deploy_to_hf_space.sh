#!/bin/bash
# deploy_to_hf_space.sh
# Script to deploy TEC_OFFICE_REPO to Hugging Face Space

# Exit on error
set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RESET='\033[0m'

usage() {
    echo -e "${BLUE}Usage:${RESET} $0 ${YELLOW}[options]${RESET}"
    echo
    echo -e "${BLUE}Options:${RESET}"
    echo -e "  ${YELLOW}-u, --username USERNAME${RESET}  Hugging Face username or organization"
    echo -e "  ${YELLOW}-s, --space SPACENAME${RESET}   Hugging Face space name"
    echo -e "  ${YELLOW}-c, --create${RESET}           Create space if it doesn't exist"
    echo -e "  ${YELLOW}-h, --help${RESET}             Show this help message"
    echo
    echo -e "${BLUE}Examples:${RESET}"
    echo -e "  $0 -u your-username -s tec-office -c"
    echo -e "  $0 --username your-organization --space tec-agent-hub"
}

# Default values
CREATE_SPACE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -u|--username)
            USERNAME="$2"
            shift 2
            ;;
        -s|--space)
            SPACENAME="$2"
            shift 2
            ;;
        -c|--create)
            CREATE_SPACE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${RESET}"
            usage
            exit 1
            ;;
    esac
done

# Check required arguments
if [ -z "$USERNAME" ] || [ -z "$SPACENAME" ]; then
    echo -e "${RED}Error: Username and space name are required${RESET}"
    usage
    exit 1
fi

echo -e "${BLUE}=== TEC Office Hugging Face Space Deployment ===${RESET}"
echo -e "${BLUE}Username:${RESET} $USERNAME"
echo -e "${BLUE}Space:${RESET} $SPACENAME"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python is not installed${RESET}"
    exit 1
fi

# Check if the huggingface_connection.py script exists
HF_SCRIPT="scripts/huggingface_connection.py"
if [ ! -f "$HF_SCRIPT" ]; then
    echo -e "${RED}Error: $HF_SCRIPT script not found${RESET}"
    exit 1
fi

# Check if the space exists
echo -e "${BLUE}Checking if space exists...${RESET}"
python "$HF_SCRIPT" check "$USERNAME" "$SPACENAME"
SPACE_CHECK=$?

# Create the space if needed
if [ $SPACE_CHECK -ne 0 ] && [ "$CREATE_SPACE" = true ]; then
    echo -e "${YELLOW}Space does not exist. Creating...${RESET}"
    python "$HF_SCRIPT" create "$USERNAME" "$SPACENAME" --sdk gradio --hardware cpu-basic
    SPACE_CREATE=$?
    
    if [ $SPACE_CREATE -ne 0 ]; then
        echo -e "${RED}Error: Failed to create space${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}Space created successfully${RESET}"
    # Give Hugging Face a moment to set up the space
    echo "Waiting 5 seconds for space initialization..."
    sleep 5
elif [ $SPACE_CHECK -ne 0 ]; then
    echo -e "${RED}Error: Space does not exist and --create was not specified${RESET}"
    exit 1
fi

# Create files to ignore during deployment
cat > .hfignore << EOF
# Git and version control
.git
.github
.gitignore

# Environment and configuration
venv
.venv
env
.env
config/.env

# Python cache files
__pycache__
*.pyc
*.pyo
*.pyd
.pytest_cache

# Editor and IDE files
.vscode
.idea
*.swp
*.swo

# Build and distribution
build
dist
*.egg-info

# Data directories
data/memories/*
!data/memories/.gitkeep
data/lore/*
!data/lore/.gitkeep
data/storage/*
!data/storage/.gitkeep

# Logs
logs/*
!logs/.gitkeep

# Other
.DS_Store
EOF

# Create a custom app_hf.py file for HF Space
cat > app_hf.py << EOF
#!/usr/bin/env python3
"""
Entry point for the TEC Office Hugging Face Space.
This file is automatically loaded by Hugging Face Spaces.
"""
import os
import sys
import logging
from pathlib import Path
import gradio as gr

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.HFSpace")

# Check if we're running in a Hugging Face Space
HF_SPACE = os.environ.get('SPACE_ID') is not None
if HF_SPACE:
    logger.info("Running in Hugging Face Space environment")
else:
    logger.info("Running in local environment")

# Import the Gradio app
try:
    from app import demo
    logger.info("Successfully imported Gradio app")
except ImportError as e:
    logger.error(f"Failed to import Gradio app: {e}")
    # Create a fallback demo
    demo = gr.Interface(
        fn=lambda text: f"TEC Office setup error: {str(e)}",
        inputs=gr.Textbox(label="Input"),
        outputs=gr.Textbox(label="Output"),
        title="TEC Office - Error",
        description="There was an error loading the TEC Office application."
    )

if __name__ == "__main__":
    demo.launch()
EOF

# Deploy to the space
echo -e "${BLUE}Uploading files to space...${RESET}"
python "$HF_SCRIPT" upload "$USERNAME" "$SPACENAME"
UPLOAD_STATUS=$?

if [ $UPLOAD_STATUS -ne 0 ]; then
    echo -e "${RED}Error: Failed to upload files to space${RESET}"
    exit 1
fi

# Clean up temporary files
rm -f .hfignore app_hf.py

echo -e "${GREEN}Deployment completed successfully!${RESET}"
echo -e "Visit your space at: ${BLUE}https://huggingface.co/spaces/$USERNAME/$SPACENAME${RESET}"
