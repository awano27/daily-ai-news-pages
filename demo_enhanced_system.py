#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced System Demo - Gemini URL contextの実際の動作デモ
"""
import os
from pathlib import Path

def load_env_manual():
    """手動で.envファイルを読み込み"""
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def demo_gemini_url_context():
    """Gemini URL context機能のデモ"""
    print("🧠 Gemini URL Context デモ実行")
    
    # 環境設定
    load_env_manual()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY が設定されていません")
        return False
    
    try:
        from gemini_url_context import GeminiURLContextClient
        
        client = GeminiURLContextClient()
        print("✅ Geminiクライアント初期化完了")
        
        # AI業界ニュースURLのサンプル
        demo_urls = [
            "https://techcrunch.com/2024/12/01/anthropic-launches-computer-use/",
            "https://venturebeat.com/ai/"
        ]
        
        print(f"📰 サンプルURL分析中: {len(demo_urls)}件")
        print("   - TechCrunch AI記事")
        print("   - VentureBeat AI ニュース")
        
        # URL context分析実行
        result = client.generate_from_urls(
            prompt="""
            以下のAI業界ニュースを分析し、以下の形式で日本語要約してください：

            ## 主要ニュース
            各記事の核心的な内容を2-3文で要約

            ## 技術トレンド  
            言及されている技術や製品

            ## 業界への影響
            AI業界全体への意味合い

            簡潔で読みやすい形式でお願いします。
            """,
            urls=demo_urls,
            enable_search=False  # デモでは検索なし
        )
        
        if result.get('text') and 'error' not in result:
            print("\n" + "="*60)
            print("📝 **Gemini URL Context 分析結果**")
            print("="*60)
            print(result['text'])
            print("="*60)
            
            # メタデータ表示
            usage = result.get('usage_metadata')
            if usage:
                total_tokens = getattr(usage, 'total_token_count', 0)
                print(f"\n📊 使用量: {total_tokens} tokens")
            
            url_meta = result.get('url_context_metadata')
            if url_meta:
                print("🔗 URL context metadata: 取得済み")
            
            print(f"\n⏰ 実行時刻: {result.get('timestamp')}")
            return True
        else:
            print(f"❌ 分析失敗: {result.get('error', '不明なエラー')}")
            return False
            
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        return False

def demo_enhanced_collector():
    """強化版収集システムのデモ"""
    print("\n📰 Enhanced News Collector デモ")
    
    try:
        # サンプルfeeds.yml作成
        if not Path("feeds.yml").exists():
            sample_feeds = """business:
  - url: "https://techcrunch.com/feed/"
    name: "TechCrunch"
  - url: "https://venturebeat.com/feed/"
    name: "VentureBeat"
    
tech:  
  - url: "https://www.reddit.com/r/MachineLearning/.rss"
    name: "Reddit ML"

posts:
  - url: "https://www.reddit.com/r/artificial/.rss" 
    name: "Reddit AI"
"""
            with open("feeds.yml", "w", encoding="utf-8") as f:
                f.write(sample_feeds)
            print("✅ サンプルfeeds.yml作成完了")
        
        from enhanced_news_collector import EnhancedNewsCollector
        
        collector = EnhancedNewsCollector()
        print("✅ Enhanced News Collector初期化完了")
        
        print("📡 ニュース収集開始（デモモード）...")
        
        # 実際のニュース収集実行（時間制限あり）
        results = collector.collect_and_analyze_feeds()
        
        if results:
            stats = results['statistics']
            print(f"\n📊 収集結果:")
            print(f"   総記事数: {stats['total_articles']}件")
            print(f"   Gemini分析済み: {stats['enhanced_count']}件")
            print(f"   情報源: {len(stats['sources'])}個")
            print(f"   平均品質スコア: {stats['avg_quality_score']:.2f}")
            
            # 結果保存
            output_file = collector.save_results(results)
            print(f"💾 結果保存: {output_file}")
            
            return True
        else:
            print("❌ ニュース収集に失敗しました")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced Collector デモ失敗: {e}")
        return False

def main():
    """デモメイン実行"""
    print("🚀 Enhanced AI News System - Live Demo")
    print("Gemini URL Contextを活用した次世代ニュース収集システム")
    print("="*70)
    
    # 1. URL Context機能デモ
    demo1_success = demo_gemini_url_context()
    
    # 2. 強化版収集システムデモ
    demo2_success = demo_enhanced_collector()
    
    print("\n" + "="*70)
    print("📊 **デモ実行結果**")
    print(f"🧠 Gemini URL Context: {'✅ 成功' if demo1_success else '❌ 失敗'}")
    print(f"📰 Enhanced Collector: {'✅ 成功' if demo2_success else '❌ 失敗'}")
    
    if demo1_success and demo2_success:
        print("\n🎉 **全機能が正常に動作しています！**")
        print("\n🚀 本格運用準備完了:")
        print("1. run_enhanced_build.bat で定期実行")
        print("2. GitHub Actionsとの統合")
        print("3. 品質向上のための継続的改善")
        
    elif demo1_success:
        print("\n✅ **基本機能は動作中**")
        print("URL context機能は正常です。収集システムを調整してください。")
        
    else:
        print("\n⚠️ **設定の見直しが必要**") 
        print("API key設定やネットワーク接続を確認してください。")

if __name__ == "__main__":
    main()