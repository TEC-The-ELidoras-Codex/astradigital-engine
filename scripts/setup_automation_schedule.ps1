# Setup Airth News Automation Scheduling
# This script helps set up scheduled tasks for the Airth News Automation system
# Run as administrator for best results

param (
    [string]$TaskName = "Airth News Automation",
    [string]$TimeTrigger = "08:00", # Default 8:00 AM
    [string]$MaxAge = "1",
    [string]$MaxTopics = "3",
    [string]$Status = "draft",
    [switch]$Publish = $false,
    [switch]$Notify = $true
)

# Get the script directory path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir
$AutomationScript = Join-Path -Path $ProjectDir -ChildPath "scripts\airth_news_automation.py"
$PythonExe = "python"

# Build parameters
$PublishParam = if (-not $Publish) { "--no-publish" } else { "" }
$NotifyParam = if ($Notify) { "--notify" } else { "" }

$TaskCommand = "$PythonExe `"$AutomationScript`" --max-age $MaxAge --max-topics $MaxTopics --status $Status $PublishParam $NotifyParam"
$WorkingDir = $ProjectDir

Write-Host "Setting up scheduled task for Airth News Automation:"
Write-Host "Task name: $TaskName"
Write-Host "Time: $TimeTrigger daily"
Write-Host "Command: $TaskCommand"
Write-Host "Working directory: $WorkingDir"

# Check if the task already exists
$TaskExists = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($TaskExists) {
    Write-Host "Task '$TaskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the action
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "$AutomationScript --max-age $MaxAge --max-topics $MaxTopics --status $Status $PublishParam $NotifyParam" -WorkingDirectory $WorkingDir

# Create the trigger
$TriggerTime = (Get-Date).Date.Add([TimeSpan]::Parse($TimeTrigger))
$Trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime

# Create the principal (runs as current user)
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U

# Create the settings
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -WakeToRun

# Create and register the task
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings
Register-ScheduledTask -TaskName $TaskName -InputObject $Task

Write-Host "Task created successfully. It will run daily at $TimeTrigger."
Write-Host "You can check or modify it in Task Scheduler."

# Create a log file for verification
@"
Airth News Automation Schedule
-----------------------------
Scheduled on: $(Get-Date)
Task name: $TaskName
Runs at: $TimeTrigger daily
Command: $TaskCommand
Working directory: $WorkingDir
"@ | Out-File -FilePath (Join-Path -Path $ProjectDir -ChildPath "logs\schedule_setup.log") -Append

Write-Host "Schedule information saved to logs\schedule_setup.log"
