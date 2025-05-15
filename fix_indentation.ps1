Get-ChildItem -Path 'scripts' -Filter *.py -Recurse | ForEach-Object { Write-Host \
Processing
\; python -m autopep8 --aggressive --aggressive --in-place .FullName }
