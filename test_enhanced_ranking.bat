@echo off
echo Testing Enhanced Daily AI News with Ranking System
echo ================================================

REM Set environment variables for maximum information retention
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=25

echo Configuration:
echo   HOURS_LOOKBACK: %HOURS_LOOKBACK%
echo   MAX_ITEMS_PER_CATEGORY: %MAX_ITEMS_PER_CATEGORY%
echo   TRANSLATE_TO_JA: %TRANSLATE_TO_JA%
echo.

echo Running enhanced ranking build system...
python build_enhanced_ranking.py

if %ERRORLEVEL% NEQ 0 (
    echo Build failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Build completed successfully!
echo Generated: index.html (with ranking system)

REM Check if file was created and show stats
if exist "index.html" (
    echo File created successfully
    echo File size: 
    for %%A in (index.html) do echo   %%~zA bytes
    echo.
    echo Opening in default browser...
    start "" "index.html"
) else (
    echo Warning: Output file not found
)

echo.
echo Enhanced Ranking System Features:
echo   📊 Technical relevance scoring
echo   🔥 Priority-based visual indicators  
echo   🔍 Advanced search and filtering
echo   📌 Bookmark functionality
echo   ⌨️ Keyboard shortcuts
echo   💾 User preference persistence
echo.
echo Test complete!
pause