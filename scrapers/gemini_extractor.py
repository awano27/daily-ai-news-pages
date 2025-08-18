#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini AI コンテンツ抽出器
高性能なAI分析によるコンテンツ要約・構造化
"""

import os
import google.generativeai as genai
import time
from typing import Dict, Any, List
import json

class GeminiExtractor:
    """Gemini APIベースのコンテンツ抽出器"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.0-flash"):
        """
        初期化
        
        Args:
            api_key: Gemini APIキー (.envから自動取得)
            model: 使用モデル名
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model_name = model
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEYが設定されていません")
        
        # Gemini API設定
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        print(f"✅ Gemini AI初期化完了: {self.model_name}")
    
    def extract(self, content: str, extraction_type: str = "summary") -> Dict[str, Any]:
        """
        コンテンツからの情報抽出
        
        Args:
            content: 抽出対象コンテンツ
            extraction_type: 抽出タイプ (summary, keywords, structure, analysis)
            
        Returns:
            抽出結果辞書
        """
        print(f"🤖 Gemini抽出開始: {extraction_type}")
        
        try:
            if extraction_type == "summary":
                return self._extract_summary(content)
            elif extraction_type == "keywords":
                return self._extract_keywords(content)
            elif extraction_type == "structure":
                return self._extract_structure(content)
            elif extraction_type == "analysis":
                return self._extract_analysis(content)
            else:
                return self._extract_custom(content, extraction_type)
                
        except Exception as e:
            print(f"❌ Gemini抽出エラー: {e}")
            return {
                'success': False,
                'error': str(e),
                'extraction_type': extraction_type
            }
    
    def _extract_summary(self, content: str) -> Dict[str, Any]:
        """要約抽出"""
        prompt = f"""
以下のWebコンテンツを分析し、JSON形式で要約してください：

【分析対象】
{content[:3000]}

【出力形式】
{{
    "title": "適切なタイトル",
    "summary": "3-5文での要約",
    "key_points": ["重要ポイント1", "重要ポイント2", "重要ポイント3"],
    "category": "コンテンツカテゴリ",
    "language": "ja/en",
    "confidence": 0.9
}}

日本語で回答してください。
"""
        
        result = self._call_gemini(prompt)
        
        try:
            # JSON解析を試行
            json_result = json.loads(result)
            json_result['success'] = True
            json_result['extraction_type'] = 'summary'
            return json_result
        except json.JSONDecodeError:
            # JSON解析失敗時はテキストとして返す
            return {
                'success': True,
                'extraction_type': 'summary',
                'raw_response': result,
                'summary': result[:500]
            }
    
    def _extract_keywords(self, content: str) -> Dict[str, Any]:
        """キーワード抽出"""
        prompt = f"""
以下のコンテンツから重要なキーワードを抽出してJSON形式で出力してください：

【コンテンツ】
{content[:2000]}

【出力形式】
{{
    "primary_keywords": ["最重要キーワード1", "最重要キーワード2"],
    "secondary_keywords": ["関連キーワード1", "関連キーワード2", "関連キーワード3"],
    "entities": ["人名/会社名/製品名など"],
    "topics": ["主要トピック1", "主要トピック2"],
    "relevance_score": 0.8
}}
"""
        
        result = self._call_gemini(prompt)
        
        try:
            json_result = json.loads(result)
            json_result['success'] = True
            json_result['extraction_type'] = 'keywords'
            return json_result
        except json.JSONDecodeError:
            return {
                'success': True,
                'extraction_type': 'keywords',
                'raw_response': result
            }
    
    def _extract_structure(self, content: str) -> Dict[str, Any]:
        """構造化データ抽出"""
        prompt = f"""
以下のコンテンツの構造を分析し、JSON形式で出力してください：

【コンテンツ】
{content[:2000]}

【出力形式】
{{
    "document_type": "記事/ブログ/ニュース/商品ページ等",
    "sections": [
        {{"section": "セクション名", "content": "セクション内容要約"}},
        {{"section": "セクション名", "content": "セクション内容要約"}}
    ],
    "metadata": {{
        "author": "著者名（もしあれば）",
        "date": "日付（もしあれば）",
        "source": "情報源"
    }},
    "readability": "易しい/普通/難しい"
}}
"""
        
        result = self._call_gemini(prompt)
        
        try:
            json_result = json.loads(result)
            json_result['success'] = True
            json_result['extraction_type'] = 'structure'
            return json_result
        except json.JSONDecodeError:
            return {
                'success': True,
                'extraction_type': 'structure',
                'raw_response': result
            }
    
    def _extract_analysis(self, content: str) -> Dict[str, Any]:
        """詳細分析"""
        prompt = f"""
以下のコンテンツを詳細に分析し、ビジネス価値の観点からJSON形式で評価してください：

【コンテンツ】
{content[:2500]}

【出力形式】
{{
    "business_value": {{
        "relevance": "ビジネス関連性（高/中/低）",
        "actionability": "実行可能性の評価",
        "impact": "インパクトの大きさ"
    }},
    "content_quality": {{
        "credibility": "信頼性評価",
        "completeness": "情報の完全性",
        "timeliness": "情報の新しさ"
    }},
    "insights": ["洞察1", "洞察2", "洞察3"],
    "recommendations": ["推奨アクション1", "推奨アクション2"],
    "overall_score": 0.8
}}

日本語で分析してください。
"""
        
        result = self._call_gemini(prompt)
        
        try:
            json_result = json.loads(result)
            json_result['success'] = True
            json_result['extraction_type'] = 'analysis'
            return json_result
        except json.JSONDecodeError:
            return {
                'success': True,
                'extraction_type': 'analysis',
                'raw_response': result
            }
    
    def _extract_custom(self, content: str, custom_prompt: str) -> Dict[str, Any]:
        """カスタム抽出"""
        prompt = f"""
{custom_prompt}

【対象コンテンツ】
{content[:2000]}
"""
        
        result = self._call_gemini(prompt)
        
        return {
            'success': True,
            'extraction_type': 'custom',
            'custom_prompt': custom_prompt,
            'result': result
        }
    
    def _call_gemini(self, prompt: str) -> str:
        """Gemini API呼び出し"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API呼び出しエラー: {e}")
    
    def summarize(self, content: str, length: str = "medium") -> str:
        """簡易要約（レガシーメソッド）"""
        length_map = {
            "short": "1-2文で簡潔に",
            "medium": "3-5文で",
            "long": "詳細に（10文程度）"
        }
        
        length_instruction = length_map.get(length, "3-5文で")
        
        prompt = f"""
以下のコンテンツを{length_instruction}要約してください：

{content[:2000]}

日本語で自然な文章として回答してください。
"""
        
        try:
            return self._call_gemini(prompt)
        except Exception as e:
            return f"要約エラー: {e}"
    
    def batch_extract(self, contents: List[str], extraction_type: str = "summary") -> List[Dict[str, Any]]:
        """バッチ処理"""
        results = []
        
        print(f"🤖 Geminiバッチ処理開始: {len(contents)}件")
        
        for i, content in enumerate(contents, 1):
            print(f"進行状況: {i}/{len(contents)}")
            result = self.extract(content, extraction_type)
            results.append(result)
            
            # API レート制限対応
            time.sleep(1)
        
        print(f"✅ Geminiバッチ処理完了")
        return results

# 使用例
if __name__ == "__main__":
    try:
        extractor = GeminiExtractor()
        
        # テストコンテンツ
        test_content = "人工知能（AI）の発展により、様々な分野で革新的な変化が起きています。特に自然言語処理の分野では、大規模言語モデルが注目を集めています。"
        
        # 要約抽出テスト
        result = extractor.extract(test_content, "summary")
        print("要約結果:", result)
        
    except Exception as e:
        print(f"テストエラー: {e}")