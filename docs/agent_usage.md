# TEC AI Agents Documentation

This document provides a comprehensive guide to using the AI agents in the TEC_OFFICE_REPO.

## Table of Contents

1. [Introduction](#introduction)
2. [Setting Up](#setting-up)
3. [Agent Overview](#agent-overview)
4. [Airth: The Oracle](#airth-the-oracle)
5. [Budlee: The Automation Agent](#budlee-the-automation-agent)
6. [Sassafras: The Creative Agent](#sassafras-the-creative-agent)
7. [WordPress Integration](#wordpress-integration)
8. [GitHub Integration](#github-integration)
9. [Hugging Face Integration](#hugging-face-integration)
10. [Advanced Configuration](#advanced-configuration)
11. [Troubleshooting](#troubleshooting)

## Introduction

The TEC_OFFICE_REPO hosts a collection of AI agents designed to enhance productivity and creativity in various aspects of your digital workflow. These agents integrate with WordPress, GitHub, and Hugging Face to provide a comprehensive suite of tools for content creation, automation, and more.

## Setting Up

### Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)
- WordPress site with XML-RPC enabled (for WordPress integration)
- GitHub account (for GitHub integration)
- Hugging Face account (for Hugging Face integration)
- OpenAI API key or other supported AI service

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/TEC_OFFICE_REPO.git
   cd TEC_OFFICE_REPO
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment variable template:
   ```bash
   cp config/env.example config/.env
   ```

4. Edit the `.env` file with your credentials:
   ```bash
   nano config/.env
   ```

5. Run the setup script (optional):
   ```bash
   python setup.py
   ```

## Agent Overview

TEC_OFFICE_REPO includes three primary AI agents:

1. **Airth** - The Oracle: Knowledge retrieval, research, and blog writing
2. **Budlee** - The Automation Agent: Task automation and system management
3. **Sassafras** - The Creative Agent: Creative content generation and idea exploration

Each agent is designed with a specific personality and set of capabilities, making them suitable for different tasks.

## Airth: The Oracle

Airth specializes in knowledge retrieval, research, and content creation. This agent can answer questions, create blog posts, and provide insightful analysis on various topics.

### Usage Examples

#### Python API

```python
from src.agents.airth_agent import AirthAgent

# Initialize Airth
airth = AirthAgent('config')

# Get a response from Airth
response = airth.respond("Explain the concept of neural networks")
print(response)

# Create a blog post
blog_post = airth.create_blog_post(
    title="The Future of AI",
    tags=["technology", "artificial intelligence"],
    target_words=1500,
    tone="informative"
)
print(blog_post)
```

#### Command Line

```bash
# Ask Airth a question
python scripts/airth_blog_post.py --query "Explain quantum computing"

# Generate a blog post
python scripts/airth_blog_post.py --title "The Future of AI" --tags technology,ai --target-words 1500
```

#### Web Interface

Access the web interface by running:

```bash
python app.py
```

Navigate to the "Airth" tab to interact with the Oracle agent.

### Configuration Options

Airth's behavior can be customized through the following environment variables:

- `AIRTH_PERSONALITY`: Defines the tone and style of Airth's responses
- `OPENAI_MODEL`: Specifies which OpenAI model to use for Airth
- `AIRTH_MEMORY_PATH`: Path to store Airth's memory file (defaults to data/memories/airth_memories.json)

## Budlee: The Automation Agent

Budlee focuses on task automation and system management. This agent can help with scheduling, file organization, data processing, and more.

### Usage Examples

#### Python API

```python
from src.agents.budlee_agent import BudleeAgent

# Initialize Budlee
budlee = BudleeAgent('config')

# Process a task
result = budlee.process_task("Schedule a weekly backup of our database")
print(result)

# Organize files
organization_result = budlee.organize_files("/path/to/directory")
print(organization_result)
```

#### Command Line

```bash
# Ask Budlee to process a task
python src/main.py --agent budlee --task "Schedule a weekly backup of our database"
```

#### Web Interface

Access the web interface by running:

```bash
python app.py
```

Navigate to the "Budlee" tab to interact with the Automation agent.

### Configuration Options

Budlee's behavior can be customized through the following environment variables:

- `BUDLEE_PERSONALITY`: Defines the tone and style of Budlee's responses
- `BUDLEE_MEMORY_PATH`: Path to store Budlee's memory file

## Sassafras: The Creative Agent

Sassafras generates creative content and artistic outputs. This agent can help with brainstorming, storytelling, and creative writing.

### Usage Examples

#### Python API

```python
from src.agents.sassafras_agent import SassafrasAgent

# Initialize Sassafras
sassafras = SassafrasAgent('config')

# Generate creative content
creative_text = sassafras.create("A cyberpunk short story about digital consciousness")
print(creative_text)

# Brainstorm ideas
ideas = sassafras.brainstorm("New features for a music streaming app", num_ideas=5)
print(ideas)
```

#### Command Line

```bash
# Generate creative content
python src/main.py --agent sassafras --prompt "A cyberpunk short story about digital consciousness"
```

#### Web Interface

Access the web interface by running:

```bash
python app.py
```

Navigate to the "Sassafras" tab to interact with the Creative agent.

### Configuration Options

Sassafras's behavior can be customized through the following environment variables:

- `SASSAFRAS_PERSONALITY`: Defines the tone and style of Sassafras's responses
- `SASSAFRAS_MEMORY_PATH`: Path to store Sassafras's memory file
- `SASSAFRAS_CREATIVITY_LEVEL`: Controls the randomness and creativity of outputs (1-10)

## WordPress Integration

TEC_OFFICE_REPO integrates with WordPress to enable direct publishing of content from the agents.

### Configuration

Set the following environment variables in your `.env` file:

```
WP_URL=https://your-wordpress-site.com/xmlrpc.php
WP_USERNAME=your_username
WP_PASSWORD=your_application_password
```

### Usage Examples

#### Python API

```python
from src.agents.wp_poster import WordPressAgent

# Initialize the WordPress agent
wp_agent = WordPressAgent('config')

# Create a post
result = wp_agent.create_post(
    title="The Digital Frontier",
    content="<p>Exploring the future of technology...</p>",
    category="Technology",
    tags=["future", "AI", "digital"],
    status="draft"  # or "publish" to go live immediately
)
print(result)
```

#### Testing Connection

Test your WordPress connection with:

```bash
python scripts/test_wordpress_connection.py
```

## GitHub Integration

TEC_OFFICE_REPO can connect to GitHub repositories for version control and project management.

### Configuration

Set the following environment variables in your `.env` file:

```
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_github_username
GITHUB_REPO=your_github_repository
```

### Usage Examples

```bash
# Check repository status
python scripts/github_connection.py status your-repository-name

# Clone a repository
python scripts/github_connection.py clone your-username/your-repository
```

## Hugging Face Integration

TEC_OFFICE_REPO integrates with Hugging Face Spaces to deploy models and applications.

### Configuration

Set the following environment variables in your `.env` file:

```
HF_TOKEN=your_huggingface_token
HF_USERNAME=your_huggingface_username
HF_SPACE_NAME=your_space_name
```

### Usage Examples

```bash
# Check if a space exists
python scripts/huggingface_connection.py check your-username your-space-name

# Create a new space
python scripts/huggingface_connection.py create your-username your-space-name --sdk gradio

# Upload files to a space
python scripts/huggingface_connection.py upload your-username your-space-name
```

## Advanced Configuration

### Agent Memory

All agents maintain a memory system to remember past interactions. These memories are stored in JSON files in the `data/memories/` directory:

- Airth: `data/memories/airth_memories.json`
- Budlee: `data/memories/budlee_memories.json`
- Sassafras: `data/memories/sassafras_memories.json`

You can reset an agent's memory by deleting the corresponding file.

### Custom Prompts

The agents use prompts defined in `config/prompts.json` to guide their behavior. You can edit this file to customize how the agents respond.

### Docker Deployment

For containerized deployment, use:

```bash
# Build and start the containers
make docker-build
make docker-up

# Check container status
python scripts/docker_manager.py status

# Stop the containers
make docker-down
```

## Troubleshooting

### Common Issues

1. **Connection Issues with WordPress**:
   - Ensure XML-RPC is enabled on your WordPress site
   - Verify that your application password has the correct permissions

2. **API Key Issues**:
   - Check that all API keys are correctly set in your `.env` file

3. **Agent Not Responding as Expected**:
   - Try adjusting the personality settings in the `.env` file
   - Check the agent's memory file to see if past interactions are affecting its behavior

### Logging

Check the logs in the `logs/` directory for detailed information about errors and agent activity.

### Getting Help

If you encounter any issues that aren't covered in this documentation, please open an issue on the GitHub repository or contact the TEC support team.
