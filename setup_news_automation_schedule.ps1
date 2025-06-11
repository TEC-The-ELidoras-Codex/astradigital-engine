# TEC News Automation Scheduler Setup
# Creates Windows Task Scheduler entry for daily news automation

param(
    [string]$TaskName = "TEC_Airth_News_Automation",
    [string]$ScheduleTime = "08:00",
    [int]$MaxAge = 1,
    [int]$MaxTopics = 3,
    [string]$Status = "draft",
    [switch]$EnablePublishing = $true
)

Write-Host "🤖 Setting up TEC News Automation Scheduler..." -ForegroundColor Cyan

# Get current directory
$ScriptDir = $PSScriptRoot
$ProjectDir = Split-Path $ScriptDir -Parent

# Build command arguments
$Arguments = @(
    "$ProjectDir\scripts\airth_news_automation.py"
    "--max-age", $MaxAge
    "--max-topics", $MaxTopics
    "--status", $Status
)

if (-not $EnablePublishing) {
    $Arguments += "--no-publish"
}

$Arguments += "--notify"

# Create the scheduled task
try {
    # Define task action
    $Action = New-ScheduledTaskAction -Execute "python" -Argument ($Arguments -join " ") -WorkingDirectory $ProjectDir
    
    # Define task trigger (daily at specified time)
    $Trigger = New-ScheduledTaskTrigger -Daily -At $ScheduleTime
    
    # Define task settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    # Create the task
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "TEC Airth News Automation - Daily content generation and publishing"
    
    Write-Host "✅ Task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host "📅 Scheduled to run daily at $ScheduleTime" -ForegroundColor Yellow
    Write-Host "⚙️  Parameters: MaxAge=$MaxAge, MaxTopics=$MaxTopics, Status=$Status" -ForegroundColor White
    if ($EnablePublishing) {
        Write-Host "🔄 Publishing: Enabled" -ForegroundColor White
    } else {
        Write-Host "🔄 Publishing: Disabled" -ForegroundColor White
    }
    
    # Show next run time
    $Task = Get-ScheduledTask -TaskName $TaskName
    $NextRun = (Get-ScheduledTaskInfo -TaskName $TaskName).NextRunTime
    Write-Host "⏰ Next run: $NextRun" -ForegroundColor Magenta
    
} catch {
    Write-Error "❌ Failed to create scheduled task: $_"
    exit 1
}
}

Write-Host "`n🎯 TEC News Automation is now scheduled!" -ForegroundColor Green
Write-Host "📋 To manage the task, use Task Scheduler or:" -ForegroundColor White
Write-Host "   Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host "   Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host "   Unregister-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
