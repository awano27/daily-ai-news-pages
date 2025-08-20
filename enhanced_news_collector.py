#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced News Collector - Gemini URL contextを使った改良版ニュース収集システム
"""
import os
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
import feedparser
import requests
from pathlib import Path

# Gemini URL context client
try:
    from gemini_url_context import GeminiURLContextClient, get_client
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Gemini URL context機能は利用できません")

# 既存モジュール
try:
    import build
    BUILD_AVAILABLE = True
except ImportError:
    BUILD_AVAILABLE = False

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedNewsCollector:
    """Gemini URL contextを活用した強化版ニュース収集システム"""
    
    def __init__(self):
        """初期化"""
        self.gemini_client = get_client() if GEMINI_AVAILABLE else None
        self.cache_dir = Path("_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # AI関連キーワード
        self.ai_keywords = [
            "AI", "人工知能", "機械学習", "深層学習", "neural network", 
            "transformer", "LLM", "GPT", "Claude", "Gemini", "ChatGPT",
            "生成AI", "generative", "diffusion", "stable diffusion",
            "computer vision", "natural language", "reinforcement learning",
            "MLOps", "AutoML", "federated learning"
        ]
        
        logger.info(f"🤖 Enhanced News Collector initialized (Gemini: {'✅' if GEMINI_AVAILABLE else '❌'})")
    
    def collect_and_analyze_feeds(self, feeds_config: str = "feeds.yml") -> Dict[str, Any]:
        """フィード収集と分析の統合処理"""
        
        # 1. 従来のフィード収集
        logger.info("📡 RSS フィード収集開始...")
        raw_articles = self._collect_rss_feeds(feeds_config)
        
        # 2. AI関連記事のフィルタリング
        logger.info("🔍 AI関連記事フィルタリング...")
        ai_articles = self._filter_ai_articles(raw_articles)
        
        # 3. Gemini URL contextによる深い分析
        if GEMINI_AVAILABLE and ai_articles:
            logger.info("🧠 Gemini URL context分析開始...")
            enhanced_articles = self._analyze_with_gemini(ai_articles)
        else:
            logger.warning("⚠️ Gemini分析をスキップ")
            enhanced_articles = ai_articles
        
        # 4. カテゴリ別整理
        categorized = self._categorize_articles(enhanced_articles)
        
        # 5. 重複除去と品質フィルタ
        final_articles = self._deduplicate_and_filter(categorized)
        
        return {
            "articles": final_articles,
            "statistics": self._calculate_statistics(final_articles),
            "timestamp": datetime.now().isoformat()
        }
    
    def _collect_rss_feeds(self, feeds_config: str) -> List[Dict[str, Any]]:
        """RSSフィード収集（従来ロジック活用）"""
        articles = []
        
        # feeds.ymlの読み込み
        import yaml
        try:
            with open(feeds_config, 'r', encoding='utf-8') as f:
                feeds = yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"❌ {feeds_config} が見つかりません")
            return articles
        
        # 時間フィルタ
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
        
        for category, feed_list in feeds.items():
            if not isinstance(feed_list, list):
                continue
                
            logger.info(f"📰 {category}カテゴリ: {len(feed_list)}フィード")
            
            for feed_info in feed_list:
                if isinstance(feed_info, dict):
                    url = feed_info.get('url')
                    source = feed_info.get('name', 'Unknown')
                    is_general = feed_info.get('general', False)
                else:
                    url = feed_info
                    source = 'Unknown'
                    is_general = False
                
                if not url:
                    continue
                
                try:
                    # RSS解析
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:10]:  # 最新10件
                        # 日時チェック
                        pub_time = None
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            pub_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                            pub_time = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                        
                        if pub_time and pub_time < cutoff_time:
                            continue  # 古い記事をスキップ
                        
                        # 記事情報を構築
                        article = {
                            'title': entry.get('title', '').strip(),
                            'link': entry.get('link', ''),
                            'summary': entry.get('summary', ''),
                            'source': source,
                            'category': category,
                            'published': pub_time.isoformat() if pub_time else '',
                            'is_general_feed': is_general,
                            'raw_entry': entry
                        }
                        
                        articles.append(article)
                        
                except Exception as e:
                    logger.error(f"❌ フィード解析エラー ({url}): {e}")
                    continue
        
        logger.info(f"📊 収集完了: {len(articles)}件の記事")
        return articles
    
    def _filter_ai_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """AI関連記事のフィルタリング"""
        ai_articles = []
        
        for article in articles:
            # 一般フィードはキーワードフィルタリング
            if article.get('is_general_feed', False):
                title = article.get('title', '').lower()
                summary = article.get('summary', '').lower()
                content = f"{title} {summary}"
                
                # AI関連キーワードチェック
                if any(keyword.lower() in content for keyword in self.ai_keywords):
                    ai_articles.append(article)
            else:
                # AI専門フィードはそのまま採用
                ai_articles.append(article)
        
        logger.info(f"🎯 AI関連記事: {len(ai_articles)}件")
        return ai_articles
    
    def _analyze_with_gemini(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gemini URL contextによる記事分析"""
        if not self.gemini_client:
            return articles
        
        enhanced_articles = []
        batch_size = 5  # 一度に分析するURL数
        
        # バッチ処理
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            batch_urls = [article['link'] for article in batch if article.get('link')]
            
            if not batch_urls:
                enhanced_articles.extend(batch)
                continue
            
            try:
                logger.info(f"🧠 バッチ{i//batch_size + 1}: {len(batch_urls)}記事を分析中...")
                
                # Gemini分析実行
                analysis_result = self.gemini_client.summarize_news_articles(
                    article_urls=batch_urls,
                    focus_topics=["技術トレンド", "企業動向", "市場インパクト", "日本への影響"]
                )
                
                # 結果をバッチ記事に統合
                for j, article in enumerate(batch):
                    enhanced_article = article.copy()
                    
                    # Gemini分析結果を追加
                    enhanced_article.update({
                        'gemini_analysis': analysis_result.get('text', ''),
                        'analysis_metadata': {
                            'url_context': analysis_result.get('url_context_metadata'),
                            'usage': analysis_result.get('usage_metadata'),
                            'timestamp': analysis_result.get('timestamp')
                        },
                        'enhanced': True
                    })
                    
                    enhanced_articles.append(enhanced_article)
                
                # レート制限対策
                import time
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Gemini分析エラー (batch {i//batch_size + 1}): {e}")
                # 分析失敗時は元記事をそのまま追加
                for article in batch:
                    article['enhanced'] = False
                enhanced_articles.extend(batch)
        
        logger.info(f"✅ Gemini分析完了: {len(enhanced_articles)}件")
        return enhanced_articles
    
    def _categorize_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """記事のカテゴリ別整理"""
        categories = {
            'business': [],
            'technology': [],
            'research': [],
            'tools': [],
            'other': []
        }
        
        # カテゴリマッピング
        category_mapping = {
            'business': 'business',
            'tech': 'technology',
            'posts': 'research',
            'tools': 'tools'
        }
        
        for article in articles:
            original_category = article.get('category', 'other')
            mapped_category = category_mapping.get(original_category, 'other')
            categories[mapped_category].append(article)
        
        logger.info(f"📊 カテゴリ別記事数: {[(k, len(v)) for k, v in categories.items()]}")
        return categories
    
    def _deduplicate_and_filter(self, categorized: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """重複除去と品質フィルタ"""
        filtered_categories = {}
        
        for category, articles in categorized.items():
            # URL重複除去
            seen_urls = set()
            unique_articles = []
            
            for article in articles:
                url = article.get('link', '')
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_articles.append(article)
            
            # 品質スコア計算
            scored_articles = []
            for article in unique_articles:
                score = self._calculate_quality_score(article)
                article['quality_score'] = score
                scored_articles.append(article)
            
            # スコア順でソート、上位記事を選択
            scored_articles.sort(key=lambda x: x['quality_score'], reverse=True)
            filtered_categories[category] = scored_articles[:15]  # 各カテゴリ最大15件
        
        return filtered_categories
    
    def _calculate_quality_score(self, article: Dict[str, Any]) -> float:
        """記事品質スコア計算"""
        score = 0.0
        
        # タイトル長（適度な長さを評価）
        title_len = len(article.get('title', ''))
        if 20 <= title_len <= 100:
            score += 1.0
        
        # 要約の有無
        if article.get('summary') and len(article.get('summary', '')) > 50:
            score += 1.0
        
        # Gemini分析済み
        if article.get('enhanced', False):
            score += 2.0
        
        # 信頼できるソース
        source = article.get('source', '').lower()
        trusted_sources = ['techcrunch', 'venturebeat', 'wired', 'arxiv', 'google', 'microsoft', 'openai']
        if any(trusted in source for trusted in trusted_sources):
            score += 1.0
        
        # 最新性（24時間以内）
        if article.get('published'):
            try:
                pub_time = datetime.fromisoformat(article['published'].replace('Z', '+00:00'))
                hours_ago = (datetime.now(timezone.utc) - pub_time).total_seconds() / 3600
                if hours_ago <= 24:
                    score += 1.0
            except:
                pass
        
        return score
    
    def _calculate_statistics(self, articles: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """統計情報計算"""
        stats = {
            'total_articles': sum(len(v) for v in articles.values()),
            'by_category': {k: len(v) for k, v in articles.items()},
            'enhanced_count': 0,
            'sources': set(),
            'avg_quality_score': 0.0
        }
        
        all_articles = []
        for article_list in articles.values():
            all_articles.extend(article_list)
        
        if all_articles:
            stats['enhanced_count'] = sum(1 for a in all_articles if a.get('enhanced', False))
            stats['sources'] = list(set(a.get('source', '') for a in all_articles))
            quality_scores = [a.get('quality_score', 0) for a in all_articles]
            stats['avg_quality_score'] = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return stats
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """結果をJSONファイルに保存"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_news_{timestamp}.json"
        
        output_path = self.cache_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 結果保存完了: {output_path}")
        return str(output_path)

def run_enhanced_collection():
    """強化版ニュース収集の実行"""
    print("🚀 Enhanced News Collection with Gemini URL Context")
    
    try:
        collector = EnhancedNewsCollector()
        
        # メイン収集処理
        results = collector.collect_and_analyze_feeds()
        
        # 結果保存
        output_file = collector.save_results(results)
        
        # 統計表示
        stats = results['statistics']
        print(f"\\n📊 収集結果:")
        print(f"   総記事数: {stats['total_articles']}件")
        print(f"   Gemini分析済み: {stats['enhanced_count']}件")
        print(f"   情報源: {len(stats['sources'])}個")
        print(f"   平均品質スコア: {stats['avg_quality_score']:.2f}")
        
        print(f"\\n📂 結果ファイル: {output_file}")
        return results
        
    except Exception as e:
        logger.error(f"❌ 収集処理エラー: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    run_enhanced_collection()