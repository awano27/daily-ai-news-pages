@echo off
echo ⚠️  注意: これはforce pushを行います
echo 続行する前にリモートの変更が重要でないことを確認してください
echo.
set /p confirm="続行しますか？ (y/N): "
if /i not "%confirm%"=="y" (
    echo キャンセルしました
    pause
    exit /b
)

echo.
echo 変更をステージングします...
git add build.py enhanced_x_processor.py

echo コミットを作成します...
git commit -m "fix: 包括的なSNS文字化け対策 - エンコーディング・正規化・制御文字処理

- HTTPリクエスト時のUTF-8エンコーディング明示
- Unicode正規化(NFKC)追加
- HTMLエンティティデコード強化  
- 制御文字・不正文字の除去
- 連続空白の正規化処理
- build.pyとenhanced_x_processor.py両方で対応

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo Force pushを実行します...
git push --force-with-lease origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ Force pushが成功しました！
) else (
    echo.
    echo ❌ Force pushに失敗しました
)

echo.
pause