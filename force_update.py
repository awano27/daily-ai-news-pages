#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Pagesを強制更新するスクリプト
"""
import subprocess
import os
from datetime import datetime

print("🔄 GitHub Pages強制更新開始")
print("=" * 40)

try:
    # 現在時刻を取得
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # index.htmlに微小な変更を加える（コメント追加）
    print("📝 HTMLファイルを更新中...")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 既存の更新コメントを探す
    if '<!-- Last update:' in content:
        # 既存のコメントを置換
        import re
        pattern = r'<!-- Last update: .+? -->'
        new_comment = f'<!-- Last update: {timestamp} -->'
        content = re.sub(pattern, new_comment, content)
    else:
        # 新しいコメントを追加（</head>の直前）
        new_comment = f'  <!-- Last update: {timestamp} -->\n</head>'
        content = content.replace('</head>', new_comment)
    
    # ファイルに書き戻し
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ HTMLファイル更新完了: {timestamp}")
    
    # Gitコミット&プッシュ
    print("📤 GitHubにプッシュ中...")
    
    commands = [
        ['git', 'add', 'index.html'],
        ['git', 'commit', '-m', f'Force GitHub Pages update - {timestamp}'],
        ['git', 'push', 'origin', 'main']
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {' '.join(cmd)} 成功")
            else:
                print(f"⚠️ {' '.join(cmd)} エラー: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {' '.join(cmd)} 失敗: {e}")
    
    print("\n🎉 強制更新完了！")
    print("📍 2-3分後に以下で確認:")
    print("   https://awano27.github.io/daily-ai-news/")
    print("   Postsタブ → X / SNS (実データ) が表示されるはず")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()