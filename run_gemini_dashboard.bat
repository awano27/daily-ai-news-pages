@echo off
chcp 65001 > nul
echo Gemini Dashboard Generator
echo.
echo Features:
echo   - Reference site format compliance
echo   - Google Sheets X posts integration
echo   - Gemini 2.0 Flash API translation
echo   - Business-friendly Japanese summaries
echo   - Technical term localization
echo.

REM Load settings from .env file
echo Loading API settings from .env file...

echo Starting dashboard generation...
python generate_reference_format_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo Gemini-powered dashboard generation completed!
    echo.
    echo Improvements:
    echo   - Summary translation: Gemini 2.0 Flash
    echo   - Text quality: Business-oriented Japanese
    echo   - Technical terms: Proper localization
    echo   - Length optimization: 100-150 characters
    echo   - Target audience: General business users
    echo.
    echo Please open the generated HTML file in your browser
    echo.
) else (
    echo.
    echo Error occurred during generation
    echo.
)

pause