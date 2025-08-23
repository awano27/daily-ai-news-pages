@echo off
echo リモートとの同期を開始します...

REM まずリモートの変更を取得
git fetch origin main

REM リモートとの差分を確認
git status

echo.
echo リモートの変更をローカルにマージします...
git pull origin main

REM マージが成功した場合、変更をプッシュ
if %errorlevel% equ 0 (
    echo.
    echo 変更をプッシュします...
    git add build.py enhanced_x_processor.py
    git commit -m "fix: 包括的なSNS文字化け対策 - エンコーディング・正規化・制御文字処理

- HTTPリクエスト時のUTF-8エンコーディング明示
- Unicode正規化(NFKC)追加
- HTMLエンティティデコード強化  
- 制御文字・不正文字の除去
- 連続空白の正規化処理
- build.pyとenhanced_x_processor.py両方で対応

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    git push origin main
    if %errorlevel% equ 0 (
        echo.
        echo ✅ プッシュが成功しました！
    ) else (
        echo.
        echo ❌ プッシュに失敗しました
    )
) else (
    echo.
    echo ❌ マージに失敗しました。手動で競合を解決してください。
    git status
)

echo.
pause