# A PowerShell wrapper script to run and capture output from the Airth news automation
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = ".\logs\news_automation_$timestamp.log"

Write-Output "Starting Airth news automation at $timestamp" | Out-File -FilePath $logFile

try {
    # Run the Python script and capture output
    $output = python .\scripts\airth_news_automation.py --max-age 3 --max-topics 2 --status draft 2>&1
    $output | Out-File -FilePath $logFile -Append
    
    # Add final message
    Write-Output "`nAutomation completed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -FilePath $logFile -Append
    
    Write-Output "Automation completed. Results written to $logFile"
}
catch {
    Write-Output "Error running Airth news automation: $_" | Out-File -FilePath $logFile -Append
    Write-Output "Automation failed. Error details written to $logFile"
}
