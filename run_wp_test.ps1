# A PowerShell wrapper script to run and capture output from the WordPress posting test
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = ".\logs\wp_posting_test_$timestamp.log"

Write-Output "Starting WordPress posting test at $timestamp" | Out-File -FilePath $logFile

try {
    # Run the Python script and capture output
    $output = python .\scripts\test_wordpress_posting.py 2>&1
    $output | Out-File -FilePath $logFile -Append
    
    # Add final message
    Write-Output "`nTest completed at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File -FilePath $logFile -Append
    
    Write-Output "Test completed. Results written to $logFile"
}
catch {
    Write-Output "Error running WordPress posting test: $_" | Out-File -FilePath $logFile -Append
    Write-Output "Test failed. Error details written to $logFile"
}
