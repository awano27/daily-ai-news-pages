@echo off
echo 🔧 Git設定の最適化 - プッシュ競合を減らすための設定

echo リベースでプル設定（マージコミットを減らす）...
git config pull.rebase true

echo 自動プルシュ前にフェッチ...
git config push.autoSetupRemote true

echo 設定完了！
echo.
echo 📋 設定された項目:
git config --list | findstr "pull\|push"

echo.
echo ✅ これで今後のプッシュがスムーズになります
pause