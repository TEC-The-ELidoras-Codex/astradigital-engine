# WordPress Setup for Airth News Automation

This guide explains how to set up WordPress integration for the Airth News Automation system.

## Prerequisites

- WordPress site with admin access
- REST API enabled
- Ability to create application passwords or use admin credentials

## Configuration Steps

### 1. Enable the REST API

Make sure the WordPress REST API is enabled. It's enabled by default in WordPress 4.7 and later. If you're using an older version or have disabled it, you'll need to re-enable it.

### 2. Create an Application Password

For security, it's recommended to use application passwords instead of your main WordPress login:

1. Log in to your WordPress admin dashboard
2. Go to Users → Your Profile
3. Scroll down to the "Application Passwords" section
4. Enter a name like "Airth News Automation"
5. Click "Add New Application Password"
6. Copy the generated password

### 3. Configure Environment Variables

Create a `.env` file in the `config` directory with the following content:

```
# WordPress API Authentication
WP_URL=https://your-wordpress-site.com
WP_USERNAME=your_wp_username
WP_PASSWORD=your_app_password_from_step_2
```

### 4. Test the Connection

Run the WordPress connection test script:

```
python scripts/test_wordpress_connection.py
```

If successful, you should see confirmation that a test post was created (as a draft).

## WordPress Categories

For optimal organization, create the following categories in your WordPress site:

1. technology_ai
2. technology_news
3. technology_analysis
4. technology_trends
5. technology_business
6. technology_research
7. creative_explorations

## Troubleshooting

### Common Issues

1. **Authentication Failed**: Make sure your username and password/application password are correct.

2. **API Not Available**: Ensure the WordPress REST API is enabled and accessible.

3. **Permission Errors**: The user account needs appropriate permissions to create posts.

### Testing REST API Access

You can test if the REST API is accessible by visiting:
```
https://your-wordpress-site.com/wp-json/
```

### Checking for Proper Authorization

Test if your credentials work with:
```
curl -X GET 'https://your-wordpress-site.com/wp-json/wp/v2/posts' --user 'your_username:your_password'
```

## Advanced Configuration

For advanced configurations like custom post types, custom fields, or different publishing workflows, see the WordPress REST API documentation at:
https://developer.wordpress.org/rest-api/
