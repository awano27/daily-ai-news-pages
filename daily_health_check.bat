@echo off
chcp 65001 > nul
echo 🏥 Daily AI News Dashboard - Health Check
echo.
echo Running comprehensive system health check...
echo This will verify all components are working correctly.
echo.

python check_system_health.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ All systems are healthy!
    echo The dashboard should update automatically.
    echo.
) else (
    echo.
    echo ❌ Issues detected - manual intervention may be required.
    echo Please check DAILY_UPDATE_GUIDE.md for troubleshooting steps.
    echo.
)

echo Check completed at: %DATE% %TIME%
pause