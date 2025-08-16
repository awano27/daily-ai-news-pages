#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大きなニュースを上位に表示するスマートソート機能を追加
"""
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
import re

def add_importance_scoring():
    """build.pyに重要度スコアリング機能を追加"""
    
    print("🎯 重要度スコアリング機能を追加中...")
    
    build_path = Path('build.py')
    content = build_path.read_text(encoding='utf-8')
    
    # 重要度スコアリング関数を追加
    scoring_function = '''
def calculate_importance_score(item):
    """
    ニュースの重要度スコアを計算
    大きなニュースほど高いスコアを返す
    """
    title = item.get("title", "").lower()
    summary = item.get("_summary", "").lower()
    source = item.get("_source", "").lower()
    content = f"{title} {summary}"
    
    score = 0
    
    # 1. 企業・組織の重要度（大手企業ほど高スコア）
    major_companies = {
        'openai': 100, 'anthropic': 100, 'google': 90, 'microsoft': 90,
        'meta': 85, 'nvidia': 85, 'apple': 80, 'amazon': 80,
        'tesla': 75, 'deepmind': 95, 'cohere': 70, 'hugging face': 70,
        'mistral': 65, 'stability ai': 65, 'midjourney': 60
    }
    
    for company, points in major_companies.items():
        if company in content:
            score += points
            break  # 最高スコアのみ適用
    
    # 2. 重要キーワード（画期的な発表ほど高スコア）
    high_impact_keywords = {
        'breakthrough': 80, 'launch': 70, 'release': 65, 'announce': 60,
        'unveil': 75, 'introduce': 60, 'partnership': 55, 'acquisition': 85,
        'funding': 70, 'investment': 65, 'ipo': 90, 'valuation': 60,
        'gpt-5': 100, 'gpt-4': 80, 'claude': 70, 'gemini': 70,
        'billion': 75, 'million': 50, 'record': 65, 'first': 60
    }
    
    for keyword, points in high_impact_keywords.items():
        if keyword in content:
            score += points * 0.5  # 重複を避けるため0.5倍
    
    # 3. ソースの信頼性・影響力
    source_credibility = {
        'techcrunch': 80, 'bloomberg': 90, 'reuters': 85, 'wsj': 85,
        'financial times': 80, 'the verge': 70, 'wired': 70,
        'mit technology review': 85, 'nature': 95, 'science': 95,
        'anthropic': 90, 'openai': 90, 'google': 85, 'meta': 80
    }
    
    for src, points in source_credibility.items():
        if src in source:
            score += points * 0.3  # ソース信頼性は30%の重み
            break
    
    # 4. 技術的重要度
    tech_importance = {
        'artificial general intelligence': 100, 'agi': 100,
        'multimodal': 70, 'reasoning': 60, 'safety': 65,
        'alignment': 70, 'robotics': 60, 'autonomous': 55,
        'quantum': 70, 'neural network': 50, 'transformer': 60
    }
    
    for tech, points in tech_importance.items():
        if tech in content:
            score += points * 0.4
    
    # 5. 新鮮度ボーナス（新しいニュースにボーナス）
    dt = item.get("_dt")
    if dt:
        hours_old = (NOW - dt).total_seconds() / 3600
        if hours_old < 6:  # 6時間以内
            score += 30
        elif hours_old < 12:  # 12時間以内
            score += 20
        elif hours_old < 24:  # 24時間以内
            score += 10
    
    # 6. タイトルの長さ（詳細なタイトルほどニュース価値高い）
    title_length = len(item.get("title", ""))
    if title_length > 80:
        score += 15
    elif title_length > 50:
        score += 10
    
    return max(score, 0)  # 負のスコアは0に
'''
    
    # 関数を追加（is_ai_relevantの後に挿入）
    if 'def is_ai_relevant(' in content and 'def calculate_importance_score(' not in content:
        content = content.replace(
            'def build_cards(items, translator):',
            scoring_function + '\ndef build_cards(items, translator):'
        )
        print("✅ 重要度スコアリング関数を追加しました")
    
    # gather_items関数のソート部分を修正
    old_sort = """    # sort by time desc
    items.sort(key=lambda x: x["_dt"], reverse=True)"""
    
    new_sort = """    # スマートソート: 重要度と時刻を組み合わせて並び替え
    if category_name == "Business":
        # ビジネスニュースは重要度順でソート
        items.sort(key=lambda x: (calculate_importance_score(x), x["_dt"]), reverse=True)
        print(f"[INFO] {category_name}: Sorted by importance score")
    else:
        # その他のカテゴリは時刻順
        items.sort(key=lambda x: x["_dt"], reverse=True)"""
    
    if old_sort in content:
        content = content.replace(old_sort, new_sort)
        print("✅ ビジネスニュースに重要度ソートを適用しました")
    
    # ファイルを保存
    build_path.write_text(content, encoding='utf-8')
    print("✅ build.py を更新しました")
    
    return True

def test_smart_sort():
    """スマートソート機能をテスト"""
    
    print(f"\n🧪 スマートソート機能をテスト中...")
    
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
        
        # 結果を確認
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'Sorted by importance' in line or 'Business' in line:
                    print(f"   {line}")
        
        # 生成されたHTMLでビジネスニュースの順序を確認
        index_path = Path('index.html')
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ビジネスセクションの最初の3つのタイトルを抽出
            business_section = content.split('id="business"')[1].split('id="tools"')[0] if 'id="business"' in content else ""
            titles = re.findall(r'<a class="card-title"[^>]*>([^<]+)</a>', business_section)
            
            if titles:
                print(f"\n📊 ビジネスニュース上位3件（重要度順）:")
                for i, title in enumerate(titles[:3], 1):
                    print(f"   {i}. {title[:60]}{'...' if len(title) > 60 else ''}")
        
        print("✅ スマートソート機能のテスト完了")
        return True
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False

def deploy_smart_sort():
    """スマートソート機能をデプロイ"""
    
    print(f"\n📤 スマートソート機能をデプロイ中...")
    
    try:
        JST = timezone(timedelta(hours=9))
        now = datetime.now(JST)
        
        # Git operations
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        
        files_to_add = ['build.py', 'index.html']
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        commit_msg = f"feat: Add smart sorting for business news (importance-based ranking) [{now.strftime('%Y-%m-%d %H:%M JST')}]"
        
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
    print("🎯 スマートソート機能追加 - 大きなニュースを上位表示")
    print("=" * 60)
    
    # Step 1: 重要度スコアリング機能を追加
    if not add_importance_scoring():
        return False
    
    # Step 2: 機能をテスト
    if not test_smart_sort():
        return False
    
    # Step 3: デプロイ
    if not deploy_smart_sort():
        return False
    
    print("\n" + "=" * 60)
    print("✅ スマートソート機能追加完了!")
    print("=" * 60)
    
    print(f"\n🎯 新機能:")
    print(f"  🏢 ビジネスニュース: 重要度順でソート")
    print(f"  📈 大手企業（OpenAI、Google等）のニュースが上位")
    print(f"  🚀 重要キーワード（launch、breakthrough等）を優先")
    print(f"  📰 信頼性の高いソース（TechCrunch、Bloomberg等）を重視")
    print(f"  ⏰ 新鮮なニュースにボーナス")
    
    print(f"\n⚡ その他のカテゴリ:")
    print(f"  📊 ツール・研究カテゴリは時刻順を維持")
    
    print(f"\n🌐 サイトURL:")
    print(f"   https://awano27.github.io/daily-ai-news/")
    
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)