@echo off
chcp 65001 >nul
echo ========================================
echo    阿里云Tair + Celery 完整演示
echo ========================================
echo.

echo 1. 检查Tair连接...
python -c "from config_manager import ConfigManager; cm = ConfigManager(); success, msg, _ = cm.test_redis_connection(); print(msg); exit(0 if success else 1)"
if %errorlevel% neq 0 (
    echo.
    echo ❌ Tair连接失败！
    echo 请检查并更新 config.json 中的Tair连接信息
    exit /b 1
)

echo.
echo 2. 启动Celery Worker...
start "Celery Worker" cmd /c start_worker.bat

echo.
echo 3. 等待Worker启动...
timeout /t 5 /nobreak >nul

echo.
echo 4. 启动Flower监控...
start "Flower Monitor" cmd /c start_flower_simple.bat

echo.
echo 5. 等待Flower启动...
timeout /t 3 /nobreak >nul

echo.
echo 6. 运行演示任务...
python flower_demo.py

echo.
echo ========================================
echo 演示完成！
echo.
echo 🌐 Flower监控: http://localhost:5555
echo 📊 查看任务执行情况和Worker状态
echo.
echo 3秒后自动关闭所有服务...
timeout /t 3 /nobreak >nul

echo.
echo 正在关闭服务...
taskkill /f /im "celery.exe" 2>nul
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq Celery Worker*" 2>nul
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq Flower Monitor*" 2>nul

echo 所有服务已关闭
