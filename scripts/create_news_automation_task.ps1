# Schedule Airth News Automation Task
# This script creates a scheduled task to run the news automation daily

param (
    [Parameter(Mandatory=$false)]
    [int]$MaxAge = 2,
    
    [Parameter(Mandatory=$false)]
    [int]$MaxTopics = 3,
    
    [Parameter(Mandatory=$false)]
    [string]$TimeTrigger = "10:00",
    
    [Parameter(Mandatory=$false)]
    [string]$Status = "draft"
)

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "This script needs to be run as Administrator to create a scheduled task." -ForegroundColor Red
    Write-Host "Please restart this script with Administrator privileges." -ForegroundColor Yellow
    Write-Host "`nAlternatively, you can set up the task manually with the following details:" -ForegroundColor Cyan
    
    $pythonPath = "python"
    $scriptPath = "c:\Users\Ghedd\TEC_CODE\astradigital-engine\scripts\airth_news_automation.py"
    $arguments = "--max-age $MaxAge --max-topics $MaxTopics --status $Status"
    $fullCommand = "$pythonPath $scriptPath $arguments"
    
    Write-Host "Program/Script: $pythonPath" -ForegroundColor Green
    Write-Host "Arguments: $scriptPath $arguments" -ForegroundColor Green
    Write-Host "Start in: c:\Users\Ghedd\TEC_CODE\astradigital-engine\" -ForegroundColor Green
    Write-Host "Schedule: Daily at $TimeTrigger" -ForegroundColor Green
    
    exit 1
}

# Continue with task creation as we're running as admin
Write-Host "Creating scheduled task for Airth News Automation..." -ForegroundColor Green

# Path to script and Python executable
$scriptPath = "c:\Users\Ghedd\TEC_CODE\astradigital-engine\scripts\airth_news_automation.py"
$pythonExe = "python"

# Build the full command
$arguments = "$scriptPath --max-age $MaxAge --max-topics $MaxTopics --status $Status"

# Create the scheduled task action
$action = New-ScheduledTaskAction -Execute $pythonExe -Argument $arguments -WorkingDirectory "c:\Users\Ghedd\TEC_CODE\astradigital-engine\"

# Create the scheduled task trigger (daily at specified time)
$trigger = New-ScheduledTaskTrigger -Daily -At $TimeTrigger

# Create the task principal (run with highest privileges)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U -RunLevel Highest

# Set task settings
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries

# Register the scheduled task
$taskName = "AirthNewsAutomation"
$description = "Run Airth News Automation daily to generate news content from recent tech articles"

try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description $description -Force
    
    Write-Host "Scheduled task '$taskName' created successfully!" -ForegroundColor Green
    Write-Host "Task will run daily at $TimeTrigger" -ForegroundColor Green
    Write-Host "News collection window: $MaxAge days" -ForegroundColor Green
    Write-Host "Maximum topics: $MaxTopics" -ForegroundColor Green
    Write-Host "Post status: $Status" -ForegroundColor Green
} catch {
    Write-Host "Error creating scheduled task: $_" -ForegroundColor Red
    
    Write-Host "`nYou can set up the task manually with the following details:" -ForegroundColor Cyan
    
    Write-Host "Program/Script: $pythonExe" -ForegroundColor Green
    Write-Host "Arguments: $arguments" -ForegroundColor Green
    Write-Host "Start in: c:\Users\Ghedd\TEC_CODE\astradigital-engine\" -ForegroundColor Green
    Write-Host "Schedule: Daily at $TimeTrigger" -ForegroundColor Green
}
