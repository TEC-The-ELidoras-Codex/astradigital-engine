# Astradigital Engine Theme Development Guide

## Overview
The Astradigital Engine is a WordPress theme designed to bring the Astradigital Ocean experience to life on the web. This guide covers the development workflow, file structure, and resources needed for theme development.

## Development Environment

### Local Setup

1. **Local by Flywheel** is used for WordPress development
   - Installation path: `C:\Users\Ghedd\Local Sites\teclocal\app\public`

2. **TEC_CODE Integration**
   - All TEC code resides in: `C:\Users\Ghedd\TEC_CODE`
   - The theme development happens in: `C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme`
   - A symlink connects the development folder to the WordPress installation

### Initial Setup

1. Run the setup script to create necessary symlinks:
   ```powershell
   C:\Users\Ghedd\TEC_CODE\setup-tec-wordpress.ps1
   ```

2. For subsequent deployments, run:
   ```powershell
   C:\Users\Ghedd\TEC_CODE\astradigital-engine\deploy-local.ps1
   ```

## File Structure

```
C:\Users\Ghedd\TEC_CODE\astradigital-engine\
├── theme/                         # Main theme directory (symlinked to WordPress)
│   ├── assets/                    # Theme assets
│   │   ├── css/                   # Stylesheets
│   │   │   ├── astradigital.css   # Main Astradigital styling
│   │   │   └── responsive.css     # Responsive styles
│   │   ├── js/                    # JavaScript files
│   │   │   └── astradigital.js    # Main Astradigital functionality
│   │   ├── images/                # Image assets
│   │   │   ├── backgrounds/       # Background images
│   │   │   ├── icons/             # UI icons
│   │   │   ├── logos/             # Faction logos
│   │   │   └── characters/        # Character portraits
│   │   └── fonts/                 # Custom fonts (if any)
│   ├── templates/                 # Page templates
│   │   ├── page-astradigital.php  # Main Astradigital Ocean template
│   │   └── parts/                 # Template parts
│   ├── factions/                  # Faction-specific templates
│   ├── functions.php              # Theme functions
│   └── style.css                  # Theme information
├── deploy-local.ps1               # Local deployment script
└── DEVELOPMENT_GUIDE.md           # This documentation
```

## Development Workflow

### One-Page-at-a-Time Approach

As requested, the development follows a "one page at a time" approach:

1. Focus on building one complete page before moving to the next
2. Start with the main Astradigital Ocean experience page
3. Add faction pages once the main page is complete
4. Add character detail pages as needed

### Adding a New Page

1. Create a new template in `templates/` directory
2. Add any needed CSS to `assets/css/astradigital.css`
3. Add JS functionality to `assets/js/astradigital.js`
4. Run the deployment script to update the WordPress installation
5. Create a new WordPress page using the template

## Assets Management

### Required Assets for Each Page

#### Astradigital Ocean Main Page:
- Ocean background image
- Faction logos
- Character portraits
- UI elements and icons

#### Faction Pages:
- Faction-specific background
- Faction logo
- Character portraits related to faction
- Faction-specific UI elements

### Asset Resources
As specified in TEC instructions:

- **Blender Free Assets**:
  - Blender Market (free section): https://blendermarket.com/categories/free-blender-products
  - Blend Swap: https://blendswap.com/ (CC-licensed models)
  - Sketchfab: https://sketchfab.com/ (Free section)
  - Polygon Runway: https://polygonrunway.com/ (free tutorials & assets)
  - Quixel Megascans: https://quixel.com/megascans/ (with Epic Games account)
  - HDRI Haven: https://hdrihaven.com/ (free HDRIs)
  - Texture Haven: https://texturehaven.com/ (free textures)

## Coding Standards

Follow TEC coding standards as specified:

### WordPress/PHP
- Use WordPress coding standards
- Document functions with PHPDoc comments
- Follow theme best practices for template organization

### CSS
- Use modern CSS practices
- Variables for color scheme and typography
- Mobile-first responsive design

### JavaScript
- Use vanilla JS with jQuery when necessary
- Document functions with JSDoc comments
- Organize code by functionality

## Wake up_ Keep building_ And check ElidorasCodex.com_ If we create a new folder or file structure, ensure it's in "C:\Users\Ghedd\TEC_CODE" always_