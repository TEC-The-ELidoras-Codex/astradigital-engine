# Script to run TEC tests using pytest
# Usage: .\run_tests.ps1 [all|wordpress|integration|unit] [-v|--verbose] [--collect-only]

param (
    [Parameter(Position=0)]
    [ValidateSet("all", "wordpress", "integration", "unit")]
    [string]$TestType = "all",
    
    [Parameter()]
    [Alias("v")]
    [switch]$VerboseOutput,
    
    [Parameter()]
    [switch]$CollectOnly,
    
    [Parameter()]
    [string]$JunitXml
)

# Determine the test path
if ($TestType -eq "all") {
    $TestPath = "tests"
} else {
    $TestPath = "tests\$TestType"
}

# Build pytest command
$PytestArgs = @("python", "-m", "pytest", $TestPath)

if ($VerboseOutput) {
    $PytestArgs += "-v"
}

if ($CollectOnly) {
    $PytestArgs += "--collect-only"
}

if ($JunitXml) {
    $PytestArgs += "--junit-xml"
    $PytestArgs += $JunitXml
}

# Print the command
Write-Host "Running: $($PytestArgs -join ' ')" -ForegroundColor Cyan

# Execute the command
& $PytestArgs[0] $PytestArgs[1..$PytestArgs.Length]

# Get the exit code from the last command
$ExitCode = $LASTEXITCODE

# Exit with the same code
exit $ExitCode
