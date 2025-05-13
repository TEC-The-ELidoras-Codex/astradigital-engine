# PowerShell script to run WordPress posting tests
# This script provides a menu to run different WordPress posting tests

# Set console colors
$FgGreen = @{ForegroundColor = "Green"}
$FgCyan = @{ForegroundColor = "Cyan"}
$FgYellow = @{ForegroundColor = "Yellow"}
$FgRed = @{ForegroundColor = "Red"}

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

# Check if .env file exists
$EnvPath = Join-Path -Path $ProjectRoot -ChildPath "config\.env"
if (-Not (Test-Path $EnvPath)) {
    Write-Host "❌ .env file not found at $EnvPath" @FgRed
    Write-Host "Please run setup_env.ps1 first to configure your environment variables." @FgYellow
    exit
}

# Function to display the menu
function Show-Menu {
    Clear-Host
    Write-Host "=======================================" @FgCyan
    Write-Host "      WordPress Testing Utility       " @FgCyan
    Write-Host "=======================================" @FgCyan
    Write-Host ""
    Write-Host "1: Run Basic WordPress Connection Test" @FgGreen
    Write-Host "2: Post Test Roadmap Article (Draft)" @FgGreen
    Write-Host "3: Post Test Roadmap Article (Publish)" @FgGreen
    Write-Host "4: Run Enhanced WordPress Test" @FgGreen
    Write-Host "5: Initialize WordPress Categories" @FgGreen
    Write-Host "Q: Quit" @FgYellow
    Write-Host ""
}

# Function to run a test with error handling
function Run-Test {
    param (
        [string]$Command,
        [string]$Description
    )
    
    Write-Host "=======================================" @FgCyan
    Write-Host " $Description " @FgCyan
    Write-Host "=======================================" @FgCyan
    Write-Host ""
    
    try {
        Invoke-Expression $Command
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ Test completed successfully!" @FgGreen
        } else {
            Write-Host "`n❌ Test failed with exit code $LASTEXITCODE" @FgRed
        }
    } catch {
        Write-Host "`n❌ Error executing command: $_" @FgRed
    }
    
    Write-Host "`nPress any key to return to menu..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Main loop
do {
    Show-Menu
    $selection = Read-Host "Select an option"
    
    switch ($selection) {
        '1' {
            Run-Test -Command "python scripts\test_wordpress.py" -Description "Basic WordPress Connection Test"
        }
        
        '2' {
            Run-Test -Command "python scripts\test_roadmap_post.py" -Description "Post Test Roadmap Article (Draft)"
        }
        
        '3' {
            Run-Test -Command "python scripts\test_roadmap_post.py --publish" -Description "Post Test Roadmap Article (Publish)"
        }
        
        '4' {
            # Check if the enhanced test exists
            $EnhancedTestPath = Join-Path -Path $ProjectRoot -ChildPath "scripts\enhanced_wordpress_test.py"
            if (Test-Path $EnhancedTestPath) {
                Run-Test -Command "python scripts\enhanced_wordpress_test.py" -Description "Enhanced WordPress Test"
            } else {
                Write-Host "`n❌ Enhanced WordPress test script not found." @FgRed
                Write-Host "This script might not have been created yet.`n" @FgYellow
                Write-Host "Press any key to return to menu..."
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
        }
        
        '5' {
            # Check if the initialize script exists
            $InitializeWPPath = Join-Path -Path $ProjectRoot -ChildPath "scripts\initialize_wordpress.py"
            if (Test-Path $InitializeWPPath) {
                Run-Test -Command "python scripts\initialize_wordpress.py" -Description "Initialize WordPress Categories"
            } else {
                Write-Host "`n❌ WordPress initialization script not found." @FgRed
                Write-Host "This script might not have been created yet.`n" @FgYellow
                Write-Host "Press any key to return to menu..."
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
        }
        
        'q' {
            return
        }
        
        default {
            Write-Host "`nInvalid selection. Please try again.`n" @FgRed
            Write-Host "Press any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    }
} until ($selection -eq 'q')
