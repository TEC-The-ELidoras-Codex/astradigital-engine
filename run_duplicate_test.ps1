# PowerShell wrapper script to run the duplicate detection test
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = ".\logs\duplicate_detection_test_$timestamp.log"

Write-Output "Starting duplicate detection test at $timestamp" | Out-File -FilePath $logFile

try {
    # Run the Python script and capture output
    Write-Output "Running duplicate detection test script..."
    $output = python .\scripts\test_duplicate_detection.py 2>&1
    $output | Out-File -FilePath $logFile -Append
    
    # Display the output to console as well
    $output
    
    # Add final message
    Write-Output "`nTest completed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -FilePath $logFile -Append
    
    Write-Output "`nTest completed. Results written to $logFile"
}
catch {
    Write-Output "Error running duplicate detection test: $_" | Out-File -FilePath $logFile -Append
    Write-Output "Test failed. Error details written to $logFile"
    Write-Output "Error: $_"
}
