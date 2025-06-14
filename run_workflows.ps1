# TEC Workflow Management PowerShell Interface
# Easy-to-use interface for running and managing TEC AI workflows

param(
    [Parameter(Position=0)]
    [ValidateSet("run", "list", "monitor", "test", "daily", "original", "maintenance", "emergency")]
    [string]$Action = "list",
    
    [Parameter(Position=1)]
    [string]$WorkflowName,
    
    [string]$Parameters = "{}",
    [switch]$VerboseOutput = $false
)

Write-Host "🤖 TEC AI Workflow Manager" -ForegroundColor Cyan
Write-Host "⏰ $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "=" * 60 -ForegroundColor Gray

# Get script directory and project root
$ScriptDir = $PSScriptRoot
$ProjectDir = Split-Path $ScriptDir -Parent

# Change to project directory
Push-Location $ProjectDir

try {
    switch ($Action) {
        "run" {
            if (-not $WorkflowName) {
                Write-Host "❌ Please specify a workflow name" -ForegroundColor Red
                Write-Host "Usage: .\run_workflows.ps1 run <workflow_name>" -ForegroundColor Yellow
                exit 1
            }
            
            Write-Host "🚀 Running workflow: $WorkflowName" -ForegroundColor Green
            
            $VerboseFlag = if ($VerboseOutput) { "--verbose" } else { "" }
            $Result = python "scripts\workflow_manager.py" run --workflow $WorkflowName --params $Parameters $VerboseFlag
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Workflow completed successfully!" -ForegroundColor Green
            } else {
                Write-Host "❌ Workflow failed!" -ForegroundColor Red
            }
        }
        
        "list" {
            Write-Host "📋 Listing available workflows..." -ForegroundColor Yellow
            python "scripts\workflow_manager.py" list
        }
        
        "monitor" {
            Write-Host "📊 Monitoring workflow status..." -ForegroundColor Yellow
            python "scripts\workflow_manager.py" monitor
        }
        
        "test" {
            Write-Host "🧪 Testing workflow engine..." -ForegroundColor Yellow
            python "scripts\workflow_manager.py" test
        }
        
        "daily" {
            Write-Host "📰 Running daily content automation..." -ForegroundColor Green
            python "scripts\workflow_manager.py" run --workflow "daily_content_automation" --params '{"max_topics": 3, "content_type": "article"}'
        }
        
        "original" {
            Write-Host "✨ Creating original TEC content..." -ForegroundColor Magenta
            python "scripts\workflow_manager.py" run --workflow "original_content_creation" --params '{"topic": "Astradigital Ocean factions", "content_type": "lore"}'
        }
        
        "maintenance" {
            Write-Host "🔧 Running system maintenance..." -ForegroundColor Blue
            python "scripts\workflow_manager.py" run --workflow "system_maintenance" --params '{"days_old": 30}'
        }
        
        "emergency" {
            Write-Host "🚨 Running emergency recovery..." -ForegroundColor Red
            python "scripts\workflow_manager.py" run --workflow "emergency_recovery"
        }
        
        default {
            Write-Host "📋 Available Actions:" -ForegroundColor Cyan
            Write-Host "  list       - List all available workflows" -ForegroundColor White
            Write-Host "  monitor    - Monitor workflow status" -ForegroundColor White
            Write-Host "  test       - Test workflow engine" -ForegroundColor White
            Write-Host "  run <name> - Run specific workflow" -ForegroundColor White
            Write-Host "  daily      - Run daily content automation" -ForegroundColor White
            Write-Host "  original   - Create original TEC content" -ForegroundColor White
            Write-Host "  maintenance- Run system maintenance" -ForegroundColor White
            Write-Host "  emergency  - Emergency recovery" -ForegroundColor White
            
            Write-Host "`n🚀 Quick Examples:" -ForegroundColor Yellow
            Write-Host "  .\run_workflows.ps1 daily" -ForegroundColor Gray
            Write-Host "  .\run_workflows.ps1 original" -ForegroundColor Gray
            Write-Host "  .\run_workflows.ps1 run news_automation" -ForegroundColor Gray
            Write-Host "  .\run_workflows.ps1 monitor" -ForegroundColor Gray
        }
    }
    
} catch {
    Write-Error "❌ Failed to execute workflow action: $_"
    exit 1
} finally {
    Pop-Location
}

Write-Host "`n🎭 TEC Workflow Manager ready!" -ForegroundColor Magenta
