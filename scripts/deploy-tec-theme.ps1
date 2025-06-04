# TEC WordPress Theme Deployment Script
# Creates a production-ready ZIP package for WordPress installation

param(
    [string]$OutputPath = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\builds",
    [string]$ThemeName = "tec-theme",
    [string]$Version = "1.0.0"
)

# Function to write colored output
function Write-ColoredOutput {
    param([string]$Message, [string]$Color = "Green")
    Write-Host $Message -ForegroundColor $Color
}

# Main deployment function
function Deploy-TECTheme {
    Write-ColoredOutput "🚀 TEC Theme Deployment Starting..." "Cyan"
    
    # Define paths
    $SourcePath = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\theme"
    $BuildPath = Join-Path $OutputPath "wordpress-theme"
    $ThemeFolder = Join-Path $BuildPath $ThemeName
    $ZipPath = Join-Path $OutputPath "$ThemeName-v$Version.zip"
    
    # Ensure output directory exists
    if (!(Test-Path $OutputPath)) {
        New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
        Write-ColoredOutput "✅ Created output directory: $OutputPath"
    }
    
    # Clean previous build
    if (Test-Path $BuildPath) {
        Remove-Item $BuildPath -Recurse -Force
        Write-ColoredOutput "🧹 Cleaned previous build"
    }
    
    # Create build directory structure
    New-Item -ItemType Directory -Path $ThemeFolder -Force | Out-Null
      # Files to exclude
    $ExcludeFiles = @(
        "WORDPRESS_FUNCTION_ERRORS_ANALYSIS.md",
        "*.log",
        "*.tmp",
        ".DS_Store",
        "Thumbs.db"
    )
    
    Write-ColoredOutput "📦 Copying theme files..."
    
    # Copy all theme files except excluded ones
    $allItems = Get-ChildItem -Path $SourcePath
    foreach ($item in $allItems) {
        $shouldExclude = $false
        foreach ($excludePattern in $ExcludeFiles) {
            if ($item.Name -like $excludePattern) {
                $shouldExclude = $true
                break
            }
        }
        
        if (-not $shouldExclude) {
            $sourcePath = $item.FullName
            $destPath = Join-Path $ThemeFolder $item.Name
            
            if ($item.PSIsContainer) {
                # Copy directory
                Copy-Item $sourcePath $destPath -Recurse -Force
                Write-ColoredOutput "  📁 Copied directory: $($item.Name)" "Yellow"
            } else {
                # Copy file
                Copy-Item $sourcePath $destPath -Force
                Write-ColoredOutput "  📄 Copied file: $($item.Name)" "Yellow"
            }
        } else {
            Write-ColoredOutput "  🚫 Excluded: $($item.Name)" "DarkGray"
        }
    }
    
    # Remove excluded files from copied structure
    foreach ($excludePattern in $ExcludeFiles) {
        $excludeItems = Get-ChildItem -Path $ThemeFolder -Name $excludePattern -Recurse -ErrorAction SilentlyContinue
        foreach ($excludeItem in $excludeItems) {
            $excludePath = Join-Path $ThemeFolder $excludeItem
            if (Test-Path $excludePath) {
                Remove-Item $excludePath -Force
                Write-ColoredOutput "  🗑️ Removed: $excludeItem" "Red"
            }
        }
    }
    
    # Verify required WordPress theme files
    $requiredFiles = @("style.css", "index.php", "functions.php")
    $missingFiles = @()
    
    foreach ($required in $requiredFiles) {
        $filePath = Join-Path $ThemeFolder $required
        if (!(Test-Path $filePath)) {
            $missingFiles += $required
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-ColoredOutput "❌ Missing required WordPress theme files: $($missingFiles -join ', ')" "Red"
        return $false
    }
    
    Write-ColoredOutput "✅ All required WordPress theme files present"
    
    # Create deployment info file
    $deploymentInfo = @"
# TEC WordPress Theme - Deployment Info

**Theme Name:** The Elidoras Codex  
**Version:** $Version  
**Build Date:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  
**Build Environment:** Windows PowerShell  

## Installation Instructions

1. Download the ZIP file: ``$ThemeName-v$Version.zip``
2. Log into your WordPress admin panel
3. Go to **Appearance > Themes > Add New**
4. Click **Upload Theme**
5. Choose the ZIP file & click **Install Now**
6. Activate the theme
7. Go to **Appearance > Menus** to set up navigation
8. Configure widgets in **Appearance > Widgets**

## Theme Features

✅ Responsive mobile design  
✅ TEC faction integration  
✅ Cartel signup functionality  
✅ Admin dashboard for signups  
✅ Custom post types (Factions, Entities)  
✅ SEO optimized  
✅ Modern CSS Grid & Flexbox  
✅ TailwindCSS integration  
✅ Mobile menu with animations  

## Support

Visit: https://elidorascodex.com  
Email: kaznakalpha@elidorascodex.com  

Built with 💜 by The Machine Goddess
"@
    
    $deploymentInfo | Out-File -FilePath (Join-Path $ThemeFolder "DEPLOYMENT_INFO.md") -Encoding UTF8
    
    # Create ZIP package
    Write-ColoredOutput "📦 Creating ZIP package..."
    
    # Remove existing ZIP if it exists
    if (Test-Path $ZipPath) {
        Remove-Item $ZipPath -Force
    }
    
    # Create ZIP using .NET compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($ThemeFolder, $ZipPath)
    
    # Verify ZIP was created
    if (Test-Path $ZipPath) {
        $zipSize = [math]::Round((Get-Item $ZipPath).Length / 1MB, 2)
        Write-ColoredOutput "✅ ZIP package created successfully!" "Green"
        Write-ColoredOutput "📍 Location: $ZipPath" "Cyan"
        Write-ColoredOutput "📊 Size: $zipSize MB" "Yellow"
        
        # Clean up build directory
        Remove-Item $BuildPath -Recurse -Force
        
        Write-ColoredOutput "`n🎉 TEC WordPress Theme Package Ready for Deployment!" "Magenta"
        Write-ColoredOutput "Upload this ZIP to your WordPress site: $ZipPath" "White"
        
        return $true
    } else {
        Write-ColoredOutput "❌ Failed to create ZIP package" "Red"
        return $false
    }
}

# Execute deployment
try {
    $success = Deploy-TECTheme
    if ($success) {
        Write-ColoredOutput "`n✨ Ready to conquer the Astradigital Ocean! ✨" "Magenta"
    }
} catch {
    Write-ColoredOutput "❌ Deployment failed: $($_.Exception.Message)" "Red"
    Write-ColoredOutput "Stack trace: $($_.ScriptStackTrace)" "DarkRed"
}
