@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Full Intelligence Analysis Mode
echo.
echo Select execution option:
echo   1. Full Analysis    - 5 URLs per category, all AI analysis types (Recommended)
echo   2. Large Analysis   - 10 URLs per category, all AI analysis types  
echo   3. Extra Large      - 15 URLs per category, all AI analysis types
echo   4. Quick Test       - 2 URLs per category, summary only (For testing)
echo.
set /p choice="Select (1-4): "

if "%choice%"=="1" (
    echo Running Full Analysis...
    python run_comprehensive_analysis.py --max-per-category 5
) else if "%choice%"=="2" (
    echo Running Large Analysis...
    python run_comprehensive_analysis.py --max-per-category 10
) else if "%choice%"=="3" (
    echo Running Extra Large Analysis...
    python run_comprehensive_analysis.py --max-per-category 15
) else if "%choice%"=="4" (
    echo Running Quick Analysis...
    python run_comprehensive_analysis.py --quick
) else (
    echo Invalid selection
    goto end
)

echo.
echo Execution completed! Please check the generated JSON files.
:end
pause