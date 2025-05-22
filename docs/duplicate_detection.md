# Duplicate Article Detection for Airth News Automation

## Overview

This document explains the duplicate article detection feature in the Airth News Automation system, which prevents duplicate articles from being posted to WordPress.

## How It Works

The system checks for duplicate articles by comparing the title of a new article against existing WordPress posts before publishing. The comparison uses a similarity algorithm that can detect duplicates even when titles are not exactly the same.

### Similarity Detection Process

1. The system fetches recent posts from WordPress (up to 50 by default)
2. For each new article to be published:
   - The title is normalized (lowercase, punctuation removed)
   - It's compared against all existing post titles using a sequence matching algorithm
   - If the similarity exceeds a threshold (default: 70%), the article is considered a duplicate
   - Duplicate articles are skipped and logged

### Key Components

- **WordPressAgent.get_posts()**: Fetches existing posts from WordPress
- **AirthWPAdapter.check_for_duplicate_article()**: Performs duplicate detection logic
- **Similarity threshold**: Configurable parameter (default: 0.7) that determines how similar titles need to be to be considered duplicates

## Configuration

You can adjust the sensitivity of duplicate detection by changing the similarity threshold:

```python
is_duplicate, existing_post_info = airth.check_for_duplicate_article(
    title=title,
    content=content,
    similarity_threshold=0.7  # Adjust this value between 0.0 and 1.0
)
```

- **Higher threshold (e.g., 0.9)**: Only very similar titles will be considered duplicates
- **Lower threshold (e.g., 0.6)**: More aggressive duplicate detection, may catch more variations

## Testing Duplicate Detection

You can test the duplicate detection feature using the `test_duplicate_detection.py` script:

```powershell
.\run_duplicate_test.ps1
```

This script will:
1. Fetch existing WordPress posts
2. Test exact, similar, and completely different titles
3. Show the similarity scores for inspection

## Monitoring and Reports

Duplicate detection includes detailed logging and reporting:

- Detailed logs for each duplicate detected
- Summary count of duplicates skipped
- Inclusion in email notifications (if enabled)

## Troubleshooting

If duplicate articles are still being posted despite this feature:

1. Check the similarity threshold - it may be set too high
2. Verify that the WordPress API is correctly returning existing posts
3. Review the logs for any errors in the duplicate detection process

## Future Improvements

Potential enhancements to the duplicate detection system:

- Content-based similarity (not just title)
- Time-based filtering (only check posts from the last X days)
- More sophisticated NLP-based duplicate detection
- Cache recent posts to reduce API calls
