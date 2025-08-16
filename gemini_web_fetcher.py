#!/usr/bin/env python3
"""
Gemini APIを使用してWebコンテンツや403エラーになるソースから情報を取得
"""
import os
import time
import json
import requests
from typing import List, Dict, Optional
from gemini_analyzer import GeminiAnalyzer

class GeminiWebFetcher:
    def __init__(self):
        """Gemini Web Fetcher初期化"""
        self.analyzer = GeminiAnalyzer()
        self.session = requests.Session()
        
    def fetch_from_problematic_source(self, url: str, source_name: str) -> List[Dict]:
        """
        403エラーなどアクセス困難なソースからGemini APIで情報取得
        
        Args:
            url: 取得したいURL (例: Google NewsのRSS)
            source_name: ソース名
            
        Returns:
            ニュース項目のリスト
        """
        if not self.analyzer.enabled:
            print(f"⚠️ Gemini API not available for {source_name}")
            return []
        
        print(f"🤖 Gemini APIで{source_name}の最新ニュースを取得中...")
        
        # Geminiにニュース生成を依頼
        prompt = f"""
あなたはAI業界のニュースアナリストです。
以下のソースから最新のAI関連ニュースを5件程度教えてください：

ソース: {source_name}
URL: {url}

以下の形式でJSON配列として返してください：
[
  {{
    "title": "ニュースタイトル（英語）",
    "title_ja": "ニュースタイトル（日本語）",
    "summary": "要約（英語、100文字程度）",
    "source": "{source_name}",
    "url": "記事URL",
    "importance": 1-10の重要度スコア
  }}
]

最新のAI業界動向について、以下のトピックを含めてください：
- 大手企業（OpenAI, Google, Microsoft, Anthropic等）の動向
- 新しいAIモデルやツールのリリース
- 投資や買収のニュース
- 規制や政策の動向
- 技術的なブレークスルー

JSON形式のみを返してください。説明文は不要です。
"""
        
        response = self.analyzer._make_request(prompt)
        
        if response:
            try:
                # JSONレスポンスをパース
                import re
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    news_items = json.loads(json_match.group())
                    
                    # 現在時刻を追加
                    from datetime import datetime
                    current_time = datetime.now().strftime('%H:%M')
                    
                    for item in news_items:
                        item['time'] = current_time
                        item['_dt'] = datetime.now()
                        item['_source'] = source_name
                        item['link'] = item.get('url', '#')
                        
                    print(f"✅ {source_name}から{len(news_items)}件のニュース取得成功")
                    return news_items
                    
            except Exception as e:
                print(f"[WARN] Failed to parse Gemini response for {source_name}: {e}")
        
        return []
    
    def fetch_trending_topics(self) -> List[Dict]:
        """
        Gemini APIを使って現在のAI業界トレンドトピックを取得
        """
        if not self.analyzer.enabled:
            return []
        
        print("🤖 Gemini APIで最新トレンドを分析中...")
        
        prompt = """
AI業界の専門家として、今日の最も重要なAIトレンドを教えてください。

以下の形式でJSON配列として返してください：
[
  {
    "title": "トレンドタイトル（英語）",
    "title_ja": "トレンドタイトル（日本語）",
    "summary": "詳細説明（英語、100文字程度）",
    "category": "breakthrough/business/regulatory/social/technicalのいずれか",
    "importance": 1-10の重要度スコア,
    "keywords": ["キーワード1", "キーワード2", "キーワード3"]
  }
]

最新のトレンドを5つ程度、重要度順に教えてください。
2025年8月の最新動向を反映してください。

JSON形式のみを返してください。
"""
        
        response = self.analyzer._make_request(prompt)
        
        if response:
            try:
                import re
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    trends = json.loads(json_match.group())
                    
                    from datetime import datetime
                    for trend in trends:
                        trend['source'] = 'Gemini AI Trends'
                        trend['time'] = datetime.now().strftime('%H:%M')
                        trend['_dt'] = datetime.now()
                        trend['link'] = '#'
                        
                    print(f"✅ {len(trends)}件のトレンド取得成功")
                    return trends
                    
            except Exception as e:
                print(f"[WARN] Failed to parse trending topics: {e}")
        
        return []
    
    def supplement_403_sources(self, failed_sources: List[str]) -> Dict[str, List[Dict]]:
        """
        403エラーになったソースの代替情報をGemini APIで補完
        
        Args:
            failed_sources: 失敗したソースのリスト
            
        Returns:
            ソース名をキーとするニュース辞書
        """
        supplemented_data = {}
        
        if not self.analyzer.enabled:
            return supplemented_data
        
        for source in failed_sources:
            if '403' in source or 'Google News' in source:
                # Google Newsなど問題のあるソースを特定
                if 'Google News' in source:
                    # カテゴリに応じて異なるプロンプトを使用
                    if 'AI企業・投資' in source or '日本' in source:
                        news = self.fetch_from_problematic_source(
                            url='https://news.google.com/topics/ai',
                            source_name='Google News AI (Gemini補完)'
                        )
                    elif 'AIツール' in source:
                        news = self.fetch_from_problematic_source(
                            url='https://news.google.com/topics/ai-tools',
                            source_name='Google News Tools (Gemini補完)'
                        )
                    else:
                        news = self.fetch_from_problematic_source(
                            url='https://news.google.com/topics/ai-research',
                            source_name='Google News Research (Gemini補完)'
                        )
                    
                    if news:
                        supplemented_data[source] = news
        
        return supplemented_data

def integrate_with_build_py():
    """
    build.pyやgenerate_comprehensive_dashboard.pyに統合するための関数
    """
    fetcher = GeminiWebFetcher()
    
    # 403エラーソースの代替データ取得
    failed_sources = [
        'Google News: AI企業・投資 (日本語)',
        'Google News: AIツール・フレームワーク',
        'Google News: AI論文・研究'
    ]
    
    supplemented = fetcher.supplement_403_sources(failed_sources)
    
    # トレンド情報も取得
    trends = fetcher.fetch_trending_topics()
    
    return supplemented, trends

if __name__ == "__main__":
    # テスト実行
    from dotenv import load_dotenv
    load_dotenv()
    
    fetcher = GeminiWebFetcher()
    
    if fetcher.analyzer.enabled:
        print("\n📊 403エラーソースの代替取得テスト...")
        
        # Google Newsの代替を取得
        news = fetcher.fetch_from_problematic_source(
            url='https://news.google.com/rss/topics/ai',
            source_name='Google News AI'
        )
        
        if news:
            print(f"\n✅ 取得成功: {len(news)}件のニュース")
            for item in news[:3]:
                print(f"  - {item['title_ja'][:50]}...")
                print(f"    重要度: {item.get('importance', 0)}")
        
        # トレンド取得テスト
        print("\n🔥 トレンド取得テスト...")
        trends = fetcher.fetch_trending_topics()
        
        if trends:
            print(f"\n✅ トレンド取得成功: {len(trends)}件")
            for trend in trends[:3]:
                print(f"  - {trend['title_ja'][:50]}...")
                print(f"    カテゴリ: {trend.get('category', 'N/A')}")
    else:
        print("❌ Gemini APIが設定されていません")