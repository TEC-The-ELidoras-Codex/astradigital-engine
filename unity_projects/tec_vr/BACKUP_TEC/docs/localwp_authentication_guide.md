# LocalWP REST API Authentication Guide

## Authentication Issues Identified
The test connections to your LocalWP site at `needless-chimneysweep.localsite.io` are failing with authentication errors. The WordPress REST API typically requires proper authentication to access posts and other data.

## Solution: Install Basic Authentication Plugin

The simplest solution is to install the Basic Authentication plugin on your LocalWP WordPress site:

1. **Download the plugin**:
   - Go to https://github.com/WP-API/Basic-Auth
   - Click the green "Code" button and select "Download ZIP"

2. **Install on your LocalWP site**:
   - Log in to your WordPress admin panel at https://needless-chimneysweep.localsite.io/wp-admin/
   - Go to Plugins → Add New → Upload Plugin
   - Upload the ZIP file you downloaded
   - Click "Install Now" and then "Activate"

3. **Create a new admin user** (optional but recommended):
   - Go to Users → Add New
   - Create a user specifically for API access
   - Set role to Administrator
   - Note down the username and password

4. **Update your .env file**:
   ```
   LOCAL_WP_SITE_URL=https://needless-chimneysweep.localsite.io
   LOCAL_WP_USER=your_new_username
   LOCAL_WP_PASSWORD=your_new_password
   LOCAL_WP_API_PATH=/wp-json/wp/v2/
   LOCAL_WP_APP_PASS=your_new_password
   ```

5. **Test the connection again**:
   ```
   python -m scripts.local_wp_debug
   ```

## Alternative Solutions

If installing the Basic Auth plugin isn't possible, try these alternatives:

### 1. Application Passwords
WordPress 5.6+ includes Application Passwords feature:
- Go to Users → Your Profile
- Scroll to "Application Passwords"
- Create a new application password
- Use this password in your .env file

### 2. Use the Site Shell
LocalWP provides direct shell access:
- In LocalWP, click on your site
- Click "Site Shell"
- Run `wp user list` to see available users
- Create a new user: `wp user create api_user api_user@example.com --role=editor --user_pass=secure_password`

### 3. JWT Authentication
Install a JWT authentication plugin for more secure API access:
- WP REST API - JWT Authentication
- Or JWT Authentication for WP REST API

## WordPress Development Environment

For serious WordPress development work, consider setting up a more developer-friendly environment:
- Use DevKinsta, LocalWP, or Docker-based setups
- Enable debugging with `WP_DEBUG` and `WP_DEBUG_LOG`
- Consider tools like WP-CLI for easier WordPress management

## Next Steps

Once authentication is working:
1. Update the TEC agent configuration
2. Test with basic post creation/fetching
3. Set up workflows with the local environment

Remember to always use the `--use-local-wp` flag with TEC workflows when you want to use the local environment instead of production.
