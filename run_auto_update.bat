@echo off
chcp 65001 > nul
echo ========================================
echo 🔄 Daily AI News 自動更新
echo ========================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📅 %date% %time%
echo.

python auto_update_all.py

if %errorlevel% == 0 (
    echo.
    echo ✅ 更新成功！
) else (
    echo.
    echo ❌ 更新失敗
)

echo.
echo Enterキーを押して終了...
pause > nul
