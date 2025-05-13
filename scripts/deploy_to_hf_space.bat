@echo off
REM deploy_to_hf_space.bat - Windows script for deploying to Hugging Face Spaces
REM Usage: deploy_to_hf_space.bat --username USERNAME --space SPACENAME [--create]

setlocal enabledelayedexpansion

REM Default values
set CREATE_SPACE=0

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :end_parse_args
if /i "%~1"=="--username" (
    set "USERNAME=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="-u" (
    set "USERNAME=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--space" (
    set "SPACENAME=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="-s" (
    set "SPACENAME=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--create" (
    set CREATE_SPACE=1
    shift
    goto :parse_args
)
if /i "%~1"=="-c" (
    set CREATE_SPACE=1
    shift
    goto :parse_args
)
if /i "%~1"=="--help" (
    goto :show_usage
)
if /i "%~1"=="-h" (
    goto :show_usage
)
echo Unknown option: %~1
goto :show_usage
:end_parse_args

REM Check required arguments
if "%USERNAME%"=="" (
    echo Error: Username is required
    goto :show_usage
)
if "%SPACENAME%"=="" (
    echo Error: Space name is required
    goto :show_usage
)

echo === TEC Office Hugging Face Space Deployment ===
echo Username: %USERNAME%
echo Space: %SPACENAME%

REM Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed
    exit /b 1
)

REM Check if the huggingface_connection.py script exists
set "HF_SCRIPT=scripts\huggingface_connection.py"
if not exist "%HF_SCRIPT%" (
    echo Error: %HF_SCRIPT% script not found
    exit /b 1
)

REM Check if the space exists
echo Checking if space exists...
python "%HF_SCRIPT%" check "%USERNAME%" "%SPACENAME%"
set SPACE_CHECK=%ERRORLEVEL%

REM Create the space if needed
if %SPACE_CHECK% neq 0 (
    if %CREATE_SPACE% equ 1 (
        echo Space does not exist. Creating...
        python "%HF_SCRIPT%" create "%USERNAME%" "%SPACENAME%" --sdk gradio --hardware cpu-basic
        set SPACE_CREATE=%ERRORLEVEL%
        
        if %SPACE_CREATE% neq 0 (
            echo Error: Failed to create space
            exit /b 1
        )
        
        echo Space created successfully
        REM Give Hugging Face a moment to set up the space
        echo Waiting 5 seconds for space initialization...
        timeout /t 5 > nul
    ) else (
        echo Error: Space does not exist and --create was not specified
        exit /b 1
    )
)

REM Create files to ignore during deployment
echo # Git and version control > .hfignore
echo .git >> .hfignore
echo .github >> .hfignore
echo .gitignore >> .hfignore
echo. >> .hfignore
echo # Environment and configuration >> .hfignore
echo venv >> .hfignore
echo .venv >> .hfignore
echo env >> .hfignore
echo .env >> .hfignore
echo config/.env >> .hfignore
echo. >> .hfignore
echo # Python cache files >> .hfignore
echo __pycache__ >> .hfignore
echo *.pyc >> .hfignore
echo *.pyo >> .hfignore
echo *.pyd >> .hfignore
echo .pytest_cache >> .hfignore
echo. >> .hfignore
echo # Editor and IDE files >> .hfignore
echo .vscode >> .hfignore
echo .idea >> .hfignore
echo *.swp >> .hfignore
echo *.swo >> .hfignore
echo. >> .hfignore
echo # Build and distribution >> .hfignore
echo build >> .hfignore
echo dist >> .hfignore
echo *.egg-info >> .hfignore
echo. >> .hfignore
echo # Data directories >> .hfignore
echo data/memories/* >> .hfignore
echo ^!data/memories/.gitkeep >> .hfignore
echo data/lore/* >> .hfignore
echo ^!data/lore/.gitkeep >> .hfignore
echo data/storage/* >> .hfignore
echo ^!data/storage/.gitkeep >> .hfignore
echo. >> .hfignore
echo # Logs >> .hfignore
echo logs/* >> .hfignore
echo ^!logs/.gitkeep >> .hfignore
echo. >> .hfignore
echo # Other >> .hfignore
echo .DS_Store >> .hfignore

REM Create a custom app_hf.py file for HF Space
echo #!/usr/bin/env python3 > app_hf.py
echo """>> app_hf.py
echo Entry point for the TEC Office Hugging Face Space.>> app_hf.py
echo This file is automatically loaded by Hugging Face Spaces.>> app_hf.py
echo """>> app_hf.py
echo import os>> app_hf.py
echo import sys>> app_hf.py
echo import logging>> app_hf.py
echo from pathlib import Path>> app_hf.py
echo import gradio as gr>> app_hf.py
echo.>> app_hf.py
echo # Configure logging>> app_hf.py
echo logging.basicConfig(>> app_hf.py
echo     level=logging.INFO,>> app_hf.py
echo     format='%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s'>> app_hf.py
echo )>> app_hf.py
echo logger = logging.getLogger("TEC.HFSpace")>> app_hf.py
echo.>> app_hf.py
echo # Check if we're running in a Hugging Face Space>> app_hf.py
echo HF_SPACE = os.environ.get('SPACE_ID') is not None>> app_hf.py
echo if HF_SPACE:>> app_hf.py
echo     logger.info("Running in Hugging Face Space environment")>> app_hf.py
echo else:>> app_hf.py
echo     logger.info("Running in local environment")>> app_hf.py
echo.>> app_hf.py
echo # Import the Gradio app>> app_hf.py
echo try:>> app_hf.py
echo     from app import demo>> app_hf.py
echo     logger.info("Successfully imported Gradio app")>> app_hf.py
echo except ImportError as e:>> app_hf.py
echo     logger.error(f"Failed to import Gradio app: {e}")>> app_hf.py
echo     # Create a fallback demo>> app_hf.py
echo     demo = gr.Interface(>> app_hf.py
echo         fn=lambda text: f"TEC Office setup error: {str(e)}",>> app_hf.py
echo         inputs=gr.Textbox(label="Input"),>> app_hf.py
echo         outputs=gr.Textbox(label="Output"),>> app_hf.py
echo         title="TEC Office - Error",>> app_hf.py
echo         description="There was an error loading the TEC Office application.">> app_hf.py
echo     )>> app_hf.py
echo.>> app_hf.py
echo if __name__ == "__main__":>> app_hf.py
echo     demo.launch()>> app_hf.py

REM Deploy to the space
echo Uploading files to space...
python "%HF_SCRIPT%" upload "%USERNAME%" "%SPACENAME%"
set UPLOAD_STATUS=%ERRORLEVEL%

if %UPLOAD_STATUS% neq 0 (
    echo Error: Failed to upload files to space
    exit /b 1
)

REM Clean up temporary files
del .hfignore
del app_hf.py

echo Deployment completed successfully!
echo Visit your space at: https://huggingface.co/spaces/%USERNAME%/%SPACENAME%
exit /b 0

:show_usage
echo Usage: deploy_to_hf_space.bat [options]
echo.
echo Options:
echo   -u, --username USERNAME  Hugging Face username or organization
echo   -s, --space SPACENAME   Hugging Face space name
echo   -c, --create           Create space if it doesn't exist
echo   -h, --help             Show this help message
echo.
echo Examples:
echo   deploy_to_hf_space.bat -u your-username -s tec-office -c
echo   deploy_to_hf_space.bat --username your-organization --space tec-agent-hub
exit /b 1
