# TEC News Automation Scheduler Setup
param(
    [string]$TaskName = "TEC_Airth_News_Automation",
    [string]$ScheduleTime = "08:00",
    [int]$MaxAge = 1,
    [int]$MaxTopics = 3,
    [string]$Status = "draft"
)

Write-Host "🤖 Setting up TEC News Automation Scheduler..." -ForegroundColor Cyan

# Get current directory
$ProjectDir = "C:\Users\Ghedd\TEC_CODE\astradigital-engine"

# Build command arguments
$Arguments = "$ProjectDir\scripts\airth_news_automation.py --max-age $MaxAge --max-topics $MaxTopics --status $Status --notify"

Write-Host "Creating scheduled task: $TaskName" -ForegroundColor Yellow
Write-Host "Command: python $Arguments" -ForegroundColor Gray
Write-Host "Schedule: Daily at $ScheduleTime" -ForegroundColor Gray

# Create the scheduled task
$Action = New-ScheduledTaskAction -Execute "python" -Argument $Arguments -WorkingDirectory $ProjectDir
$Trigger = New-ScheduledTaskTrigger -Daily -At $ScheduleTime
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "TEC Airth News Automation - Daily content generation and publishing" -Force

Write-Host "✅ Task '$TaskName' created successfully!" -ForegroundColor Green
Write-Host "📅 Scheduled to run daily at $ScheduleTime" -ForegroundColor Yellow

# Show next run time
$NextRun = (Get-ScheduledTaskInfo -TaskName $TaskName).NextRunTime
Write-Host "⏰ Next run: $NextRun" -ForegroundColor Magenta

Write-Host ""
Write-Host "TEC News Automation is now scheduled!" -ForegroundColor Green
