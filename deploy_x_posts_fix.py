#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X投稿修正版のデプロイスクリプト
"""
import os
import subprocess
import time

print("🚀 X投稿修正版デプロイ開始")
print("=" * 50)

# 環境変数設定
env_vars = {
    'TRANSLATE_TO_JA': '1',
    'TRANSLATE_ENGINE': 'google',
    'HOURS_LOOKBACK': '24',
    'MAX_ITEMS_PER_CATEGORY': '8',
    'X_POSTS_CSV': 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
}

for key, value in env_vars.items():
    os.environ[key] = value
    print(f"✓ {key}={value}")

print("\n🔧 サイト構築中...")

try:
    # build.pyを実行
    result = subprocess.run(['python', 'build.py'], 
                          capture_output=True, text=True, timeout=300)
    
    if result.returncode == 0:
        print("✅ build.py実行成功")
        print(result.stdout[-500:])  # 最後の500文字を表示
    else:
        print(f"❌ build.py実行失敗 (code: {result.returncode})")
        print(result.stderr)
    
    # HTMLファイル確認
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # X投稿が含まれているかチェック
        x_indicators = [
            'X / SNS',
            'Xポスト',
            '強制表示',
            'OpenAI GPT-4o',
            'Anthropic Claude'
        ]
        
        found_indicators = [indicator for indicator in x_indicators if indicator in content]
        
        print(f"\n📊 HTML確認結果:")
        print(f"   ファイルサイズ: {len(content):,} 文字")
        print(f"   X投稿指標: {len(found_indicators)}/{len(x_indicators)} 発見")
        print(f"   発見された指標: {found_indicators}")
        
        if found_indicators:
            print("✅ X投稿が正常にHTMLに含まれています")
        else:
            print("⚠️ X投稿がHTMLに含まれていない可能性があります")
    
    # Gitコミットとプッシュ
    print("\n📤 GitHubにデプロイ中...")
    
    git_commands = [
        ['git', 'add', 'build.py', 'index.html'],
        ['git', 'commit', '-m', 'fix: Force X posts display with score 10.0 and enhanced debug logging'],
        ['git', 'push', 'origin', 'main']
    ]
    
    for cmd in git_commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✓ {' '.join(cmd)}")
            else:
                print(f"⚠️ {' '.join(cmd)}: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"⏰ {' '.join(cmd)}: タイムアウト")
        except Exception as e:
            print(f"❌ {' '.join(cmd)}: {e}")
    
    print("\n🎉 X投稿修正版デプロイ完了")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()