# Deploy Astradigital Engine Theme to Local WordPress
# Copies the theme files to the local WordPress themes directory

# Configuration
$sourceDir = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme"
$destinationDir = "C:\Users\Ghedd\Local Sites\teclocal\app\public\wp-content\themes\astradigital-engine"

# Ensure the destination directory exists
Write-Host "Creating destination directory if it doesn't exist..."
New-Item -Path $destinationDir -ItemType Directory -Force | Out-Null

# Copy all theme files to the destination
Write-Host "Copying theme files to local WordPress installation..."
Copy-Item -Path "$sourceDir\*" -Destination $destinationDir -Recurse -Force

# Create a page for the Astradigital Ocean if it doesn't exist
Write-Host "Checking for Astradigital Ocean page..."
$wpCliPath = "C:\Users\Ghedd\Local Sites\teclocal\app\public\wp-cli.phar"

# This is just informational - the actual page creation would require WP-CLI
Write-Host "To create the Astradigital Ocean page, run this command in your WordPress directory:"
Write-Host "php wp-cli.phar post create --post_type=page --post_title='Astradigital Ocean' --post_status=publish --page_template='templates/page-astradigital.php'"

Write-Host "`nDeployment complete! The Astradigital Engine theme is now available in your local WordPress installation."
Write-Host "You can activate it from the WordPress admin panel: Appearance > Themes"
Write-Host "Remember to set up the Astradigital Ocean page with the page-astradigital.php template."

# Show link to open the local site
Write-Host "`nLocal site URL: http://teclocal.local/"
