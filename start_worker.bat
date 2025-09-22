@echo off
chcp 65001 >nul
echo Starting Celery Worker...
echo ========================

echo Checking Tair connection...
python -c "from config_manager import ConfigManager; cm = ConfigManager(); success, msg, _ = cm.test_redis_connection(); print(msg); exit(0 if success else 1)"
if %errorlevel% neq 0 (
    echo.
    echo Tair connection failed! Please check:
    echo 1. config.json file exists and is configured correctly
    echo 2. Tair instance is running and accessible
    echo 3. Network connection and firewall settings
    echo.
    echo Please check and update config.json with correct Tair connection info
    pause
    exit /b 1
)

echo Tair is running, starting Celery worker...
celery -A celery_app worker --loglevel=info --pool=solo --queues=celery,math,long_tasks

pause
