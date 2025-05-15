# Data

## Purpose
The `data` folder stores all data files and resources used for TEC's AI tools, automation, and content generation.

## Subfolder Structure
- **astradigital-map.json**: Contains the map data for the Astradigital Ocean.
- **automation_runs**: Logs and outputs from automation scripts.
- **cache**: Temporary data storage for faster processing.
- **generated_content**: AI-generated content files.
- **lore**: Lore-related data files.
- **memories**: Persistent memory files for AI agents.
- **news_cache**: Cached news articles and data.
- **processed_news**: Processed news data ready for use.
- **storage**: General-purpose data storage.

## Naming Conventions
- Use snake_case for file names (e.g., `processed_news_20250515.json`).
- Include timestamps where relevant (e.g., `automation_run_20250515.log`).

## Metadata Standards
- JSON files should include a `metadata` field with details like `source`, `date`, and `tags`.

## Notes
- Regularly clean up the `cache` folder to free up space.
- Ensure sensitive data is encrypted or stored securely.
