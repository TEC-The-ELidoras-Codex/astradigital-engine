# TEC Asset Tools Environment Activator
# This script activates the virtual environment for TEC asset tools

& "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\tec-asset-env\Scripts\Activate.ps1"
Write-Host "TEC asset tools environment activated!" -ForegroundColor Green
Write-Host "Available commands:"
Write-Host "  python C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\scripts\optimize.py --help" -ForegroundColor Cyan
Write-Host "  python C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\scripts\prepare_wp_assets.py --help" -ForegroundColor Cyan
Write-Host "  python C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\scripts\prepare_hf_assets.py --help" -ForegroundColor Cyan
