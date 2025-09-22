@echo off
chcp 65001 >nul
echo Celery Full Demo with Flower Monitoring
echo =======================================
echo.
echo This demo will start:
echo 1. Redis Server
echo 2. Celery Worker
echo 3. Flower Monitoring (Web UI)
echo 4. Demo Tasks
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Step 1: Checking Tair Connection...
echo ===================================
python -c "from config_manager import ConfigManager; cm = ConfigManager(); success, msg, _ = cm.test_redis_connection(); print(msg); exit(0 if success else 1)"
if %errorlevel% neq 0 (
    echo Tair connection failed! Please check config.json
    pause
    exit /b 1
)
timeout /t 2 >nul

echo.
echo Step 2: Starting Celery Worker...
echo =================================
start "Celery Worker" cmd /c start_worker.bat
timeout /t 5 >nul

echo.
echo Step 3: Starting Flower Monitoring...
echo =====================================
start "Flower Monitoring" cmd /c start_flower_simple.bat
timeout /t 3 >nul

echo.
echo Step 4: Opening Flower Web Interface...
echo =======================================
echo Flower monitoring is available at: http://localhost:5555
echo Opening in your default browser...
start http://localhost:5555
timeout /t 2 >nul

echo.
echo Step 5: Running Demo Tasks...
echo =============================
echo You can now:
echo 1. View the Flower web interface at http://localhost:5555
echo 2. Run demo tasks to see them in real-time
echo.
echo Press any key to run demo tasks...
pause >nul

echo.
echo Running demo tasks...
python producer.py

echo.
echo =======================================
echo Demo completed!
echo.
echo Services are still running:
echo - Tair Instance: Connected and running
echo - Celery Worker: Processing tasks
echo - Flower Monitoring: http://localhost:5555
echo.
echo To stop all services, close the opened windows or press Ctrl+C in each.
echo.
pause
