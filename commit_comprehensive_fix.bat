@echo off
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
echo 包括的修正のコミットとプッシュが完了しました
pause