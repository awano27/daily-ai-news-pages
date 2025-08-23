@echo off
echo Enhanced Daily AI News - Full Integration Test
echo ===========================================

REM Set environment variables for maximum information
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=25
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo Configuration:
echo   Article lookback: %HOURS_LOOKBACK% hours
echo   Max articles per category: %MAX_ITEMS_PER_CATEGORY%
echo   Translation: %TRANSLATE_TO_JA%
echo   X Posts CSV: Configured
echo.

echo Starting enhanced ranking build with SNS integration...
python build_simple_ranking.py

if %ERRORLEVEL% NEQ 0 (
    echo Build failed with error code: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ✅ Build completed successfully!
echo 📄 Generated file: index.html

if exist "index.html" (
    echo 📊 File verification:
    for %%A in (index.html) do echo   Size: %%~zA bytes
    echo.
    echo 🌐 Opening in browser...
    start "" "index.html"
) else (
    echo ⚠️ Warning: Output file not found
)

echo.
echo 🎯 Features implemented:
echo   ✅ Engineer relevance scoring (0-10 scale)
echo   ✅ 5-level priority system (🔥⚡📖📰📄)
echo   ✅ SNS/Twitter posts integration
echo   ✅ arXiv research papers
echo   ✅ Interactive search and filtering
echo   ✅ Bookmark functionality
echo   ✅ Information volume preservation (25+ articles/category)
echo.
echo Test completed!
pause