@echo off
echo ==== Video Transcription Tool Setup ====
echo This script will install all requirements for the Video Transcription Tool.

REM Check for Python installation
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check for ffmpeg
where ffmpeg >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo FFmpeg is not installed or not in PATH.
    echo.
    echo Please download ffmpeg from https://ffmpeg.org/download.html
    echo Extract the files and add the bin folder to your PATH.
    echo.
    echo Instructions:
    echo 1. Download ffmpeg from https://ffmpeg.org/download.html
    echo 2. Extract the zip file to a folder (e.g., C:\ffmpeg)
    echo 3. Add the bin folder to your PATH:
    echo    - Right-click on 'This PC' and select 'Properties'
    echo    - Click on 'Advanced system settings'
    echo    - Click on 'Environment Variables'
    echo    - Under 'System variables', select 'Path' and click 'Edit'
    echo    - Click 'New' and add the path to the bin folder (e.g., C:\ffmpeg\bin)
    echo    - Click 'OK' on all dialogs
    echo.
    echo After installing ffmpeg, please run this setup script again.
    pause
    exit /b 1
) else (
    echo FFmpeg is already installed.
)

REM Create virtual environment
echo Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists.
) else (
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
)

REM Activate virtual environment and install packages
echo Activating virtual environment and installing Python packages...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing Python packages...
pip install --upgrade pip
pip install openai-whisper faster-whisper

REM Create ToDo directory if it doesn't exist
echo Creating ToDo directory for video files...
if not exist ToDo (
    mkdir ToDo
    echo ToDo directory created.
) else (
    echo ToDo directory already exists.
)

echo.
echo ==== Setup Complete ====
echo To use the Video Transcription Tool:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo 2. Place your video files in the 'ToDo' folder
echo 3. Run the script:
echo    python process_todo_files.py
echo.
echo For more details, please refer to the README.md file.

pause 