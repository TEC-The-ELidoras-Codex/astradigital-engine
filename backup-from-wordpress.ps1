# Backup WordPress Theme to TEC_CODE
# This script copies changes from your WordPress theme to your development directory

Write-Output "Backing up WordPress theme to TEC_CODE..."

$wpThemeDir = "C:\Users\Ghedd\Local Sites\teclocal\app\public\wp-content\themes\astradigital-engine"
$tecCodeDir = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme-backup"

# Create backup directory if it doesn't exist
if (-not (Test-Path $tecCodeDir)) {
    New-Item -Path $tecCodeDir -ItemType Directory -Force
    Write-Output "Created backup directory"
}

# Copy WordPress theme files to backup
Copy-Item -Path "$wpThemeDir\*" -Destination $tecCodeDir -Recurse -Force
Write-Output "Copied WordPress theme files to: $tecCodeDir"

Write-Output "Backup complete!"
Write-Output "------------------------------------------------"
Write-Output "Your WordPress theme has been backed up to: $tecCodeDir"
Write-Output "You can now safely merge any changes into your main development directory:"
Write-Output "C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme"
Write-Output "------------------------------------------------"
