# WordPress Category Setup Guide for TEC

This document provides instructions for setting up WordPress categories for the Airth News Automation system.

## Automatic Setup Method

We've created a script that automatically sets up all required WordPress categories:

```powershell
python .\scripts\setup_wp_categories.py
```

This will create the following categories in your WordPress site:

- technology_ai (AI Technology)
- technology_news (Technology News)  
- technology_analysis (Technology Analysis)
- technology_trends (Technology Trends)
- technology_business (Technology Business)
- technology_research (Technology Research)
- creative_explorations (Creative Explorations)

The script will display a success message when all categories are created successfully.

## Manual Setup Method

If you prefer to create the categories manually:

1. Log in to your WordPress admin dashboard
2. Go to Posts → Categories
3. For each of the categories listed above:
   - Click "Add New Category"
   - Enter the user-friendly name (e.g., "AI Technology")
   - Enter the exact slug as shown above (e.g., "technology_ai")
   - Click "Add New Category"
4. Verify that all categories have been created

## Troubleshooting

If you encounter any issues:

- Make sure the WordPress REST API is enabled
- Verify that your application password has appropriate permissions
- Check the logs at `logs/wp_category_setup.log` for detailed error messages
- Test your WordPress connection using:
  ```powershell
  python .\scripts\check_app_password.py
  ```

## Next Steps

After creating the categories, run the Airth News Automation script:

```powershell
python .\scripts\airth_news_automation.py --max-age 2 --max-topics 3 --status draft
```

If successful, you should see articles published to WordPress in the specified categories.
