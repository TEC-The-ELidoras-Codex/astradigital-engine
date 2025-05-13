# PowerShell script to securely create and configure .env file
# Run this script to set up your environment variables for TEC Office Suite

# Get the script directory and project paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$EnvFile = Join-Path -Path $ProjectRoot -ChildPath "config\.env"
$EnvTemplate = Join-Path -Path $ProjectRoot -ChildPath "config\.env.template"

# Check if .env file already exists
if (Test-Path $EnvFile) {
    $overwrite = Read-Host "The .env file already exists. Do you want to overwrite it? (y/n)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Operation cancelled."
        exit
    }
}

# Check if template exists
if (-not (Test-Path $EnvTemplate)) {
    Write-Host "Error: .env.template file not found at $EnvTemplate"
    exit 1
}

# Copy template to .env
Copy-Item -Path $EnvTemplate -Destination $EnvFile -Force

# Function to update a variable in the .env file
function Update-EnvVar {
    param (
        [string]$VarName,
        [string]$VarPrompt,
        [switch]$IsSensitive = $false
    )
    
    # Get current value from .env file
    $content = Get-Content -Path $EnvFile -Raw
    $pattern = "(?m)^$VarName=(.*)$"
    $match = [regex]::Match($content, $pattern)
    $currentValue = if ($match.Success) { $match.Groups[1].Value } else { "" }
    
    # Prompt for new value
    if ($IsSensitive -and $currentValue -ne "" -and -not $currentValue.StartsWith("your_")) {
        Write-Host "$VarPrompt [currently set - press Enter to keep]: " -NoNewline
        $secureString = Read-Host -AsSecureString
        $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString)
        $newValue = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
    } else {
        if ($IsSensitive) {
            Write-Host "$VarPrompt [current: $currentValue]: " -NoNewline
            $secureString = Read-Host -AsSecureString
            $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString)
            $newValue = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
            [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
        } else {
            $newValue = Read-Host "$VarPrompt [current: $currentValue]"
        }
    }
    
    # Only update if a new value was provided
    if ($newValue -ne "") {
        if ($match.Success) {
            $content = $content -replace "(?m)^$VarName=.*$", "$VarName=$newValue"
        } else {
            $content = "$content`r`n$VarName=$newValue"
        }
        Set-Content -Path $EnvFile -Value $content
        Write-Host "Updated $VarName."
    } else {
        Write-Host "Kept existing value for $VarName."
    }
}

# Set restrictive permissions - limit to current user
$acl = Get-Acl -Path $EnvFile
$acl.SetAccessRuleProtection($true, $false)
$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$fileSystemRights = [System.Security.AccessControl.FileSystemRights]::FullControl
$inheritanceFlags = [System.Security.AccessControl.InheritanceFlags]::None
$propagationFlags = [System.Security.AccessControl.PropagationFlags]::None
$accessControlType = [System.Security.AccessControl.AccessControlType]::Allow
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($identity, $fileSystemRights, $inheritanceFlags, $propagationFlags, $accessControlType)
$acl.AddAccessRule($rule)
Set-Acl -Path $EnvFile -AclObject $acl

Write-Host "Configuring WordPress Settings..."
Update-EnvVar -VarName "WP_URL" -VarPrompt "WordPress URL (e.g., https://yourdomain.com)"
Update-EnvVar -VarName "WP_USERNAME" -VarPrompt "WordPress Username"
Update-EnvVar -VarName "WP_PASSWORD" -VarPrompt "WordPress Application Password (create in WordPress admin)" -IsSensitive
Update-EnvVar -VarName "WP_XMLRPC_PATH" -VarPrompt "WordPress XMLRPC Path (default: /xmlrpc.php)"

Write-Host "`nConfiguring AI Providers..."
Update-EnvVar -VarName "OPENAI_API_KEY" -VarPrompt "OpenAI API Key" -IsSensitive
Update-EnvVar -VarName "OPENAI_MODEL" -VarPrompt "OpenAI Model (default: gpt-4-turbo)"
Update-EnvVar -VarName "ANTHROPIC_API_KEY" -VarPrompt "Anthropic API Key (optional)" -IsSensitive

Write-Host "`nConfiguring Logging..."
Update-EnvVar -VarName "LOG_LEVEL" -VarPrompt "Log Level (INFO, DEBUG, WARNING, ERROR)"
Update-EnvVar -VarName "DEBUG" -VarPrompt "Debug Mode (true/false)"

Write-Host "`nEnvironment configuration complete!"
Write-Host "Your .env file has been created at: $EnvFile"
Write-Host "IMPORTANT: This file contains sensitive information. Do not commit it to version control."
