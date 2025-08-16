#!/usr/bin/env python3
"""
Gemini API を使用した高度なAIニュース分析・評価・選択システム
"""
import os
import json
import time
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

class GeminiAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Gemini APIクライアントを初期化
        
        Args:
            api_key: Gemini API キー (環境変数 GEMINI_API_KEY からも取得可能)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        # 最新のGemini 2.5モデルを使用 (2025年8月時点の最新安定版)
        # gemini-2.5-flash: 最新の安定版（推奨）
        # gemini-2.5-flash-lite: 低レイテンシ/高スループット版
        # gemini-2.5-pro: 高度な推論用
        self.model = "gemini-2.5-flash"  # 最新の安定版モデル
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        if not self.api_key:
            print("⚠️ Gemini API key not found. Set GEMINI_API_KEY environment variable.")
            self.enabled = False
        else:
            self.enabled = True
            print(f"✅ Gemini API initialized successfully with model: {self.model}")
    
    def _make_request(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Gemini APIへのリクエストを実行"""
        if not self.enabled:
            return None
        
        for attempt in range(max_retries):
            try:
                headers = {
                    'Content-Type': 'application/json',
                }
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.3,
                        "topK": 40,
                        "topP": 0.95,
                        "maxOutputTokens": 2048
                    }
                }
                
                url = f"{self.base_url}?key={self.api_key}"
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result and len(result['candidates']) > 0:
                        candidate = result['candidates'][0]
                        
                        # 標準的なGemini 1.5レスポンス形式
                        if 'content' in candidate and 'parts' in candidate['content']:
                            parts = candidate['content']['parts']
                            if len(parts) > 0 and 'text' in parts[0]:
                                return parts[0]['text'].strip()
                        
                        # エラーケースの詳細ログ
                        finish_reason = candidate.get('finishReason', 'UNKNOWN')
                        print(f"[WARN] Gemini response issue - finishReason: {finish_reason}")
                        if finish_reason == 'MAX_TOKENS':
                            print(f"[WARN] Response truncated due to token limit")
                        return None
                else:
                    error_text = response.text if hasattr(response, 'text') else 'Unknown error'
                    print(f"[WARN] Gemini API failed: {response.status_code} - {error_text[:200]}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        
            except Exception as e:
                print(f"[WARN] Gemini API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        return None
    
    def analyze_news_importance(self, news_items: List[Dict]) -> List[Dict]:
        """
        ニュース項目の重要度をGeminiで分析・評価
        
        Args:
            news_items: ニュース項目のリスト
            
        Returns:
            重要度スコア付きのニュース項目リスト
        """
        if not self.enabled:
            print("⚠️ Gemini API not available, using fallback scoring")
            return self._fallback_scoring(news_items)
        
        print("🤖 Gemini APIでニュース重要度を分析中...")
        
        enhanced_items = []
        
        for item in news_items[:20]:  # 最大20件まで分析
            try:
                prompt = f"""
AI業界のニュース分析エキスパートとして、以下のニュースの重要度を評価してください。

タイトル: {item.get('title', '')}
要約: {item.get('summary', item.get('_summary', ''))}
ソース: {item.get('source', item.get('_source', ''))}

以下の観点から総合的に評価し、1-100の重要度スコアを付けてください：

1. 技術的革新性 (breakthrough, 新技術, 新製品リリース)
2. 市場への影響度 (投資, M&A, IPO, 規制)
3. 業界への影響度 (主要企業の動向, パートナーシップ)
4. 緊急性・時効性 (速報性, トレンド性)
5. 社会的影響度 (倫理, 雇用, 社会問題)

レスポンス形式:
スコア: [1-100の数値]
理由: [評価理由を1-2文で簡潔に]
カテゴリ: [breakthrough/business/regulatory/social/technicalのいずれか]
キーワード: [重要なキーワード3つをカンマ区切り]
"""
                
                response = self._make_request(prompt)
                if response:
                    # レスポンスをパース
                    score, reason, category, keywords = self._parse_analysis_response(response)
                    
                    enhanced_item = item.copy()
                    enhanced_item.update({
                        'gemini_score': score,
                        'gemini_reason': reason,
                        'gemini_category': category,
                        'gemini_keywords': keywords,
                        'final_importance': max(score, item.get('importance', 0))
                    })
                    enhanced_items.append(enhanced_item)
                    
                    print(f"  ✅ {item.get('title', '')[:50]}... -> Score: {score}")
                    
                    # API rate limit対策
                    time.sleep(0.5)
                else:
                    # Gemini API失敗時はフォールバック
                    enhanced_items.append(item)
                    
            except Exception as e:
                print(f"[WARN] Gemini analysis failed for item: {e}")
                enhanced_items.append(item)
        
        # 残りのアイテムはそのまま追加
        enhanced_items.extend(news_items[20:])
        
        # Geminiスコアでソート
        enhanced_items.sort(key=lambda x: x.get('final_importance', x.get('gemini_score', x.get('importance', 0))), reverse=True)
        
        return enhanced_items
    
    def _parse_analysis_response(self, response: str) -> tuple:
        """Geminiのレスポンスをパースして構造化データに変換"""
        try:
            lines = response.strip().split('\n')
            score = 50  # デフォルト
            reason = "Gemini分析完了"
            category = "technical"
            keywords = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('スコア:') or line.startswith('Score:'):
                    try:
                        score_text = line.split(':')[1].strip()
                        score = int(''.join(filter(str.isdigit, score_text)))
                        score = max(1, min(100, score))  # 1-100の範囲に制限
                    except:
                        pass
                elif line.startswith('理由:') or line.startswith('Reason:'):
                    reason = line.split(':', 1)[1].strip()
                elif line.startswith('カテゴリ:') or line.startswith('Category:'):
                    category = line.split(':', 1)[1].strip().lower()
                elif line.startswith('キーワード:') or line.startswith('Keywords:'):
                    keywords_text = line.split(':', 1)[1].strip()
                    keywords = [k.strip() for k in keywords_text.split(',')][:3]
            
            return score, reason, category, keywords
            
        except Exception as e:
            print(f"[WARN] Failed to parse Gemini response: {e}")
            return 50, "分析完了", "technical", []
    
    def _fallback_scoring(self, news_items: List[Dict]) -> List[Dict]:
        """Gemini API利用不可時のフォールバック重要度算出"""
        for item in news_items:
            # 既存の重要度算出ロジックを使用
            item['final_importance'] = item.get('importance', 0)
        
        return news_items
    
    def generate_market_insights(self, news_data: Dict) -> Dict:
        """
        市場動向の洞察をGeminiで生成
        """
        if not self.enabled:
            return self._fallback_market_insights(news_data)
        
        print("🤖 Geminiで市場洞察を生成中...")
        
        # 主要ニュースを抽出
        key_news = []
        for category in news_data.get('categories', {}).values():
            key_news.extend(category.get('featured_topics', [])[:3])
        
        news_summary = "\n".join([
            f"- {item.get('title_ja', item.get('title', ''))} ({item.get('source', '')})"
            for item in key_news[:10]
        ])
        
        prompt = f"""
AI業界の市場アナリストとして、今日のニュースから市場動向を分析してください。

主要ニュース:
{news_summary}

以下の観点から分析してください:
1. 市場センチメント (楽観的/中立/慎重)
2. 注目すべき投資動向
3. 技術トレンド
4. 主要企業の動向
5. 今後の予測

レスポンス形式 (JSON):
{{
  "market_sentiment": "楽観的/中立/慎重",
  "key_trends": ["トレンド1", "トレンド2", "トレンド3"],
  "investment_focus": ["投資分野1", "投資分野2"],
  "major_players": ["企業1", "企業2", "企業3"],
  "outlook": "短期的な見通し"
}}
"""
        
        response = self._make_request(prompt)
        if response:
            try:
                # JSONレスポンスをパース
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    insights = json.loads(json_match.group())
                    return insights
            except Exception as e:
                print(f"[WARN] Failed to parse Gemini market insights: {e}")
        
        return self._fallback_market_insights(news_data)
    
    def _fallback_market_insights(self, news_data: Dict) -> Dict:
        """フォールバック市場洞察"""
        return {
            "market_sentiment": "中立",
            "key_trends": ["生成AI", "企業AI導入", "オープンソース"],
            "investment_focus": ["AI インフラ", "エッジAI"],
            "major_players": ["OpenAI", "Google", "Microsoft"],
            "outlook": "継続的な成長が期待される"
        }
    
    def enhance_executive_summary(self, dashboard_data: Dict) -> Dict:
        """
        エグゼクティブサマリーをGeminiで強化
        """
        if not self.enabled:
            return dashboard_data.get('executive_summary', {})
        
        print("🤖 Geminiでエグゼクティブサマリーを強化中...")
        
        stats = dashboard_data.get('stats', {})
        market = dashboard_data.get('market_insights', {})
        
        prompt = f"""
AI業界のエグゼクティブ向けに、今日の業界動向の要約を作成してください。

データ:
- 総ニュース数: {stats.get('total_items', 0)}件
- 活動企業数: {stats.get('active_companies', 0)}社
- 市場センチメント: {market.get('market_sentiment', '中立')}
- 主要企業: {market.get('major_players', [])}

3つのキーポイントを簡潔にまとめてください:

レスポンス形式:
1. [第1のポイント]
2. [第2のポイント]
3. [第3のポイント]

今日の最重要トピック: [1つのトピック]
明日への注目点: [1つの注目点]
"""
        
        response = self._make_request(prompt)
        if response:
            lines = response.strip().split('\n')
            key_points = []
            important_topic = ""
            tomorrow_focus = ""
            
            for line in lines:
                if line.strip().startswith(('1.', '2.', '3.')):
                    key_points.append(line.strip())
                elif '最重要トピック:' in line:
                    important_topic = line.split(':', 1)[1].strip()
                elif '明日への注目点:' in line:
                    tomorrow_focus = line.split(':', 1)[1].strip()
            
            return {
                'headline': f"今日のAI業界: {stats.get('total_items', 0)}件のニュース分析",
                'key_points': key_points or ["市場動向を継続監視", "技術革新が加速", "企業投資が活発"],
                'important_topic': important_topic,
                'tomorrow_focus': tomorrow_focus,
                'outlook': market.get('outlook', '安定した成長期')
            }
        
        return dashboard_data.get('executive_summary', {})

# 使用例とテスト
if __name__ == "__main__":
    analyzer = GeminiAnalyzer()
    
    # テストニュース
    test_news = [
        {
            'title': 'OpenAI announces GPT-5 with revolutionary capabilities',
            'summary': 'OpenAI has unveiled GPT-5, featuring unprecedented reasoning abilities...',
            'source': 'TechCrunch',
            'importance': 70
        }
    ]
    
    if analyzer.enabled:
        print("🧪 Gemini分析をテスト中...")
        enhanced = analyzer.analyze_news_importance(test_news)
        print(f"Enhanced news: {enhanced[0]}")
    else:
        print("⚠️ Gemini API not configured for testing")