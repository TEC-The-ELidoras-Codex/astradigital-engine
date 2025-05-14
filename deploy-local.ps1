# Astradigital Engine Local Deployment Script
# This script updates the Astradigital Engine theme in your Local WordPress installation

Write-Output "Deploying Astradigital Engine theme to Local WordPress..."

$themeDir = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme"
$targetDir = "C:\Users\Ghedd\Local Sites\teclocal\app\public\wp-content\themes\astradigital-engine"

# Check if symlink exists
if (Test-Path $targetDir) {
    # If it's a symlink, we don't need to do anything
    if ((Get-Item $targetDir).Attributes -match "ReparsePoint") {
        Write-Output "Symlink already exists - no need to copy files"
    } else {
        # If it's a regular directory, remove it and create symlink
        Remove-Item -Path $targetDir -Force -Recurse
        New-Item -Path $targetDir -ItemType SymbolicLink -Value $themeDir -Force
        Write-Output "Created symlink for theme"
    }
} else {
    # Create symlink if target directory doesn't exist
    New-Item -Path $targetDir -ItemType SymbolicLink -Value $themeDir -Force
    Write-Output "Created symlink for theme"
}

# Create placeholder images if needed
$assetsDir = "$themeDir\assets\images"
$backgroundsDir = "$assetsDir\backgrounds"
$logosDir = "$assetsDir\logos"
$charactersDir = "$assetsDir\characters"

# Create placeholder images if they don't exist
If (-not (Test-Path "$backgroundsDir\astradigital-ocean.jpg")) {
    Write-Output "Creating placeholder images for the theme..."
    
    # Create directories if they don't exist
    if (-not (Test-Path $backgroundsDir)) { New-Item -Path $backgroundsDir -ItemType Directory -Force }
    if (-not (Test-Path $logosDir)) { New-Item -Path $logosDir -ItemType Directory -Force }
    if (-not (Test-Path $charactersDir)) { New-Item -Path $charactersDir -ItemType Directory -Force }
    
    # Download placeholder images
    Invoke-WebRequest -Uri "https://picsum.photos/1920/800" -OutFile "$backgroundsDir\astradigital-ocean.jpg"
    Invoke-WebRequest -Uri "https://picsum.photos/500/500" -OutFile "$logosDir\magmasox-logo.png"
    Invoke-WebRequest -Uri "https://picsum.photos/500/501" -OutFile "$logosDir\kaznak-logo.png"
    Invoke-WebRequest -Uri "https://picsum.photos/400/600" -OutFile "$charactersDir\character-sample.png"
    
    Write-Output "Placeholder images created"
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