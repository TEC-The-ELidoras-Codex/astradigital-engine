# PowerShell script to guide users through cleaning Git history of secrets
# This script provides guidance only and does not modify Git history directly

Write-Host "⚠️ IMPORTANT: Git History Cleanup Guide ⚠️" -ForegroundColor Yellow
Write-Host "This guide will help you clean sensitive information from Git history."
Write-Host "No changes will be made without your confirmation." -ForegroundColor Green
Write-Host ""

# Check if BFG is installed
$bfgInstalled = $false
try {
    $bfgVersion = Invoke-Expression "java -jar bfg.jar --version" 2>&1
    if ($bfgVersion -match "BFG") {
        $bfgInstalled = $true
    }
} catch {
    $bfgInstalled = $false
}

if (-not $bfgInstalled) {
    Write-Host "BFG Repo-Cleaner not found in the current directory." -ForegroundColor Yellow
    Write-Host "You'll need to download it from: https://rtyley.github.io/bfg-repo-cleaner/" -ForegroundColor Cyan
    Write-Host ""
    
    $downloadBfg = Read-Host "Would you like to download BFG now? (y/n)"
    if ($downloadBfg -eq "y" -or $downloadBfg -eq "Y") {
        $bfgUrl = "https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar"
        $bfgPath = Join-Path -Path (Get-Location) -ChildPath "bfg.jar"
        
        Write-Host "Downloading BFG Repo-Cleaner..." -ForegroundColor Cyan
        try {
            Invoke-WebRequest -Uri $bfgUrl -OutFile $bfgPath
            Write-Host "BFG downloaded successfully to: $bfgPath" -ForegroundColor Green
            $bfgInstalled = $true
        } catch {
            Write-Host "Failed to download BFG: $_" -ForegroundColor Red
            Write-Host "Please download it manually from: https://rtyley.github.io/bfg-repo-cleaner/" -ForegroundColor Yellow
        }
    }
}

# Check if we're in a git repository
$isGitRepo = Test-Path -Path ".git"
if (-not $isGitRepo) {
    Write-Host "This doesn't appear to be a Git repository." -ForegroundColor Red
    Write-Host "Please run this script from the root of your Git repository." -ForegroundColor Yellow
    exit
}

# Print warning
Write-Host "⚠️ WARNING: Cleaning Git history is a destructive operation! ⚠️" -ForegroundColor Red
Write-Host "This will permanently modify your Git repository history." -ForegroundColor Red
Write-Host "All collaborators will need to re-clone or force pull after this process." -ForegroundColor Red
Write-Host ""

$confirmation = Read-Host "Are you absolutely sure you want to proceed? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Operation cancelled. No changes were made." -ForegroundColor Green
    exit
}

# Guide user through process
Write-Host "`n== Step 1: Identify Sensitive Files ==" -ForegroundColor Cyan
Write-Host "First, identify files containing sensitive information."
Write-Host "Common files with secrets include:"
Write-Host "  - .env files"
Write-Host "  - config files with API keys"
Write-Host "  - JSON files with credentials"
Write-Host ""

# Create a text file for sensitive patterns
$patternsFile = "sensitive-patterns.txt"
Write-Host "`n== Step 2: Create Patterns File ==" -ForegroundColor Cyan
Write-Host "Creating a file ($patternsFile) to list sensitive patterns to remove."

@"
# Add patterns for sensitive data to remove from Git history
# Examples:
OPENAI_API_KEY=sk-[a-zA-Z0-9]{40,}
ANTHROPIC_API_KEY=sk-ant-[a-zA-Z0-9]{40,}
WP_PASSWORD=.*
WP_USERNAME=.*
"@ | Out-File -FilePath $patternsFile -Encoding utf8

Write-Host "File created: $patternsFile" -ForegroundColor Green
Write-Host "Please edit this file to add your specific patterns." -ForegroundColor Yellow
Write-Host "Press Enter when you're ready to continue..." -ForegroundColor Yellow
Read-Host

# Guide for BFG usage
Write-Host "`n== Step 3: Clean Repository ==" -ForegroundColor Cyan

if ($bfgInstalled) {
    Write-Host "Run the following commands to clean your repository:" -ForegroundColor Yellow
    Write-Host "`n# 1. Create a fresh clone of your repo (BFG requires this)"
    Write-Host "git clone --mirror https://github.com/yourusername/your-repo.git repo-mirror"
    Write-Host "cd repo-mirror"
    Write-Host ""
    Write-Host "# 2. Run BFG to remove sensitive data"
    Write-Host "java -jar ../bfg.jar --replace-text ../sensitive-patterns.txt"
    Write-Host ""
    Write-Host "# 3. Clean and update the repository"
    Write-Host "git reflog expire --expire=now --all"
    Write-Host "git gc --prune=now --aggressive"
    Write-Host ""
    Write-Host "# 4. Push the changes to GitHub"
    Write-Host "git push --force"
    Write-Host ""
} else {
    Write-Host "Since BFG is not installed, you can use Git's built-in filter-branch (slower but works):" -ForegroundColor Yellow
    Write-Host "`n# Create a backup first!"
    Write-Host "git clone --mirror https://github.com/yourusername/your-repo.git repo-backup"
    Write-Host ""
    Write-Host "# Remove sensitive data (example for a specific file)"
    Write-Host "git filter-branch --force --index-filter \"git rm --cached --ignore-unmatch config/.env\" --prune-empty --tag-name-filter cat -- --all"
    Write-Host ""
    Write-Host "# Force garbage collection"
    Write-Host "git for-each-ref --format=\"delete %(\$refname)\" refs/original | git update-ref --stdin"
    Write-Host "git reflog expire --expire=now --all"
    Write-Host "git gc --prune=now --aggressive"
    Write-Host ""
    Write-Host "# Push changes"
    Write-Host "git push origin --force --all"
    Write-Host "git push origin --force --tags"
    Write-Host ""
}

Write-Host "`n== Step 4: Update API Keys ==" -ForegroundColor Cyan
Write-Host "After cleaning the repository, make sure to:"
Write-Host "1. Revoke and regenerate ALL exposed API keys and credentials"
Write-Host "2. Update your .env file with the new credentials"
Write-Host "3. Ensure .env is in your .gitignore"
Write-Host ""

Write-Host "`n== Step 5: Notify Collaborators ==" -ForegroundColor Cyan
Write-Host "Notify all collaborators that they need to:"
Write-Host "1. Delete their local copy of the repository"
Write-Host "2. Clone a fresh copy"
Write-Host "3. Set up their .env file again with the new credentials"
Write-Host ""

Write-Host "For more information about cleaning Git history, see:"
Write-Host "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository" -ForegroundColor Cyan
