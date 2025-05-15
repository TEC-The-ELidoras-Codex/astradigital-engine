# TEC WordPress Local Integration Script
# This script creates the necessary folder structure and symlinks to integrate
# Local WordPress with the TEC_CODE folder structure

# Create necessary directories if they don't exist
$tecCodeDir = "C:\Users\Ghedd\TEC_CODE"
$tecWpDir = "$tecCodeDir\wordpress"
$astradigitalDir = "$tecCodeDir\astradigital-engine"
$themeTargetDir = "C:\Users\Ghedd\Local Sites\teclocal\app\public\wp-content\themes\astradigital-engine"

# Create WordPress directory in TEC_CODE if it doesn't exist
If (-not (Test-Path $tecWpDir)) {
    New-Item -Path $tecWpDir -ItemType Directory -Force
    Write-Output "Created WordPress directory in TEC_CODE"
}

# Create symlink for the theme in wp-content/themes
If (Test-Path $themeTargetDir) {
    # Remove existing directory or symlink
    Remove-Item -Path $themeTargetDir -Force -Recurse
    Write-Output "Removed existing theme directory or symlink"
}

# Create theme directory symlink
New-Item -Path $themeTargetDir -ItemType SymbolicLink -Value "$astradigitalDir\theme" -Force
Write-Output "Created symlink for astradigital-engine theme from TEC_CODE to WordPress themes directory"

# Check if we need to create placeholder images for the theme
$assetsDir = "$astradigitalDir\theme\assets\images"
$backgroundsDir = "$assetsDir\backgrounds"
$logosDir = "$assetsDir\logos"
$charactersDir = "$assetsDir\characters"

# Create placeholder images if they don't exist
If (-not (Test-Path "$backgroundsDir\astradigital-ocean.jpg")) {
    Write-Output "Creating placeholder images for the theme..."
    
    # Download placeholder images (or create color blocks as placeholders)
    Invoke-WebRequest -Uri "https://picsum.photos/1920/800" -OutFile "$backgroundsDir\astradigital-ocean.jpg"
    Invoke-WebRequest -Uri "https://picsum.photos/500/500" -OutFile "$logosDir\magmasox-logo.png"
    Invoke-WebRequest -Uri "https://picsum.photos/500/501" -OutFile "$logosDir\kaznak-logo.png"
    Invoke-WebRequest -Uri "https://picsum.photos/400/600" -OutFile "$charactersDir\character-sample.png"
    
    Write-Output "Placeholder images created"
}

Write-Output "TEC WordPress Integration Setup Complete!"
Write-Output "------------------------------------------------"
Write-Output "The astradigital-engine theme is now available in your WordPress installation."
Write-Output "You can activate it from the WordPress admin dashboard."
Write-Output "To add the Astradigital Ocean page:"
Write-Output "1. Go to WordPress admin"
Write-Output "2. Create a new page"
Write-Output "3. Set template to 'Astradigital Ocean'"
Write-Output "4. Publish the page"
Write-Output "------------------------------------------------"
