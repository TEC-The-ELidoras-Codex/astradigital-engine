# Astradigital Engine Local Copy Script
# This script copies the Astradigital Engine theme to your Local WordPress installation
# This version doesn't require administrator privileges

Write-Output "Deploying Astradigital Engine theme to Local WordPress..."

$themeDir = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme"
$targetDir = "C:\Users\Ghedd\Local Sites\teclocal\app\public\wp-content\themes\astradigital-engine"

# Remove target directory if it exists
if (Test-Path $targetDir) {
    Remove-Item -Path $targetDir -Force -Recurse
    Write-Output "Removed existing theme directory"
}

# Create target directory
New-Item -Path $targetDir -ItemType Directory -Force
Write-Output "Created theme directory"

# Copy theme files
Copy-Item -Path "$themeDir\*" -Destination $targetDir -Recurse -Force
Write-Output "Copied theme files"

# Create placeholder images if needed
$assetsDir = "$targetDir\assets\images"
$backgroundsDir = "$assetsDir\backgrounds"
$logosDir = "$assetsDir\logos"
$charactersDir = "$assetsDir\characters"

# Create directories if they don't exist
if (-not (Test-Path $backgroundsDir)) { New-Item -Path $backgroundsDir -ItemType Directory -Force }
if (-not (Test-Path $logosDir)) { New-Item -Path $logosDir -ItemType Directory -Force }
if (-not (Test-Path $charactersDir)) { New-Item -Path $charactersDir -ItemType Directory -Force }

# Download placeholder images if they don't exist
If (-not (Test-Path "$backgroundsDir\astradigital-ocean.jpg")) {
    Write-Output "Creating placeholder images for the theme..."
    
    try {
        Invoke-WebRequest -Uri "https://picsum.photos/1920/800" -OutFile "$backgroundsDir\astradigital-ocean.jpg"
        Invoke-WebRequest -Uri "https://picsum.photos/500/500" -OutFile "$logosDir\magmasox-logo.png"
        Invoke-WebRequest -Uri "https://picsum.photos/500/501" -OutFile "$logosDir\kaznak-logo.png"
        Invoke-WebRequest -Uri "https://picsum.photos/400/600" -OutFile "$charactersDir\character-sample.png"
        
        Write-Output "Placeholder images created"
    } catch {
        Write-Output "Error downloading placeholder images: $_"
    }
}

Write-Output "Deployment complete!"
Write-Output "------------------------------------------------"
Write-Output "The astradigital-engine theme is now available in your WordPress installation."
Write-Output "You can activate it from the WordPress admin dashboard."
Write-Output "To add the Astradigital Ocean page:"
Write-Output "1. Go to WordPress admin"
Write-Output "2. Create a new page"
Write-Output "3. Set template to 'Astradigital Ocean'"
Write-Output "4. Publish the page"
Write-Output "------------------------------------------------"

Write-Output "IMPORTANT: This script creates a copy of your theme."
Write-Output "Any changes made to C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme will need to be redeployed."
Write-Output "Run this script again after making changes to see them in WordPress."
Write-Output "------------------------------------------------"
