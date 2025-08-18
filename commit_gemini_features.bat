@echo off
echo Committing Gemini translation features to Git...
echo.

REM Add specific files to git
git add generate_reference_format_dashboard.py
git add test_reference_format.py
git add run_reference_format.bat
git add run_gemini_dashboard.bat
git add install_dependencies.bat

echo Checking git status...
git status

echo.
echo Creating commit...
git commit -m "feat: Add Gemini API translation for AI news summaries

- Implement Gemini 1.5 Flash API integration for English to Japanese translation
- Add smart translation logic to skip Japanese content and short summaries
- Include quota management with 30 translation limit per run
- Create reference format dashboard matching awano27.github.io style
- Add comprehensive error handling and fallback mechanisms
- Remove redundant action items, restore enhanced footer links
- Support both .env file and manual environment variable configuration

🤖 Generated with Claude Code(https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

if %ERRORLEVEL% == 0 (
    echo.
    echo Commit successful! Pushing to remote...
    git push origin main
    
    if %ERRORLEVEL% == 0 (
        echo.
        echo Successfully pushed Gemini translation features to Git!
        echo.
        echo Changes include:
        echo   - Gemini API translation integration
        echo   - Reference format dashboard generator
        echo   - Smart quota management
        echo   - Enhanced error handling
        echo   - Improved user experience
        echo.
    ) else (
        echo.
        echo Push failed - please check your remote repository settings
        echo.
    )
) else (
    echo.
    echo Commit failed - please check for conflicts
    echo.
)

pause