# TEC AI Agent Orchestrator Activation
# PowerShell script to activate and test the AI Agent system

param(
    [switch]$HealthCheck = $true,
    [switch]$Verbose = $false
)

Write-Host "🤖 TEC AI Agent Orchestrator Activation" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# Get script directory and project root
$ScriptDir = $PSScriptRoot
$ProjectDir = Split-Path $ScriptDir -Parent

# Set up environment
$env:PYTHONPATH = $ProjectDir

if ($Verbose) {
    Write-Host "📁 Project Directory: $ProjectDir" -ForegroundColor Yellow
    Write-Host "🐍 Python Path: $env:PYTHONPATH" -ForegroundColor Yellow
}

# Run the Python activation script
try {
    Write-Host "🚀 Starting AI Agent system activation..." -ForegroundColor Green
    
    $ActivationScript = Join-Path $ScriptDir "activate_ai_agents.py"
    
    if (-not (Test-Path $ActivationScript)) {
        throw "Activation script not found: $ActivationScript"
    }
    
    # Change to project directory
    Push-Location $ProjectDir
    
    # Run the activation script
    $Result = python $ActivationScript
    $ExitCode = $LASTEXITCODE
    
    # Display results
    Write-Host $Result
    
    # Interpret exit codes
    switch ($ExitCode) {
        0 {
            Write-Host "`n✅ AI Agent system activation completed successfully!" -ForegroundColor Green
            Write-Host "🎯 All agents are operational and ready for use." -ForegroundColor Green
        }
        1 {
            Write-Host "`n⚠️ AI Agent system activated with warnings." -ForegroundColor Yellow
            Write-Host "📋 Some optional features may not be available." -ForegroundColor Yellow
        }
        2 {
            Write-Host "`n❌ AI Agent system activation failed." -ForegroundColor Red
            Write-Host "🔧 Please check the logs and resolve critical issues." -ForegroundColor Red
        }
        default {
            Write-Host "`n❓ Unexpected exit code: $ExitCode" -ForegroundColor Magenta
        }
    }
    
    # Show next steps
    Write-Host "`n📋 NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Check logs in: $ProjectDir\logs\" -ForegroundColor White
    Write-Host "2. Run individual agents from: $ProjectDir\src\agents\" -ForegroundColor White
    Write-Host "3. Use news automation: $ProjectDir\scripts\airth_news_automation.py" -ForegroundColor White
    Write-Host "4. View workflows config: $ProjectDir\config\workflows.json" -ForegroundColor White
    
} catch {
    Write-Error "❌ Failed to activate AI Agent system: $_"
    exit 1
} finally {
    Pop-Location
}

Write-Host "`n🎭 TEC AI Agent Orchestrator ready for action!" -ForegroundColor Magenta
