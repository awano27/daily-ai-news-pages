@echo off
git add build.py enhanced_x_processor.py test_html_decode.py
git commit -m "fix: SNS記事の文字化け修正 - HTMLエンティティデコード追加

build.pyとenhanced_x_processor.pyでhtml.unescape()を追加し、&amp;&#32;などのHTMLエンティティを正常にデコードするよう修正

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin main
echo コミットとプッシュが完了しました
pause