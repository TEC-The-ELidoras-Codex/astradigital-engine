# WordPress Update Script for Airth News Automation
# Run this script after generating a new WordPress application password

param (
    [Parameter(Mandatory=$true)]
    [string]$AppPassword,
    
    [Parameter(Mandatory=$false)]
    [string]$Username = "elidorascodex",
    
    [Parameter(Mandatory=$false)]
    [string]$SiteUrl = "https://elidorascodex.com",
    
    [Parameter(Mandatory=$false)]
    [string]$AppName = "AirthNewsAutomation"
)

# Display information
Write-Host "Updating WordPress configuration for Airth News Automation" -ForegroundColor Green
Write-Host "=================================================="
Write-Host "Site URL: $SiteUrl"
Write-Host "Username: $Username"
Write-Host "App Password: [MASKED]"
Write-Host "App Name: $AppName"
Write-Host "=================================================="

# Call the Python script to update the configuration
$pythonCommand = "python c:\Users\Ghedd\TEC_CODE\astradigital-engine\scripts\configure_wp_automation.py --update-wp-config --app-password '$AppPassword' --username '$Username' --url '$SiteUrl' --app-name '$AppName'"

Write-Host "Running configuration update..."
Invoke-Expression $pythonCommand

# Test the connection
Write-Host "`nTesting WordPress connection..."
$testCommand = "python c:\Users\Ghedd\TEC_CODE\astradigital-engine\scripts\configure_wp_automation.py --test-connection"
Invoke-Expression $testCommand

Write-Host "`nConfiguring automation schedule..."
$automationCommand = "python c:\Users\Ghedd\TEC_CODE\astradigital-engine\scripts\configure_wp_automation.py --update-automation --max-age 2 --max-topics 3 --schedule-time '10:00'"
Invoke-Expression $automationCommand

Write-Host "`nConfiguration complete!" -ForegroundColor Green
Write-Host "You can now run the news automation with the following command:" -ForegroundColor Cyan
Write-Host "python c:\Users\Ghedd\TEC_CODE\astradigital-engine\scripts\airth_news_automation.py --max-age 2 --max-topics 3 --status draft" -ForegroundColor Yellow
