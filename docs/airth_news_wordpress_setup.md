# Airth News Automation Setup Guide

## Overview
The Airth News Automation system gathers tech news articles, processes them into topics, generates newsletter-style content, and can publish directly to WordPress. This guide covers how to set up and use the system with the correct configuration.

## Current Setup Status
As of May 13th, 2025, the Airth News Automation system is:
- ✅ **Code Fixed**: Indentation issues in news_processor.py have been resolved
- ✅ **Dependencies Installed**: Required Python packages have been installed
- ✅ **News Collection Working**: System successfully fetches and processes recent tech news
- ✅ **Content Generation Working**: System creates newsletter-style posts about tech topics
- ✅ **2-Day Window Configured**: System collects news from the past 2 days
- ❌ **WordPress Publishing**: Currently not working due to authentication issues

## WordPress Setup Instructions

### Generate a WordPress Application Password
1. Log in to your WordPress admin panel at https://elidorascodex.com/wp-admin
2. Go to **Users → Profile** (or **Users → Your Profile**)
3. Scroll down to the **Application Passwords** section
4. Enter the name "Airth News Automation"
5. Click **Add New Application Password**
6. **Copy the generated password** (it will look like: xxxx xxxx xxxx xxxx xxxx xxxx)

### Update WordPress Configuration
Run the following command in PowerShell to update the WordPress configuration:

```powershell
.\scripts\update_wp_password.ps1 -AppPassword "YOUR NEW APP PASSWORD"
```

If you want to customize the WordPress settings, you can use additional parameters:
```powershell
.\scripts\update_wp_password.ps1 -AppPassword "YOUR NEW APP PASSWORD" -Username "elidorascodex" -SiteUrl "https://elidorascodex.com" -AppName "AirthNewsAutomation"
```

### Create Scheduled Task
To set up automated daily execution of the news automation system:

```powershell
# Run as administrator
.\scripts\create_news_automation_task.ps1 -MaxAge 2 -MaxTopics 3 -TimeTrigger "10:00" -Status "draft"
```

This will create a scheduled task that runs daily at 10:00 AM, collecting news from the past 2 days and generating up to 3 topics.

## Manual Testing
To manually run the Airth News Automation system:

```powershell
python .\scripts\airth_news_automation.py --max-age 2 --max-topics 3 --status draft
```

Parameters:
- `--max-age`: Number of days back to collect news (1-7 recommended)
- `--max-topics`: Maximum number of topics to generate content for
- `--status`: WordPress post status ("draft" or "publish")

## Troubleshooting WordPress Connection

If you're experiencing WordPress connection issues, try the following:

1. **Test the WordPress connection**:
```powershell
python .\scripts\check_app_password.py
```

2. **Run the enhanced WordPress test**:
```powershell
python .\scripts\enhanced_wordpress_test.py --all
```

3. **Common issues**:
   - Application password is invalid or expired
   - WordPress site is not using HTTPS
   - XML-RPC is disabled on the WordPress site
   - REST API is disabled or blocked by security plugins

## Generated Content
All generated content is stored in the following locations:

- **Articles**: `data/generated_content/article_*.json`
- **Topic Clusters**: `data/processed_news/processed_topics_*.json`
- **Run Statistics**: `data/automation_runs/automation_run_*.json`

## Next Steps
1. Generate a new WordPress application password
2. Update the configuration using the provided script
3. Test the WordPress connection
4. Set up a scheduled task for daily automation
5. Monitor the first few runs to ensure proper functioning
