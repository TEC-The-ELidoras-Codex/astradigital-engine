# TEC WordPress Environment Configuration Guide

## Overview
The Elidoras Codex AI system supports multiple WordPress environments:
- **Production**: The live ElidorasCodex.com website
- **Local**: Development environment running on LocalWP (http://localhost:10004)

This guide explains how to configure both environments and test connectivity.

## Current Status
✅ **Production WordPress**: Successfully connecting & creating posts  
✅ **Local WordPress**: Successfully connecting (MachineGoddess user)

## Environment Configuration

### Production WordPress
The production WordPress environment connects to ElidorasCodex.com using the following credentials:

```dotenv
# WordPress Configuration (Production)
WP_SITE_URL=https://elidorascodex.com
WP_URL=https://elidorascodex.com  # For backward compatibility
WP_USER=Elidorascodex
WP_APP_PASS=a8h3 ER5O BvkT NaRr XIXv gxYJ
WP_API_PATH=/wp-json/wp/v2/
```

These credentials are already configured in the `.env` file.

### Local WordPress (LocalWP)
The current local WordPress setup uses a standard LocalWP installation:

```dotenv
# Local WordPress Development Site (LocalWP)
LOCAL_WP_SITE_URL=http://localhost:10004
LOCAL_WP_USER=MachineGoddess
LOCAL_WP_PASSWORD=Xe!2E(ST8^uM(1HXh4!^LgeE
LOCAL_WP_API_PATH=/wp-json/wp/v2/
LOCAL_WP_APP_PASS=j1xW zlI6 R8ty LnpI cnMz MHfu
```

You can verify the local WordPress connection using the verification script.

## WordPress Security & Authentication

### Application Passwords vs. Regular Passwords
WordPress offers two main authentication methods:

1. **Regular user passwords**: Works, but not recommended for scripts
2. **Application passwords**: More secure and designed for API access

#### Using the Application Passwords Plugin
You already have the Application Passwords plugin installed on your localhost WordPress! This makes authentication much easier:

1. Go to `http://localhost:10004/wp-admin/profile.php`
2. Scroll to "Application Passwords" section 
3. Enter a name (e.g., "TEC Agent")
4. Click "Add New Application Password"
5. Copy the generated password (includes spaces)

Then update your `.env` file:
```
LOCAL_WP_APP_PASS=xxxx xxxx xxxx xxxx
```

### Authentication Troubleshooting
If you're experiencing authentication issues:

1. **Verify User Exists**: Check if the username exists in WordPress
2. **Try Email Instead**: Some WordPress configurations use email as username
3. **SSL Certificate Issues**: Accept any SSL warnings in your browser first
4. **API Access**: Ensure the REST API is enabled and not blocked by plugins
5. **Basic Auth**: Install the [Basic Authentication](https://github.com/WP-API/Basic-Auth) plugin for local development

## Running Tests

Test your WordPress connections with these scripts:

```bash
# Quick connectivity test for both environments
python -m scripts.wp_quick_test

# Detailed debug information
python -m scripts.local_wp_debug --verbose

# Test post creation (creates draft posts)
python -m scripts.wordpress_environment_demo --production

# Test only local environment
python -m scripts.wordpress_environment_demo --local
```

## Workflows with WordPress Environment Selection

To use the local WordPress environment in workflows:

```bash
# Run a workflow using local WordPress
python -m scripts.tec_scheduler --run-now content_creation --use-local-wp
```

For the TEC orchestrator:

```python
# Example in Python code
result = orchestrator.execute_workflow("content_creation", workflow_data, use_local_wp=True)
```

## Common Issues and Solutions

### Unknown Username Error
If you get `{"code":"invalid_username","message":"Unknown username"}`:
- Double-check username capitalization
- Try using the email address associated with the account
- Create a new user specifically for API access

### Connection Timeouts
If connections to LocalWP time out:
- Make sure the site is running
- Check your hosts file
- Verify the SSL certificate
- Try accessing the site in a browser first

### REST API Not Available
If the REST API isn't working:
- Check if the site has the REST API enabled
- Look for security plugins that might block API access
- Install the Basic Authentication plugin for local development
