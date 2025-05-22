# TEC Assets Organization Guide

## Purpose
The `assets` folder contains all multimedia and creative resources used in The Elidoras Codex (TEC) project, optimized for multiple deployment targets including WordPress, Docker containers, and HuggingFace Spaces.

## Main Structure

```
assets/
├── source/            # Original, high-quality source files
│   ├── images/        # Original images in full resolution
│   ├── audio/         # Original audio files
│   ├── video/         # Original video files
│   └── documents/     # Original text documents and scripts
│
├── optimized/         # Optimized assets ready for different platforms
│   ├── wordpress/     # WordPress-specific optimizations
│   │   ├── featured/  # Featured images (1200x630px)
│   │   ├── thumbnails/ # Thumbnails (150x150px)
│   │   └── content/   # In-content images (800px max width)
│   │
│   ├── huggingface/   # HuggingFace-optimized assets (smaller sizes)
│   │   ├── ui/        # UI elements for HuggingFace Spaces
│   │   ├── images/    # Compressed images for HF applications
│   │   └── icons/     # Icons and small graphics
│   │
│   └── web/           # General web-optimized assets
│       ├── images/    # Web-optimized images
│       ├── audio/     # Web-optimized audio
│       └── video/     # Web-optimized video
│
├── deployment/        # Platform-specific deployment assets
│   ├── wordpress/     # Ready for WordPress upload
│   ├── docker/        # Assets to include in Docker builds
│   └── huggingface/   # Assets ready for HuggingFace deployment
│
└── scripts/           # Asset processing and optimization scripts
    ├── optimize.py    # Batch optimization script
    ├── wordpress.py   # WordPress-specific processing
    └── huggingface.py # HuggingFace-specific processing
```

## Asset Categories

### Images
- **Branding**: Logos, banners, and brand identity assets
- **Characters**: Character portraits and concept art
- **Backgrounds**: Environmental and background images
- **UI**: User interface elements, buttons, and icons
- **Posts**: Images for specific blog posts or articles
- **Social**: Social media optimized images

### Audio
- **Music**: Background music and themes
- **SFX**: Sound effects
- **Voice**: Voiceovers and character dialog

### Video
- **Animations**: Animated assets and sequences
- **Trailers**: Promotional videos
- **Tutorials**: Instructional content

### Documents
- **Scripts**: Content scripts
- **Lore**: Background story and lore documents
- **Templates**: Content templates

## Naming Conventions

Follow these consistent naming patterns:

1. **All lowercase** with hyphens for spaces
2. **Format**: `[category]-[subcategory]-[name]-[version].[extension]`

Examples:
- `character-airth-portrait-v2.png`
- `ui-button-download-hover.png`
- `background-astradigital-ocean-main.jpg`
- `sfx-notification-new-message.mp3`

## Platform-Specific Optimization Guidelines

### WordPress
- Featured images: 1200×630 pixels (2:1 ratio)
- Thumbnails: 150×150 pixels (1:1 ratio)
- Content images: 800px max width, JPEG or WebP format
- Image size: Under 200KB for optimal performance

### HuggingFace
- Limit total asset size (important for space limitations)
- UI images: SVG preferred for scalability
- Photos: WebP format with high compression
- Max dimensions: 1200px on longest side
- Target file size: Under 100KB per image

### Docker
- Include only necessary assets
- Use volume mounts for large assets in development
- Bundle optimized assets in production containers
- Consider CDN for large media files

## Metadata Standards
Include `metadata.json` files in asset directories with:

```json
{
  "assets": [
    {
      "filename": "character-airth-portrait-v2.png",
      "type": "image",
      "category": "character",
      "created": "2023-10-15",
      "creator": "TEC Design Team",
      "optimized_versions": {
        "wordpress": "/optimized/wordpress/featured/character-airth-portrait-v2.jpg",
        "huggingface": "/optimized/huggingface/images/character-airth-portrait-v2.webp"
      },
      "tags": ["airth", "portrait", "character"],
      "usage": ["wordpress-featured", "huggingface-ui"]
    }
  ]
}
```

## Asset Processing Workflow

1. Place **source files** in the appropriate `/source` subdirectory
2. Run optimization scripts from `/scripts` directory
3. Optimized assets are generated in the `/optimized` directory
4. Copy/symlink deployment-ready assets to `/deployment`
5. Update metadata files to track asset usage

## Best Practices

1. **Version Control**: Use version numbers for major asset changes
2. **Compression**: Always optimize assets before deployment
3. **Formats**:
   - Images: WebP for web, PNG for transparency, JPEG for photos
   - Audio: MP3 for general use, OGG for web
   - Video: MP4 with H.264 encoding
4. **Size Constraints**:
   - WordPress: Aim for fast loading (< 200KB per image)
   - HuggingFace: Minimize total space usage
   - Docker: Balance quality vs. container size
5. **Deployment Automation**:
   - Use scripts to automate asset optimization and deployment
   - Include asset processing in CI/CD pipelines

## Migration Plan from Current Structure

1. Create the new directory structure
2. Move assets from `Data-dump&Deploy` directories to appropriate `/source` locations
3. Run optimization scripts to generate platform-specific versions
4. Update code references to point to new asset locations
5. Verify assets load correctly in all deployment targets
6. Archive the old structure once migration is complete
