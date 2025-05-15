# WordPress Setup for Airth News Automation - UPDATED

This document provides an updated guide for setting up WordPress integration for the Airth News Automation system.

## Configuration Steps

### 1. Setup WordPress Categories

The Airth News Automation system requires specific WordPress categories to function correctly:

```powershell
# Run this script to create all required categories automatically
python scripts\setup_wp_categories.py
```

This will create the following categories:
- **technology_ai** - AI Technology content
- **technology_news** - General tech news
- **technology_analysis** - Analysis and deep-dives
- **technology_trends** - Emerging trends in technology
- **technology_business** - Business and startup news
- **technology_research** - Research findings and studies
- **creative_explorations** - Creative and artistic AI content

### 2. Generate WordPress Application Password

1. Log into WordPress admin
2. Go to Users → Your Profile
3. Scroll down to Application Passwords section
4. Enter "Airth News Automation" as the name
5. Click "Add New Application Password"
6. Copy the generated password

### 3. Update WordPress Configuration

```powershell
# Update the WordPress password
.\scripts\update_wp_password.ps1 -AppPassword "YOUR-APP-PASSWORD-HERE"
```

### 4. Test WordPress Connection

```powershell
# Test the WordPress connection
python scripts\check_app_password.py
```

### 5. Run the Automation

```powershell
# Run the automation with default settings (draft mode)
python scripts\airth_news_automation.py --max-age 2 --max-topics 3

# Or run in publish mode to make posts public
python scripts\airth_news_automation.py --max-age 2 --max-topics 3 --status publish
```

### 6. Create a Scheduled Task (Optional)

```powershell
# Create a scheduled task to run daily at 8:00 AM
.\scripts\create_news_automation_task.ps1 -MaxAge 2 -MaxTopics 3 -TimeTrigger "8:00" -Status "draft"
```

## Troubleshooting

If you encounter any issues with categories:

1. Run the category setup script again:
   ```powershell
   python scripts\setup_wp_categories.py
   ```

2. Check existing posts and their categories:
   ```powershell
   python scripts\list_wp_posts.py --count 10 --status draft
   ```

3. Update categories for existing posts:
   ```powershell
   python scripts\update_news_categories.py
   ```

## Advanced Configuration

To customize news sources, category mappings, or content generation parameters, edit the configuration files in the `config` directory:

- `news_sources.json` - News sources and API endpoints
- `news_processor.json` - Topic clustering settings
- `content_generator.json` - Article generation parameters
