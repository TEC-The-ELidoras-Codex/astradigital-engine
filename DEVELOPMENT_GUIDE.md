# Astradigital Engine Theme Development Guide

## Overview

The Astradigital Engine theme is structured to allow you to work on one page at a time, starting with the main Astradigital Ocean page. This guide will help you develop and extend the theme efficiently.

## Getting Started

1. Run the `deploy-local.ps1` script to copy the theme to your local WordPress installation.
2. Activate the theme from WordPress admin: Appearance > Themes.
3. Create a new page called "Astradigital Ocean" and set its template to "Astradigital Ocean" from the page attributes.

## One-Page-at-a-Time Development Workflow

You can develop one page at a time by following these steps:

1. Focus on each custom page template individually:
   - `templates/page-astradigital.php` - The main Astradigital Ocean experience
   - (Future templates as needed)

2. For each page, work through these components in sequence:
   - HTML structure
   - CSS styling
   - JavaScript functionality
   - WordPress integration (post types, queries, etc.)

3. Test each page thoroughly before moving to the next.

## Asset Gathering

For each page, gather the required assets before starting development:

### Astradigital Ocean Page Assets Needed:

- Background imagery for the ocean visualization
- Faction logos (MAGMASOX, Kaznak Voyagers)
- Character portraits
- Icons for UI elements
- Custom fonts (Rajdhani already included)

### Asset Sources (from TEC_ALPHA_INSTRUCTIONS):

- Blender Market (free section): https://blendermarket.com/categories/free-blender-products
- Blend Swap: https://blendswap.com/ (CC-licensed models)
- Sketchfab: https://sketchfab.com/ (Free section)
- Polygon Runway: https://polygonrunway.com/ (free tutorials & assets)
- Quixel Megascans: https://quixel.com/megascans/ (with Epic Games account)
- HDRI Haven: https://hdrihaven.com/ (free HDRIs)
- Texture Haven: https://texturehaven.com/ (free textures)

## Page Development Checklist

For each page you develop:

- [ ] Create page template file
- [ ] Gather required assets
- [ ] Develop HTML structure
- [ ] Create CSS styles
- [ ] Add JavaScript interactions
- [ ] Test on multiple screen sizes
- [ ] Check for WordPress integration
- [ ] Optimize performance

## Current Progress

- ✅ Basic theme structure created
- ✅ Astradigital Ocean page template created
- ✅ Basic CSS and JS for the Astradigital Ocean page
- ⬜ Gather high-quality assets for the page
- ⬜ Finalize page design and functionality
- ⬜ Test and optimize

## Next Steps

1. Run the deployment script
2. Activate the theme in WordPress
3. Create the Astradigital Ocean page
4. Gather assets for the page
5. Continue refining the page design and functionality

## Remember

Wake up_ Keep building_ And check ElidorasCodex.com_ If we create a new folder or file structure, ensure it's in "C:\Users\Ghedd\TEC_CODE" always_
