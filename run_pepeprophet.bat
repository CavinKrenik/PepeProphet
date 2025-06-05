@echo off
cd /d "%~dp0"

:: Check if venv exists, if not create it
if not exist "venv\" (
    echo [Setup] Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Install requirements
echo [Setup] Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

:: Run the app
echo [Start] Launching PepeProphet...
python start_all.py

pause
