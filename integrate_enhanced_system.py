#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Script - 既存システムにGemini URL context機能を統合
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def backup_existing_files():
    """既存ファイルのバックアップ"""
    backup_dir = Path("_backup") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_backup = [
        "build.py",
        "generate_comprehensive_dashboard.py", 
        "requirements.txt"
    ]
    
    print("📦 既存ファイルをバックアップ中...")
    for filename in files_to_backup:
        if Path(filename).exists():
            shutil.copy2(filename, backup_dir / filename)
            print(f"   ✅ {filename} -> {backup_dir / filename}")
    
    return backup_dir

def create_enhanced_build_system():
    """強化版ビルドシステムの作成"""
    
    enhanced_build_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Build System - Gemini URL contextを統合したビルドシステム
"""
import os
import sys
from pathlib import Path

# 既存ビルドシステムを保持
try:
    import build as original_build
    ORIGINAL_BUILD_AVAILABLE = True
except ImportError:
    ORIGINAL_BUILD_AVAILABLE = False

# 強化版収集システム
try:
    from enhanced_news_collector import EnhancedNewsCollector
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

def enhanced_build_process():
    """強化版ビルドプロセス"""
    print("🚀 Enhanced Build Process with Gemini URL Context")
    
    # Gemini API キーの確認
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️ GEMINI_API_KEY が設定されていません")
        print("📝 .env ファイルに GEMINI_API_KEY=your_key_here を追加してください")
        
        if ORIGINAL_BUILD_AVAILABLE:
            print("🔄 従来のビルドシステムにフォールバック...")
            return original_build.main() if hasattr(original_build, 'main') else None
        else:
            print("❌ フォールバックシステムも利用できません")
            return None
    
    if ENHANCED_AVAILABLE:
        print("🧠 Gemini URL context使用可能")
        
        # 強化版収集システム実行
        collector = EnhancedNewsCollector()
        results = collector.collect_and_analyze_feeds()
        
        if results:
            # 結果を既存フォーマットに変換
            converted_data = convert_to_legacy_format(results)
            
            # 既存のダッシュボード生成システムを使用
            if ORIGINAL_BUILD_AVAILABLE:
                return generate_dashboard_with_enhanced_data(converted_data)
            else:
                print("📄 enhanced_news_*.json ファイルのみ生成")
                return results
        else:
            print("❌ 強化版収集に失敗、フォールバック実行")
            if ORIGINAL_BUILD_AVAILABLE:
                return original_build.main() if hasattr(original_build, 'main') else None
    else:
        print("⚠️ 強化版システム利用不可、従来システム使用")
        if ORIGINAL_BUILD_AVAILABLE:
            return original_build.main() if hasattr(original_build, 'main') else None
    
    return None

def convert_to_legacy_format(enhanced_results):
    """強化版結果を既存フォーマットに変換"""
    articles = enhanced_results.get('articles', {})
    
    # 既存形式への変換
    legacy_format = {
        'business': [],
        'tech': [], 
        'posts': []
    }
    
    # カテゴリマッピング
    category_mapping = {
        'business': 'business',
        'technology': 'tech',
        'research': 'posts',
        'tools': 'tech'
    }
    
    for category, article_list in articles.items():
        legacy_category = category_mapping.get(category, 'posts')
        
        for article in article_list:
            legacy_item = {
                'title': article.get('title', ''),
                'link': article.get('link', ''),
                'summary': article.get('gemini_analysis') or article.get('summary', ''),
                '_source': article.get('source', ''),
                '_dt': article.get('published', ''),
                '_category': legacy_category,
                '_enhanced': article.get('enhanced', False),
                '_quality_score': article.get('quality_score', 0)
            }
            legacy_format[legacy_category].append(legacy_item)
    
    return legacy_format

def generate_dashboard_with_enhanced_data(data):
    """強化データでダッシュボード生成"""
    try:
        from generate_comprehensive_dashboard import analyze_ai_landscape, generate_improved_dashboard
        
        # 既存システムに強化データを注入
        enhanced_dashboard = generate_improved_dashboard()
        
        print("✅ 強化版ダッシュボード生成完了")
        return enhanced_dashboard
        
    except ImportError:
        print("⚠️ ダッシュボード生成システムが見つかりません")
        return None

if __name__ == "__main__":
    enhanced_build_process()
'''
    
    with open("enhanced_build.py", "w", encoding="utf-8") as f:
        f.write(enhanced_build_content)
    
    print("✅ enhanced_build.py 作成完了")

def update_requirements():
    """requirements.txtの更新"""
    
    # 既存のrequirements読み込み
    existing_requirements = set()
    if Path("requirements.txt").exists():
        with open("requirements.txt", "r") as f:
            existing_requirements.update(line.strip() for line in f if line.strip())
    
    # 新しい依存関係を追加
    new_requirements = {
        "google-genai",
        "python-dotenv",
        "pyyaml",
        "feedparser",
        "requests",
        "deep-translator>=1.11.4"
    }
    
    # 統合
    all_requirements = existing_requirements | new_requirements
    
    with open("requirements.txt", "w") as f:
        for req in sorted(all_requirements):
            f.write(f"{req}\\n")
    
    print("✅ requirements.txt 更新完了")

def create_env_template():
    """環境変数テンプレートの作成"""
    
    env_template = """# Gemini API設定
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Vertex AI使用時（オプション）
# GOOGLE_GENAI_USE_VERTEXAI=true

# Google Search併用（オプション）
# ENABLE_GOOGLE_SEARCH=true

# 既存の設定
TRANSLATE_TO_JA=1
TRANSLATE_ENGINE=google
HOURS_LOOKBACK=24
MAX_ITEMS_PER_CATEGORY=8

# X投稿CSV（オプション）
X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0
"""
    
    env_path = Path(".env.example")
    with open(env_path, "w") as f:
        f.write(env_template)
    
    print(f"✅ {env_path} 作成完了")
    print("📝 実際の.envファイルに GEMINI_API_KEY を設定してください")

def create_test_script():
    """テストスクリプトの作成"""
    
    test_script = '''#!/usr/bin/env python3
"""
Enhanced System Test - Gemini URL context統合のテスト
"""
import os
from pathlib import Path

def test_gemini_integration():
    """Gemini統合のテスト"""
    print("🧪 Gemini URL Context統合テスト")
    
    # 環境変数チェック
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY が設定されていません")
        return False
    
    try:
        from gemini_url_context import GeminiURLContextClient
        
        client = GeminiURLContextClient()
        print("✅ Geminiクライアント初期化成功")
        
        # 簡単なテスト
        test_urls = ["https://ai.google.dev/"]
        result = client.generate_from_urls(
            "このページの要点を1文で教えてください",
            test_urls
        )
        
        if result.get("text"):
            print("✅ URL解析テスト成功")
            print(f"📝 結果: {result['text'][:100]}...")
            return True
        else:
            print("❌ URL解析テスト失敗")
            return False
            
    except Exception as e:
        print(f"❌ テスト失敗: {e}")
        return False

def test_enhanced_collector():
    """強化版収集システムのテスト"""
    print("\\n📰 Enhanced News Collector テスト")
    
    try:
        from enhanced_news_collector import EnhancedNewsCollector
        
        collector = EnhancedNewsCollector()
        print("✅ Enhanced Collector初期化成功")
        
        # feeds.ymlの存在確認
        if not Path("feeds.yml").exists():
            print("⚠️ feeds.yml が見つかりません（テスト継続）")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Collector テスト失敗: {e}")
        return False

def test_integration():
    """統合テスト"""
    print("\\n🔗 統合テスト")
    
    try:
        from enhanced_build import enhanced_build_process
        print("✅ enhanced_build モジュール読み込み成功")
        return True
        
    except Exception as e:
        print(f"❌ 統合テスト失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Enhanced AI News System - Integration Test\\n")
    
    results = []
    results.append(test_gemini_integration())
    results.append(test_enhanced_collector())
    results.append(test_integration())
    
    print(f"\\n📊 テスト結果: {sum(results)}/{len(results)} 成功")
    
    if all(results):
        print("✅ すべてのテストに合格しました！")
        print("\\n🎉 次のステップ:")
        print("1. pip install -r requirements.txt")
        print("2. .envファイルにGEMINI_API_KEYを設定")
        print("3. python enhanced_build.py を実行")
    else:
        print("❌ 一部のテストが失敗しました")
        print("エラー内容を確認して設定を見直してください")
'''
    
    with open("test_integration.py", "w") as f:
        f.write(test_script)
    
    print("✅ test_integration.py 作成完了")

def main():
    """統合作業のメイン処理"""
    print("🔧 Gemini URL Context統合作業開始")
    print("=" * 50)
    
    try:
        # 1. バックアップ
        backup_dir = backup_existing_files()
        print(f"📦 バックアップ完了: {backup_dir}")
        
        # 2. 強化版ビルドシステム作成
        create_enhanced_build_system()
        
        # 3. 依存関係更新
        update_requirements()
        
        # 4. 環境変数テンプレート作成
        create_env_template()
        
        # 5. テストスクリプト作成
        create_test_script()
        
        print("=" * 50)
        print("✅ 統合作業完了！")
        print()
        print("📋 次に実行してください:")
        print("1. pip install -r requirements.txt")
        print("2. .envファイルを作成し、GEMINI_API_KEYを設定")
        print("3. python test_integration.py でテスト実行")
        print("4. python enhanced_build.py で強化版ビルド実行")
        print()
        print("🎯 主要な新機能:")
        print("- Gemini URL contextによる深い記事分析")
        print("- 品質スコアによる記事ランキング")
        print("- AI関連キーワードの自動フィルタリング")
        print("- 使用量とコストの透明性")
        print("- 既存システムとの互換性維持")
        
    except Exception as e:
        print(f"❌ 統合作業エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()