@echo off
echo Testing Engineer-focused AI News Build
echo =====================================

REM Set environment variables
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=15

echo Running build_engineer_focused.py...
python build_engineer_focused.py

if %ERRORLEVEL% NEQ 0 (
    echo Build failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo Build completed successfully!
echo Generated file: index_engineer_focused.html

REM Check if file was created
if exist "index_engineer_focused.html" (
    echo File created successfully
    echo Opening in default browser...
    start "" "index_engineer_focused.html"
) else (
    echo Warning: Output file not found
)

echo.
echo Build test complete!
pause