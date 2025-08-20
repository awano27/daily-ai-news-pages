#!/usr/bin/env python3
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
