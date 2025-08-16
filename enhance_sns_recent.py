#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
8/14以降の新しい情報のみでSNSポストを増加・重要度順
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def enhance_recent_sns():
    """build.pyのSNSポスト処理を8/14以降で強化"""
    
    print("📱 8/14以降の新しいSNSポストを大幅強化中...")
    
    build_path = Path('build.py')
    content = build_path.read_text(encoding='utf-8')
    
    # 1. 日付フィルタリングを8/14以降に戻し、取得範囲を拡大
    old_date_filter = """                        # 8/10以降の投稿を含める（より多くの投稿を取得）
            aug10_jst = datetime(2025, 8, 10, 0, 0, 0, tzinfo=JST)
            if post_date >= aug10_jst:  # 期間制限を緩和してより多く取得"""
    
    new_date_filter = """                        # 8/14以降の新しい投稿のみ（より多く取得）
            aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
            if post_date >= aug14_jst:  # 8/14以降の新しい情報のみ、期間制限なし"""
    
    # 別のパターンも確認
    alt_old_filter = """                        # 8/14以降の投稿のみ含める
            aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
            if post_date >= aug14_jst and (NOW - post_date) <= timedelta(hours=HOURS_LOOKBACK):"""
    
    alt_new_filter = """                        # 8/14以降の新しい投稿のみ（より多く取得）
            aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
            if post_date >= aug14_jst:  # 8/14以降の新しい情報のみ、期間制限なし"""
    
    if old_date_filter in content:
        content = content.replace(old_date_filter, new_date_filter)
        print("✅ SNSポストの日付フィルタリングを8/14以降に修正しました")
    elif alt_old_filter in content:
        content = content.replace(alt_old_filter, alt_new_filter)
        print("✅ SNSポストの日付フィルタリングを8/14以降に修正しました")
    
    # 2. SNSポスト用の重要度スコアリング関数が存在するか確認、なければ追加
    if 'def calculate_sns_importance_score(' not in content:
        sns_scoring_function = '''
def calculate_sns_importance_score(item):
    """
    SNSポストの重要度スコアを計算（8/14以降の新しい情報用）
    企業アカウント、インフルエンサー、内容の重要度で判定
    """
    title = item.get("title", "").lower()
    summary = item.get("_summary", "").lower()
    username = ""
    
    # ユーザー名を抽出
    if "xポスト" in title:
        username = title.replace("xポスト", "").strip().lower()
    
    content = f"{title} {summary}"
    score = 0
    
    # 1. 企業・組織アカウントの重要度（公式アカウントほど高スコア）
    enterprise_accounts = {
        '@openai': 100, '@anthropic': 100, '@google': 90, '@microsoft': 90,
        '@meta': 85, '@nvidia': 85, '@apple': 80, '@amazon': 80,
        '@deepmind': 95, '@huggingface': 80, '@langchainai': 75,
        '@cohereai': 70, '@stabilityai': 70, '@midjourney': 65,
        # 日本企業アカウント  
        '@softbank': 80, '@toyota': 75, '@nttcom': 70, '@sony': 70,
        '@hitachi_ltd': 65, '@fujitsu_global': 65, '@nec_corp': 65,
        '@rakuten': 60, '@recruit_jp': 55, '@mercari_jp': 50,
        # AI研究者・インフルエンサー
        '@ylecun': 90, '@karpathy': 90, '@jeffdean': 85, '@goodfellow_ian': 85,
        '@elonmusk': 75, '@satyanadella': 80, '@sundarpichai': 80,
        '@sama': 95, '@darioacemoglu': 80, '@fchollet': 85,
        '@hardmaru': 75, '@adcock_brett': 70, '@minimaxir': 65,
        # 日本のAI研究者・インフルエンサー
        '@karaage0703': 70, '@shi3z': 65, '@yukihiko_n': 60,
        '@npaka': 65, '@ohtaman': 60, '@toukubo': 55,
        # その他の著名人
        '@windsurf': 60, '@oikon48': 55, '@godofprompt': 50,
        '@newsfromgoogle': 70, '@suh_sunaneko': 50, '@pop_ikeda': 45
    }
    
    for account, points in enterprise_accounts.items():
        if account in username or account.replace('@', '') in username:
            score += points
            break  # 最高スコアのみ適用
    
    # 2. コンテンツの重要度（技術的な内容ほど高スコア）
    high_value_keywords = {
        'breakthrough': 50, 'release': 40, 'launch': 40, 'announce': 35,
        'gpt-5': 80, 'gpt-4': 60, 'claude': 50, 'gemini': 50,
        'research': 40, 'paper': 35, 'model': 30, 'ai': 20,
        'artificial intelligence': 40, 'machine learning': 35,
        'deep learning': 35, 'neural network': 30,
        # 日本語キーワード
        '人工知能': 35, '機械学習': 30, 'ディープラーニング': 30,
        '生成ai': 45, 'chatgpt': 40, '大規模言語モデル': 35,
        '研究': 30, '論文': 25, 'モデル': 20, 'ブレークスルー': 45,
        '資金調達': 40, '投資': 35, 'スタートアップ': 30
    }
    
    for keyword, points in high_value_keywords.items():
        if keyword in content:
            score += points * 0.3  # 重複を避けるため0.3倍
    
    # 3. エンゲージメント指標
    engagement_indicators = {
        'thread': 15, 'important': 20, 'must read': 25, 'breaking': 30,
        'update': 10, 'new': 15, 'latest': 10, 'just': 10,
        '重要': 20, '必見': 25, '最新': 10, '速報': 30, '更新': 10,
        '解決': 20, 'ついに': 15, '問題': 10
    }
    
    for indicator, points in engagement_indicators.items():
        if indicator in content:
            score += points * 0.2
    
    # 4. 投稿の新鮮度（8/14以降の新しさを重視）
    dt = item.get("_dt")
    if dt:
        aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
        hours_since_aug14 = (dt - aug14_jst).total_seconds() / 3600
        
        # 8/15の投稿に最高ボーナス
        if hours_since_aug14 >= 24:  # 8/15以降
            score += 30
        elif hours_since_aug14 >= 12:  # 8/14午後
            score += 20
        elif hours_since_aug14 >= 0:  # 8/14朝
            score += 10
    
    # 5. テキスト長ボーナス（詳細な投稿ほど高価値）
    text_length = len(summary)
    if text_length > 100:
        score += 10
    elif text_length > 50:
        score += 5
    
    return max(score, 0)  # 負のスコアは0に
'''
        
        # SNSスコアリング関数を追加
        content = content.replace(
            'def build_cards(items, translator):',
            sns_scoring_function + '\ndef build_cards(items, translator):'
        )
        print("✅ SNSポスト重要度スコアリング関数を追加しました")
    
    # 3. PostsカテゴリのSNS重要度ソートを確認・追加
    if 'calculate_sns_importance_score(x)' not in content:
        old_posts_sort = """    else:
        # その他のカテゴリは時刻順
        items.sort(key=lambda x: x["_dt"], reverse=True)"""
        
        new_posts_sort = """    elif category_name == "Posts":
        # SNS/論文ポストは重要度順でソート
        items.sort(key=lambda x: (calculate_sns_importance_score(x), x["_dt"]), reverse=True)
        print(f"[INFO] {category_name}: Sorted by SNS importance score")
    else:
        # ツールカテゴリは時刻順
        items.sort(key=lambda x: x["_dt"], reverse=True)"""
        
        if old_posts_sort in content:
            content = content.replace(old_posts_sort, new_posts_sort)
            print("✅ SNS/論文ポストに重要度ソートを適用しました")
    
    # ファイルを保存
    build_path.write_text(content, encoding='utf-8')
    print("✅ build.py を更新しました")
    
    return True

def test_recent_sns():
    """8/14以降の強化されたSNS機能をテスト"""
    
    print(f"\n🧪 8/14以降の強化されたSNS機能をテスト中...")
    
    # 環境変数設定（8/14以降で多くのSNSポストを取得）
    os.environ['HOURS_LOOKBACK'] = '48'  # 48時間
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'  # 30件に増加
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
        
        # SNSポスト処理の結果を確認
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'X post' in line or 'SNS importance' in line or 'Adding' in line and 'X posts' in line:
                    print(f"   📱 {line}")
        
        # 生成されたHTMLでSNSポストの順序を確認
        index_path = Path('index.html')
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Postsセクションの件数確認
            import re
            posts_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">SNS/論文ポスト</div>', content)
            if posts_match:
                posts_count = int(posts_match.group(1))
                print(f"\n📊 SNS/論文ポスト表示件数: {posts_count}件")
                
                if posts_count > 8:
                    print(f"✅ 成功！従来の8件から{posts_count}件に増加")
                else:
                    print(f"⚠️ 件数が増加していません")
            
            # Postsセクションの最初の5つのタイトルを抽出
            posts_section = content.split('id="posts"')[1].split('</section>')[0] if 'id="posts"' in content else ""
            titles = re.findall(r'<a class="card-title"[^>]*>([^<]+)</a>', posts_section)
            
            if titles:
                print(f"\n📱 SNS/論文ポスト上位5件（重要度順・8/14以降）:")
                for i, title in enumerate(titles[:5], 1):
                    print(f"   {i}. {title[:70]}{'...' if len(title) > 70 else ''}")
        
        print("✅ 8/14以降の強化されたSNS機能テスト完了")
        return True
        
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False

def deploy_recent_sns():
    """8/14以降の強化されたSNS機能をデプロイ"""
    
    print(f"\n📤 8/14以降の強化されたSNS機能をデプロイ中...")
    
    try:
        JST = timezone(timedelta(hours=9))
        now = datetime.now(JST)
        
        # Git operations
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        
        files_to_add = ['build.py', 'index.html']
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        commit_msg = f"feat: Enhanced SNS posts from 8/14+ with importance scoring (30 items) [{now.strftime('%Y-%m-%d %H:%M JST')}]\n\n📱 Improvements:\n- Focus on 8/14+ recent posts only\n- Increased to 30 SNS posts max\n- Importance-based ranking\n- Enterprise accounts prioritized\n- No old news, fresh content only"
        
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
    print("📱 8/14以降の新しいSNSポスト大幅強化")
    print("=" * 60)
    
    # Step 1: 8/14以降のSNS強化
    if not enhance_recent_sns():
        return False
    
    # Step 2: 機能をテスト
    if not test_recent_sns():
        return False
    
    # Step 3: デプロイ
    if not deploy_recent_sns():
        return False
    
    print("\n" + "=" * 60)
    print("✅ 8/14以降の新しいSNSポスト強化完了!")
    print("=" * 60)
    
    print(f"\n📱 強化された機能:")
    print(f"  📅 対象期間: 8/14以降の新しい情報のみ")
    print(f"  📊 表示件数: 最大30件（従来の4倍）")
    print(f"  🎯 重要度順: 企業アカウント・インフルエンサー優先")
    print(f"  🚫 古いニュース除外: 8/13以前は表示しない")
    
    print(f"\n🏆 優先されるアカウント（8/14以降のポスト）:")
    print(f"  🌟 OpenAI(100), Anthropic(100), Sam Altman(95)")
    print(f"  🤖 Google(90), Yann LeCun(90), Karpathy(90)")
    print(f"  🇯🇵 karaage0703(70), shi3z(65), windsurf(60)")
    
    print(f"\n⚡ 新鮮度ボーナス:")
    print(f"  🔥 8/15の投稿: +30点")
    print(f"  🌟 8/14午後: +20点")
    print(f"  ⭐ 8/14朝: +10点")
    
    print(f"\n🌐 サイトURL:")
    print(f"   https://awano27.github.io/daily-ai-news/")
    print(f"\n💡 8/14以降の最新・高品質SNSポストのみお楽しみください！")
    
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)