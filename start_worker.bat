@echo off
chcp 65001 >nul
echo Starting Celery Worker...
echo ========================

echo Checking Redis connection...
redis-cli ping
if %errorlevel% neq 0 (
    echo Redis is not running! Please start Redis server first.
    echo You can download Redis from: https://github.com/microsoftarchive/redis/releases
    pause
    exit /b 1
)

echo Redis is running, starting Celery worker...
celery -A celery_app worker --loglevel=info --pool=solo

pause
