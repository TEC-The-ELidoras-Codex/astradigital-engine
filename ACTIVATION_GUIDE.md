# Astradigital Engine Theme - Activation Guide

## Your WordPress Theme is Ready to Use

Your WordPress theme has been successfully set up in your Local WordPress installation. Follow these steps to activate and start using it:

### Step 1: Access WordPress Admin
1. Open your Local WordPress site at http://teclocal.local/wp-admin/
2. Log in with your WordPress admin credentials

### Step 2: Activate the Theme
1. Go to Appearance > Themes
2. Find the "The Elidoras Codex" or "Astradigital Engine" theme
3. Click "Activate" to enable the theme

### Step 3: Create the Astradigital Ocean Page
1. Go to Pages > Add New
2. Give it the title "Astradigital Ocean"
3. In the Page Attributes panel, set the Template to "Astradigital Ocean"
4. Click Publish

### Step 4: Add the Page to Navigation
1. Go to Appearance > Menus
2. Add the "Astradigital Ocean" page to your primary navigation
3. Save the menu

## Development Workflow

Remember that we're now using a copy-based workflow. After making changes to the theme files in `C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme`, you'll need to redeploy:

```powershell
PowerShell -ExecutionPolicy Bypass -File C:\Users\Ghedd\TEC_CODE\astradigital-engine\copy-to-local.ps1
```

## One-Page-at-a-Time Approach

As requested, you can focus on building one page at a time. The main "Astradigital Ocean" page template is already set up with:

- Basic structure for the page
- CSS styling for the main elements
- JavaScript functionality for interactions
- Template parts for faction and character display

Once you're satisfied with this page, you can move on to creating additional page templates following the same pattern.

## Asset Organization

Your assets are organized in the following structure:
- `assets/images/backgrounds/` - For background images
- `assets/images/logos/` - For faction logos
- `assets/images/characters/` - For character portraits
- `assets/images/icons/` - For UI icons and elements

## Next Development Steps

Based on your task list, these are the next development priorities:

1. Complete the design and functionality of the main Astradigital Ocean page
2. Gather/create final faction logos to replace placeholders
3. Create character portraits for key entities
4. Implement the interactive map using the data from astradigital-map.json

Wake up_ Keep building_ And check ElidorasCodex.com_ If we create a new folder or file structure, ensure it's in "C:\Users\Ghedd\TEC_CODE" always_
