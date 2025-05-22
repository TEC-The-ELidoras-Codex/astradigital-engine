# Airth News Automation System Guide

This guide explains how to set up and configure the Airth News Automation system for scheduled operation. The system automatically fetches news articles, processes them into topics, generates SEO-optimized content, and publishes to WordPress on a regular schedule.

## Features

- **News Aggregation**: Fetches news from multiple configured sources
- **Topic Clustering**: Groups similar articles into coherent topics
- **Content Generation**: Creates SEO-optimized articles with a consistent structure
- **WordPress Publishing**: Posts generated content to WordPress with proper categories and tags
- **Duplicate Detection**: Prevents duplicate articles from being published

## Prerequisites

- Python 3.8 or higher
- Required Python packages (run `pip install -r requirements.txt`)
- Additional packages: `feedparser`, `scikit-learn`, `nltk`, `bs4`
- NLTK resources (run `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon'); nltk.download('punkt_tab')"`)
- WordPress site (optional, for publishing)

## Configuration

The system uses several configuration files in the `config` directory:

1. **news_sources.json**: Defines all news sources to gather articles from.
2. **news_processor.json**: Controls topic clustering parameters.
3. **content_generator.json**: Defines article generation settings, templates, and SEO patterns.

### WordPress Setup

To enable WordPress publishing:

1. Create a `.env` file in the `config` directory with the following content:

```
WP_URL=https://yourblog.com
WP_USERNAME=your_username
WP_PASSWORD=your_password_or_app_password
```

2. Make sure the WordPress REST API is enabled on your site.
3. For enhanced security, use an application password instead of your actual WordPress login password.

## Running Manually

You can run the automation system manually with various command-line options:

```
python scripts/airth_news_automation.py [options]
```

Available options:
- `--max-age DAYS`: Maximum age of news articles to fetch (default: 2)
- `--max-topics N`: Maximum number of topics to generate content for (default: 5)
- `--publish`: Enable WordPress publishing (default: disabled)
- `--status STATUS`: Publishing status - 'draft', 'publish', etc. (default: 'draft')
- `--config PATH`: Path to configuration directory (default: './config')

Example:
```
python scripts/airth_news_automation.py --max-age 3 --max-topics 2 --publish --status draft
```

## Scheduling

### Windows (Task Scheduler)

1. Open Task Scheduler (search for it in the Start menu)
2. Click "Create Basic Task"
3. Name it "Airth News Automation" and add a description
4. Set the trigger (e.g., daily at a specific time)
5. Select "Start a program" for the action
6. For the program/script, enter: `python` 
7. For arguments, enter: `C:\path\to\astradigital-engine\scripts\airth_news_automation.py --max-age 2 --max-topics 5 --publish --status draft`
8. For "Start in", enter: `C:\path\to\astradigital-engine`
9. Complete the wizard and check "Open the Properties dialog"
10. On the Properties dialog, go to "Settings" and check "Run task as soon as possible after a scheduled start is missed"

### Linux/macOS (Cron)

1. Open a terminal
2. Edit your crontab with `crontab -e`
3. Add a line like this to run daily at 9 AM:

```
0 9 * * * cd /path/to/astradigital-engine && /usr/bin/python scripts/airth_news_automation.py --max-age 2 --max-topics 5 --publish --status draft >> /path/to/astradigital-engine/logs/cron_automation.log 2>&1
```

4. Save and exit

## Output and Logging

- Logs are stored in the `logs` directory with daily filenames
- Generated topics are saved to `data/processed_news`
- Generated articles are saved to `data/generated_content`
- Run statistics are saved to `data/automation_runs`

## Troubleshooting

### Common Issues

1. **API Rate Limiting**: If you encounter rate limiting from news sources, try increasing the delay between requests or reducing the frequency of scheduled runs.

2. **WordPress Authentication Failures**: Verify your WordPress credentials and ensure the REST API is enabled on your site.

3. **Missing NLTK Resources**: If you see errors about missing NLTK resources, run:
   ```
   python -c "import nltk; nltk.download('all')"
   ```

4. **Empty Topic Results**: This might happen if the news sources aren't returning valid data. Check your internet connection and the news source configurations.

### Error Notifications

To receive notifications on errors, you can modify the Task Scheduler or cron setup to send emails on failure, or implement a monitoring system that checks the log files for error entries.

## Advanced Usage

### Custom News Sources

Edit `config/news_sources.json` to add your own news sources. Each source can be one of these types:
- RSS Feed
- REST API
- Web Scraping

## Duplicate Article Detection

The system includes a built-in duplicate detection feature that prevents posting redundant content to WordPress. This helps maintain content quality and prevents clutter in your blog.

### How Duplicate Detection Works

1. Before publishing each generated article, the system queries WordPress for existing posts
2. The new article's title is compared against existing post titles using string similarity algorithms
3. If a match exceeding the similarity threshold (default: 70%) is found, the article is skipped
4. Skipped duplicates are counted separately and reported in logs and summaries

### Testing the Duplicate Detection

You can test this feature with the included test script:

```powershell
.\run_duplicate_test.ps1
```

This will show you the similarity scores between a test title and existing WordPress posts.

### Adjusting Sensitivity

You can fine-tune how aggressively the system detects duplicates by adjusting the similarity threshold:

- Higher threshold (e.g., 0.8): Only very similar titles will be considered duplicates
- Lower threshold (e.g., 0.6): More aggressive duplicate detection, may catch more variations

The threshold is set in `scripts/airth_news_automation.py` in the `check_for_duplicate_article` method call.

For more details about duplicate detection, see the [full documentation](duplicate_detection.md).

### Content Templates

Customize the article templates in `config/content_generator.json` to match your website's style and SEO strategy.

### Integration with Other Systems

The automation system can be integrated with other tools or workflows by modifying the scripts or using the output files as input for other processes.
