@echo off
chcp 65001 >nul
echo Starting Flower Monitoring...
echo ============================

echo Starting Flower monitoring...
echo.
echo Flower will be available at: http://localhost:5555
echo Press Ctrl+C to stop Flower
echo.

celery -A celery_app flower --port=5555
