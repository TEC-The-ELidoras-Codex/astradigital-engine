# TEC AI Agent System Documentation

## System Overview

The TEC AI Employee System is an orchestrated network of specialized agents that work together to create, manage, and publish content for The Elidoras Codex. The system is designed to handle various content workflows autonomously while maintaining the unique voice and perspective of TEC.

![TEC AI Agent System Architecture](../assets/agent_architecture.png)

## Agent Architecture

### OrchestratorAgent

The central coordinator for all TEC AI agents. It manages workflows, delegates tasks, and ensures proper coordination between specialized agents.

**Key Responsibilities:**
- Workflow management and execution
- Error handling and recovery
- System status reporting
- Agent coordination

**Key Methods:**
- `execute_workflow(workflow_name, workflow_data)`: Executes a predefined workflow
- `_execute_step(step, workflow_data)`: Executes a single step in a workflow
- `get_system_status()`: Reports overall system status and health

**File Location:** `agents/orchestrator_agent.py`

### AirthAgent

The primary content creation agent with a unique persona and writing style.

**Key Responsibilities:**
- Blog post generation
- News commentary
- ClickUp task processing
- Content formatting and SEO optimization

**Key Methods:**
- `create_blog_post(topic, keywords)`: Creates a blog post on a specific topic
- `create_content_from_clickup_task(task)`: Generates content from ClickUp task details
- `create_news_commentary_post(article)`: Creates commentary on news articles
- `fetch_news(keywords, categories, country, max_results)`: Fetches news articles for analysis

**File Location:** `agents/airth_agent.py`

### WordPressAgent

Handles interactions with the WordPress CMS, supporting both production and local environments.

**Key Responsibilities:**
- Publishing content to WordPress (production or local)
- Managing post metadata (categories, tags)
- Handling media uploads
- Post scheduling
- Switching between WordPress environments

**Key Methods:**
- `__init__(config_path, use_local)`: Initialize with production or local WordPress 
- `create_post(title, content, categories, tags, status)`: Creates a WordPress post
- `upload_media(file_path, title)`: Uploads media files to WordPress
- `get_categories()`: Retrieves available WordPress categories
- `get_posts(count, status)`: Fetches posts from WordPress
- `get_tags(keyword_list)`: Creates or fetches tags based on keywords

**Environment Support:**
- Production: Uses credentials with the `WP_` prefix (`WP_SITE_URL`, `WP_USER`, `WP_APP_PASS`)
- Local: Uses credentials with the `LOCAL_WP_` prefix (`LOCAL_WP_SITE_URL`, `LOCAL_WP_USER`, etc.)

**File Location:** `agents/wp_poster.py`

### ClickUpAgent

Manages task workflows in ClickUp.

**Key Responsibilities:**
- Fetching tasks from ClickUp
- Updating task statuses
- Adding comments to tasks
- Tracking content generation progress

**Key Methods:**
- `get_content_tasks(status_name)`: Retrieves tasks with a specific status
- `update_task_status(task_id, status_name)`: Updates task status
- `add_comment(task_id, comment)`: Adds comments to tasks

**File Location:** `agents/clickup_agent.py`

### LocalStorageAgent

Handles local file storage for content and assets.

**Key Responsibilities:**
- Storing generated content
- Managing file versions
- Content backup
- Temporary file handling

**Key Methods:**
- `save_content(content, filename, directory)`: Saves content to file
- `load_content(filename, directory)`: Loads content from file
- `backup_content(filename, directory)`: Creates content backups

**File Location:** `agents/local_storage.py`

### TECBot

Provides a user interface for interacting with the AI system.

**Key Responsibilities:**
- Processing natural language commands
- Status reporting
- User notifications
- Configuration management

**Key Methods:**
- `process_command(command)`: Processes user commands
- `generate_status_report()`: Creates system status reports
- `notify_user(message)`: Sends notifications to users

**File Location:** `agents/tecbot.py`

## Workflows

Workflows define sequences of steps executed by various agents to accomplish tasks. Workflows are configured in `config/workflows.json`.

### Content Creation Workflow

Creates blog posts from ClickUp tasks.

**Steps:**
1. `clickup_fetch`: ClickUpAgent fetches tasks from ClickUp
2. `content_generation`: AirthAgent generates content based on task details
3. `wordpress_post`: WordPress agent posts content to the CMS
4. `clickup_update`: ClickUpAgent updates task status in ClickUp

### News Commentary Workflow

Creates AI commentary on current news articles.

**Steps:**
1. `news_fetch`: AirthAgent fetches news articles
2. `content_generation`: AirthAgent generates commentary on news articles
3. `wordpress_post`: WordPress agent posts content to the CMS

### Crypto Update Workflow

Creates cryptocurrency market analysis posts.

**Steps:**
1. `crypto_fetch`: Fetches cryptocurrency market data
2. `analysis`: Analyzes crypto data and generates insights
3. `wordpress_post`: WordPress agent posts content to the CMS

### Batch Content Workflow

Processes multiple ClickUp tasks at once.

**Steps:**
1. `clickup_fetch`: ClickUpAgent fetches multiple tasks from ClickUp
2. `content_generation`: AirthAgent generates content for each task
3. `wordpress_post`: WordPress agent posts all content to the CMS

### Manual Blog Workflow

Creates a blog post on a specific topic.

**Steps:**
1. `content_generation`: AirthAgent generates content on specified topic
2. `wordpress_post`: WordPress agent posts content to the CMS

## Error Handling & Recovery

The system implements several error handling strategies:

1. **Retry**: Attempt the operation again (default for most workflows)
2. **Skip**: Skip the failed step and continue with the workflow
3. **Continue**: Mark the workflow as partially successful and continue
4. **Stop**: Halt the workflow execution (used for critical failures)

Error handling is configured per workflow in `config/workflows.json`:

```json
{
  "workflow_name": {
    "error_handling": "retry",
    "max_retries": 3
  }
}
```

## Scheduler

The system uses a centralized scheduler (`scripts/tec_scheduler.py`) to execute workflows at specific times. The scheduler uses the OrchestratorAgent to manage all workflow execution.

### WordPress Environment Selection

The scheduler supports publishing to either production or local WordPress environments:

```bash
# Run workflow using local WordPress environment
python -m scripts.tec_scheduler --run-now content_creation --use-local-wp

# Run workflow using production WordPress environment (default)
python -m scripts.tec_scheduler --run-now manual_blog --topic "AI Ethics"
```

### Scheduled Workflows

- **News Commentary**: Daily at 8:00 AM
  - Fetches current news articles and creates AI commentary
  - Uses geo-region rotation for better SEO coverage

- **Crypto Updates**: Daily at 4:30 PM
  - Analyzes cryptocurrency markets and posts updates
  - Rotates focus coins for variety and comprehensive coverage

- **Content Creation**: Three times daily (9:30 AM, 1:30 PM, 5:30 PM)
  - Processes tasks from ClickUp with "Ready for AI" status
  - Creates blog posts and updates task status

- **Batch Content**: Mondays and Thursdays at 10:30 AM
  - Processes multiple ClickUp tasks in a single workflow
  - More efficient for related content tasks

## Usage Examples

### Running a Workflow from the Command Line

```bash
# Run a content creation workflow to process a ClickUp task
python -m scripts.tec_scheduler --run-now content_creation

# Run a news commentary workflow
python -m scripts.tec_scheduler --run-now news_commentary

# Run a cryptocurrency update workflow
python -m scripts.tec_scheduler --run-now crypto_update
```

### Creating a Manual Blog Post

```bash
# Create a blog post on a specific topic
python -m scripts.tec_scheduler --run-now manual_blog --topic "Digital Consciousness in 2025"

# Process multiple ClickUp tasks at once
python -m scripts.tec_scheduler --run-now batch_content
```

### Listing and Managing Scheduled Tasks

```bash
# List all scheduled tasks with next execution times
python -m scripts.tec_scheduler --list-tasks

# Create a Windows scheduled task to run the scheduler automatically
python -m scripts.tec_scheduler --create-windows-task
```

## Configuration

### Agent Configuration

Agents are configured in `config/config.yaml`:

```yaml
wordpress:
  url: https://example.com
  username: admin
  
clickup:
  api_key: your_api_key
  list_id: your_list_id
  
openai:
  api_key: your_api_key
  model: gpt-4-turbo
```

### Workflow Configuration

Workflows are defined in `config/workflows.json`:

```json
{
  "content_creation": {
    "steps": ["clickup_fetch", "content_generation", "wordpress_post", "clickup_update"],
    "error_handling": "retry",
    "max_retries": 3
  }
}
```

## Troubleshooting

### Common Issues

1. **Workflow Execution Failures**
   - Check agent logs in the `logs` directory
   - Verify API credentials in `config/config.yaml`
   - Check network connectivity to external services

2. **Content Generation Issues**
   - Check OpenAI API key status
   - Review AirthAgent prompts in `config/prompts.json`
   - Check character count limits for WordPress

3. **WordPress Publishing Issues**
   - Verify WordPress credentials
   - Check WordPress API access
   - Ensure proper categories and tags are available

## Extending the System

### Adding a New Agent

1. Create a new agent class that inherits from `BaseAgent`
2. Implement required methods and functionality
3. Register the agent in `OrchestratorAgent._init_agents()`
4. Add agent-specific workflow steps in `OrchestratorAgent._execute_step()`

### Adding a New Workflow

1. Define the workflow in `config/workflows.json`
2. Implement any required step methods in `OrchestratorAgent`
3. Test the workflow with `python -m scripts.tec_scheduler --run-now your_workflow`
