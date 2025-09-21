@echo off
chcp 65001 >nul
echo Starting Redis Server...
echo ========================

echo Checking if Docker is running...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running! Please start Docker Desktop first.
    echo Alternatively, you can install Redis directly from:
    echo https://github.com/microsoftarchive/redis/releases
    pause
    exit /b 1
)

echo Stopping existing Redis container if any...
docker stop redis-celery >nul 2>&1
docker rm redis-celery >nul 2>&1

echo Starting Redis container...
docker run -d -p 6379:6379 --name redis-celery redis:alpine

if %errorlevel% equ 0 (
    echo Redis server started successfully!
    echo Redis is now running on localhost:6379
    echo.
    echo You can now:
    echo 1. Run start_worker.bat to start Celery worker
    echo 2. Run run_demo.bat to execute demo tasks
) else (
    echo Failed to start Redis server!
    echo Please check Docker installation and try again.
)

pause
