@echo off
chcp 65001 > nul
echo 🔄 Safe Git Push - 競合を自動解決してプッシュ
echo.

echo Step 1: リモートの変更を確認・取得中...
git fetch origin main

echo Step 2: リモートとの差分をチェック...
git status

echo Step 3: リモートの変更を統合...
git pull origin main --no-edit

if %ERRORLEVEL% neq 0 (
    echo.
    echo ⚠️ マージで問題が発生しました。手動で解決が必要です。
    echo 以下のコマンドを実行してください:
    echo   git status
    echo   git add .
    echo   git commit -m "resolve merge conflicts"
    pause
    exit /b 1
)

echo Step 4: 変更をプッシュ...
git push origin main

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ プッシュ成功！
    echo.
) else (
    echo.
    echo ❌ プッシュ失敗 - 再試行が必要かもしれません
    echo.
)

echo 完了時刻: %DATE% %TIME%
pause