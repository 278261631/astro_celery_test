@echo off
chcp 65001 >nul
echo Installing Python dependencies...
echo =================================

echo Installing packages from requirements.txt...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo Dependencies installed successfully!
    echo.
    echo Next steps:
    echo 1. Make sure Redis server is running
    echo 2. Run start_worker.bat to start Celery worker
    echo 3. Run run_demo.bat to execute demo tasks
) else (
    echo.
    echo Failed to install dependencies!
    echo Please check your Python and pip installation.
)

pause
