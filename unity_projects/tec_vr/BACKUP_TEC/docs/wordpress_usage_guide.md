# WordPress Environment Utilization Guide for TEC AI System

This guide explains how to use both local and production WordPress environments with The Elidoras Codex (TEC) AI system.

## Configuration Summary

The TEC system is now configured with credentials for two WordPress environments:

1. **Production Environment**
   - Site URL: https://elidorascodex.com
   - Username: Elidorascodex
   - Authentication: Application password

2. **Local Development Environment**
   - Site URL: http://localhost:10004
   - Username: MachineGoddess
   - Authentication: Application password

## How to Use Different Environments

### Command Line Arguments

When running workflows or scripts, you can use the `--use-local-wp` flag to target the local WordPress environment:

```bash
# Run with production WordPress (default)
python -m scripts.tec_scheduler --run-now content_creation

# Run with local WordPress
python -m scripts.tec_scheduler --run-now content_creation --use-local-wp
```

### In Code

To specify the WordPress environment in your code, use the `use_local` parameter when creating a `WordPressAgent` instance:

```python
# Use production WordPress
wp_agent = WordPressAgent(use_local=False)  # or omit the parameter, as False is default

# Use local WordPress
wp_agent = WordPressAgent(use_local=True)
```

## Verifying Connections

You can verify the WordPress connections at any time using:

```bash
# Test both environments (basic connection)
python -m scripts.verify_wordpress_connections

# Test with post creation (creates draft posts in both environments)
python -m scripts.verify_wordpress_connections --post-test
```

## Post Creation Example

Here's a simple example of creating posts in both environments:

```python
from agents.wp_poster import WordPressAgent

def create_test_posts():
    # Create post in production
    prod_agent = WordPressAgent(use_local=False)
    prod_result = prod_agent.create_post(
        title="Test Post on Production",
        content="<p>This is a test post on the production site.</p>",
        status="draft"
    )
    print(f"Production post created: {prod_result.get('post_url')}")
    
    # Create post in local environment
    local_agent = WordPressAgent(use_local=True)
    local_result = local_agent.create_post(
        title="Test Post on Local",
        content="<p>This is a test post on the local site.</p>",
        status="draft"
    )
    print(f"Local post created: {local_result.get('post_url')}")

if __name__ == "__main__":
    create_test_posts()
```

## Authentication Details

Both environments use application passwords, which are formatted with spaces in the `.env` file:

```
WP_APP_PASS=a8h3 ER5O BvkT NaRr XIXv gxYJ
LOCAL_WP_APP_PASS=j1xW zlI6 R8ty LnpI cnMz MHfu
```

The WordPress agent is designed to try multiple authentication methods, including both spaced and non-spaced variants of the application password.

## Best Practices

1. **Test in Local First**: Develop and test new content workflows in your local environment before publishing to production.

2. **Draft Mode**: When testing new agent features, always set `status="draft"` to prevent accidental publication.

3. **Monitor Logs**: Check the logs in `logs/` directory to troubleshoot any WordPress connectivity issues.

4. **Connection Verification**: Run the verification script before starting important workflows to ensure proper connectivity.

## Troubleshooting

If you encounter issues with WordPress connections:

1. **Check LocalWP**: Ensure your local WordPress installation is running (typically at http://localhost:10004)

2. **Verify Credentials**: Confirm the credentials in `.env` file are correct and up to date

3. **Application Password Format**: Ensure application passwords are properly formatted with spaces

4. **Run Debug Scripts**: Use `scripts/local_wp_debug.py` for detailed diagnostics of local WordPress connections

5. **Check Network**: Ensure there are no network connectivity issues between your system and the WordPress sites
