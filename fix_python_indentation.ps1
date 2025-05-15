# Fix Python indentation issues across scripts directory
$pyFiles = Get-ChildItem -Path "scripts" -Filter "*.py" -Recurse

foreach ($file in $pyFiles) {
    Write-Host "Processing $($file.FullName)"
    python -m autopep8 --aggressive --aggressive --in-place $file.FullName
}
