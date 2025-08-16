#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本のAIビジネスニュースを追加
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
import yaml

def add_japanese_feeds():
    """feeds.ymlに日本のAIビジネスニュースを追加"""
    
    print("🇯🇵 日本のAIビジネスニュースフィードを追加中...")
    
    feeds_path = Path('feeds.yml')
    
    # 現在の設定を読み込み
    with open(feeds_path, 'r', encoding='utf-8-sig') as f:
        feeds_config = yaml.safe_load(f)
    
    # 日本のAIビジネスニュースソースを追加
    japanese_business_feeds = [
        {
            "name": "日経新聞 AI・テクノロジー",
            "url": "https://www.nikkei.com/theme/DGXZQOCC140VF0U1A011C2000000.rss",
            "general": True
        },
        {
            "name": "ITmedia AI・機械学習",
            "url": "https://rss.itmedia.co.jp/rss/2.0/ait.xml",
            "general": True
        },
        {
            "name": "ZDNET Japan AI",
            "url": "https://japan.zdnet.com/rss/",
            "general": True
        },
        {
            "name": "ASCII.jp AI・IoT",
            "url": "https://ascii.jp/rss.xml",
            "general": True
        },
        {
            "name": "TechCrunch Japan",
            "url": "https://jp.techcrunch.com/feed/",
            "general": True
        },
        {
            "name": "Google News: 日本AI企業ニュース",
            "url": "https://news.google.com/rss/search?q=(%E3%82%BD%E3%83%95%E3%83%88%E3%83%90%E3%83%B3%E3%82%AF+OR+%E3%83%88%E3%83%A8%E3%82%BF+OR+NTT+OR+%E3%83%91%E3%83%8A%E3%82%BD%E3%83%8B%E3%83%83%E3%82%AF+OR+%E3%82%BD%E3%83%8B%E3%83%BC+OR+%E6%97%A5%E7%AB%8B+OR+%E5%AF%8C%E5%A3%AB%E9%80%9A+OR+NEC+OR+%E6%A5%BD%E5%A4%A9)+AND+(AI+OR+%E4%BA%BA%E5%B7%A5%E7%9F%A5%E8%83%BD+OR+%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92)&hl=ja&gl=JP&ceid=JP:ja",
            "general": True
        },
        {
            "name": "Google News: 日本AI投資・資金調達",
            "url": "https://news.google.com/rss/search?q=(%E8%B5%84%E9%87%91%E8%AA%BF%E9%81%94+OR+%E6%8A%95%E8%B3%87+OR+%E3%83%95%E3%82%A1%E3%83%B3%E3%83%89+OR+%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%88%E3%82%A2%E3%83%83%E3%83%97)+AND+(AI+OR+%E4%BA%BA%E5%B7%A5%E7%9F%A5%E8%83%BD)+%E6%97%A5%E6%9C%AC&hl=ja&gl=JP&ceid=JP:ja",
            "general": True
        },
        {
            "name": "Google News: 生成AI・ChatGPT 日本",
            "url": "https://news.google.com/rss/search?q=(%E7%94%9F%E6%88%90AI+OR+ChatGPT+OR+%E3%82%B8%E3%82%A7%E3%83%8D%E3%83%AC%E3%83%BC%E3%83%86%E3%82%A3%E3%83%96AI+OR+%E5%A4%A7%E8%A6%8F%E6%A8%A1%E8%A8%80%E8%AA%9E%E3%83%A2%E3%83%87%E3%83%AB)+%E6%97%A5%E6%9C%AC&hl=ja&gl=JP&ceid=JP:ja",
            "general": True
        }
    ]
    
    # Businessセクションに追加
    for feed in japanese_business_feeds:
        if feed not in feeds_config['Business']:
            feeds_config['Business'].append(feed)
            print(f"✅ 追加: {feed['name']}")
    
    # 設定を保存
    with open(feeds_path, 'w', encoding='utf-8') as f:
        yaml.dump(feeds_config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ feeds.yml を更新しました（{len(japanese_business_feeds)}個の日本ソース追加）")
    
    return True

def enhance_japanese_ai_filtering():
    """build.pyの日本語AI関連フィルタリングを強化"""
    
    print("\n🧠 日本語AI関連フィルタリングを強化中...")
    
    build_path = Path('build.py')
    content = build_path.read_text(encoding='utf-8')
    
    # 日本語の高関連度キーワードを追加
    japanese_ai_keywords = '''        '人工知能', '機械学習', 'ディープラーニング', 'ニューラルネット',
        'ＡＩ', 'AI', 'ML', 'DL', '生成AI', 'ジェネレーティブAI',
        'チャットGPT', 'ChatGPT', 'GPT', 'LLM', '大規模言語モデル',
        'Claude', 'Gemini', 'Copilot', 'Bard',
        '自然言語処理', 'コンピュータビジョン', '画像認識', '音声認識',
        'ロボティクス', '自動運転', '予測分析', 'データサイエンス',
        'アルゴリズム', '最適化', 'レコメンデーション',
        'スタートアップ', '資金調達', '投資', 'ファンド', 'IPO', 'M&A',
        'ソフトバンク', 'トヨタ', 'NTT', 'ソニー', '日立', '富士通', 'NEC',
        'パナソニック', '楽天', 'リクルート', 'メルカリ', 'LINE','''
    
    # 既存の高関連度キーワードの後に日本語キーワードを追加
    if "'ＡＩ', 'AI', 'ML', 'DL'" in content and "'生成AI'" not in content:
        content = content.replace(
            "'ＡＩ', 'AI', 'ML', 'DL'",
            japanese_ai_keywords
        )
        print("✅ 日本語AIキーワードを追加しました")
    
    # 除外キーワードにも日本語を追加
    japanese_exclude = """        '暗号通貨', 'ゲーム', 'スポーツ', '娯楽', '音楽', '映画',
        '政治', '選挙', '天気', '気候変動', '環境',
        'アニメ', 'マンガ', '芸能', 'タレント', 'アイドル',
        '恋愛', '結婚', 'グルメ', '料理', '旅行', 'ファッション'"""
    
    if "'政治', '選挙', '天気', '気候変動', '環境'" in content and "'アニメ'" not in content:
        content = content.replace(
            "'政治', '選挙', '天気', '気候変動', '環境'",
            japanese_exclude
        )
        print("✅ 日本語除外キーワードを追加しました")
    
    build_path.write_text(content, encoding='utf-8')
    return True

def add_japanese_companies_to_scoring():
    """重要度スコアリングに日本企業を追加"""
    
    print("\n🏢 重要度スコアリングに日本企業を追加中...")
    
    build_path = Path('build.py')
    content = build_path.read_text(encoding='utf-8')
    
    # 日本企業を重要度スコアに追加
    japanese_companies = """        'openai': 100, 'anthropic': 100, 'google': 90, 'microsoft': 90,
        'meta': 85, 'nvidia': 85, 'apple': 80, 'amazon': 80,
        'tesla': 75, 'deepmind': 95, 'cohere': 70, 'hugging face': 70,
        'mistral': 65, 'stability ai': 65, 'midjourney': 60,
        # 日本企業
        'ソフトバンク': 80, 'softbank': 80, 'トヨタ': 75, 'toyota': 75,
        'ntt': 70, 'ソニー': 70, 'sony': 70, '日立': 65, 'hitachi': 65,
        '富士通': 65, 'fujitsu': 65, 'nec': 65, 'パナソニック': 60,
        'panasonic': 60, '楽天': 60, 'rakuten': 60, 'リクルート': 55,
        'recruit': 55, 'メルカリ': 50, 'mercari': 50, 'line': 55"""
    
    if "'mistral': 65, 'stability ai': 65, 'midjourney': 60" in content and "'ソフトバンク'" not in content:
        content = content.replace(
            "'mistral': 65, 'stability ai': 65, 'midjourney': 60",
            japanese_companies
        )
        print("✅ 日本企業を重要度スコアに追加しました")
    
    build_path.write_text(content, encoding='utf-8')
    return True

def test_japanese_sources():
    """日本ソース追加後のテスト"""
    
    print(f"\n🧪 日本ソース追加後のテスト中...")
    
    # 環境変数設定
    os.environ['HOURS_LOOKBACK'] = '48'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '20'
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    try:
        # build.pyを実行
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
        
        # 日本ソースからの記事を確認
        if result.stdout:
            japanese_sources = ['日経', 'ITmedia', 'ZDNET', 'ASCII', 'TechCrunch Japan']
            for line in result.stdout.split('\n'):
                for jp_source in japanese_sources:
                    if jp_source in line and 'Found' in line:
                        print(f"   📰 {line}")
        
        print("✅ 日本ソーステスト完了")
        return True
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False

def deploy_japanese_sources():
    """日本ソースをデプロイ"""
    
    print(f"\n📤 日本ソース機能をデプロイ中...")
    
    try:
        JST = timezone(timedelta(hours=9))
        now = datetime.now(JST)
        
        # Git operations
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        
        files_to_add = ['feeds.yml', 'build.py', 'index.html']
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        commit_msg = f"feat: Add Japanese AI business news sources and enhanced filtering [{now.strftime('%Y-%m-%d %H:%M JST')}]"
        
        try:
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ コミット完了")
        except:
            print("ℹ️ 変更なし")
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ GitHubにプッシュ完了")
        
        return True
        
    except Exception as e:
        print(f"❌ デプロイエラー: {e}")
        return False

def main():
    print("=" * 60)
    print("🇯🇵 日本のAIビジネスニュース追加")
    print("=" * 60)
    
    # Step 1: 日本のフィードを追加
    if not add_japanese_feeds():
        return False
    
    # Step 2: 日本語フィルタリング強化
    if not enhance_japanese_ai_filtering():
        return False
    
    # Step 3: 日本企業を重要度スコアに追加
    if not add_japanese_companies_to_scoring():
        return False
    
    # Step 4: テスト
    if not test_japanese_sources():
        return False
    
    # Step 5: デプロイ
    if not deploy_japanese_sources():
        return False
    
    print("\n" + "=" * 60)
    print("✅ 日本のAIビジネスニュース追加完了!")
    print("=" * 60)
    
    print(f"\n🇯🇵 追加された日本ソース:")
    print(f"  📰 日経新聞 AI・テクノロジー")
    print(f"  💻 ITmedia AI・機械学習")
    print(f"  🔧 ZDNET Japan AI")
    print(f"  📱 ASCII.jp AI・IoT")
    print(f"  🚀 TechCrunch Japan")
    print(f"  📊 Google News: 日本AI企業")
    print(f"  💰 Google News: 日本AI投資")
    print(f"  🤖 Google News: 生成AI日本")
    
    print(f"\n🏢 重要度スコア追加企業:")
    print(f"  ソフトバンク(80), トヨタ(75), NTT(70)")
    print(f"  ソニー(70), 日立(65), 富士通(65)")
    print(f"  楽天(60), リクルート(55), メルカリ(50)")
    
    print(f"\n🌐 サイトURL:")
    print(f"   https://awano27.github.io/daily-ai-news/")
    print(f"\n💡 これで日本のAI業界動向も網羅できます！")
    
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)