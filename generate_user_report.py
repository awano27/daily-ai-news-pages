#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ユーザー向けサマリーレポート生成
JSONデータを分かりやすい日本語レポートに変換
"""

import json
import os
from datetime import datetime
from pathlib import Path

def generate_user_summary(analysis_file: str):
    """ユーザー向けサマリー生成"""
    
    # 分析結果読み込み
    with open(analysis_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # サマリー情報取得
    summary_file = analysis_file.replace('comprehensive_analysis_', 'analysis_summary_')
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary = json.load(f)
    else:
        summary = {}
    
    # レポート生成
    timestamp = datetime.now().strftime('%Y年%m月%d日 %H時%M分')
    
    report = f"""
# 🚀 AI業界インテリジェンス・レポート
**生成日時**: {timestamp}

## 📊 実行結果サマリー

- **📈 総処理件数**: {summary.get('total_processed', 0)}件
- **✅ 成功取得件数**: {summary.get('total_successful', 0)}件  
- **📊 成功率**: {summary.get('success_rate', '0%')}
- **🏷️ 分析カテゴリ数**: {len(data)}個
- **🤖 AI分析タイプ**: {', '.join(summary.get('analysis_types', []))}

---

## 🎯 カテゴリ別結果

"""
    
    # カテゴリ名と説明
    category_info = {
        'ai_breaking_news': {
            'name': '🔥 AI最新ニュース',
            'description': 'TechCrunch、VentureBeat等からの最新AI関連ニュース'
        },
        'ai_research_labs': {
            'name': '🧪 AI研究ラボ',
            'description': 'OpenAI、Google AI、Anthropic等の研究機関ブログ'
        },
        'business_startup': {
            'name': '💼 ビジネス・スタートアップ',
            'description': 'スタートアップ投資、企業動向、ビジネストレンド'
        },
        'tech_innovation': {
            'name': '⚡ 技術革新',
            'description': '最新テクノロジー、プロダクト、イノベーション情報'
        },
        'policy_regulation': {
            'name': '📜 政策・規制',
            'description': 'AI関連の政策、規制、法的動向'
        },
        'academic_research': {
            'name': '🎓 学術研究',
            'description': 'arXiv論文、学術機関の研究成果'
        }
    }
    
    # 重要トピック抽出
    all_topics = []
    top_articles = []
    
    for category, articles in data.items():
        if not articles:
            continue
            
        cat_info = category_info.get(category, {'name': category, 'description': ''})
        report += f"""
### {cat_info['name']} ({len(articles)}件取得)
*{cat_info['description']}*

"""
        
        for i, article in enumerate(articles[:3], 1):  # 上位3件のみ表示
            basic = article.get('basic', {})
            ai_analysis = article.get('ai_analysis', {})
            
            title = basic.get('title', 'タイトル不明')[:80]
            url = basic.get('url', '#')
            
            # AI要約取得
            summary_text = "要約なし"
            if 'summary' in ai_analysis and ai_analysis['summary'].get('success'):
                summary_data = ai_analysis['summary']
                if 'summary' in summary_data:
                    summary_text = summary_data['summary'][:150]
                elif 'raw_response' in summary_data:
                    summary_text = summary_data['raw_response'][:150]
            
            # キーワード取得
            keywords = []
            if 'keywords' in ai_analysis and ai_analysis['keywords'].get('success'):
                keywords_data = ai_analysis['keywords']
                if 'primary_keywords' in keywords_data:
                    keywords = keywords_data['primary_keywords'][:3]
            
            report += f"""
**{i}. {title}**
- 📝 **要約**: {summary_text}...
- 🏷️ **キーワード**: {', '.join(keywords) if keywords else 'なし'}
- 🔗 **URL**: {url}

"""
            
            # トップ記事収集（後でランキング用）
            content_stats = article.get('content_stats', {})
            char_count = content_stats.get('character_count', 0)
            if char_count > 1000:  # 充実したコンテンツ
                top_articles.append({
                    'title': title,
                    'summary': summary_text,
                    'keywords': keywords,
                    'category': cat_info['name'],
                    'url': url,
                    'char_count': char_count
                })
    
    # トレンドキーワード分析
    report += """
---

## 🔍 注目トレンド・キーワード

"""
    
    keyword_count = {}
    for category, articles in data.items():
        for article in articles:
            ai_analysis = article.get('ai_analysis', {})
            if 'keywords' in ai_analysis and ai_analysis['keywords'].get('success'):
                keywords_data = ai_analysis['keywords']
                if 'primary_keywords' in keywords_data:
                    for keyword in keywords_data['primary_keywords']:
                        keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
    
    # 上位キーワード
    top_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for i, (keyword, count) in enumerate(top_keywords, 1):
        report += f"**{i}.** {keyword} ({count}回言及)\n"
    
    # 重要記事ランキング
    report += """

---

## 🏆 注目記事ランキング（コンテンツ充実度順）

"""
    
    top_articles.sort(key=lambda x: x['char_count'], reverse=True)
    
    for i, article in enumerate(top_articles[:5], 1):
        report += f"""
### {i}位: {article['title']}
- **カテゴリ**: {article['category']}
- **要約**: {article['summary']}...
- **キーワード**: {', '.join(article['keywords']) if article['keywords'] else 'なし'}
- **文字数**: {article['char_count']:,}文字
- **URL**: {article['url']}

"""
    
    # 技術動向分析
    report += """
---

## 🚀 今週の技術動向

### 🤖 AI技術進化
"""
    
    ai_topics = []
    for category, articles in data.items():
        for article in articles:
            title = article.get('basic', {}).get('title', '')
            if any(keyword in title.lower() for keyword in ['gpt', 'claude', 'gemini', 'llm', 'ai model']):
                ai_topics.append(title)
    
    for topic in ai_topics[:5]:
        report += f"- {topic}\n"
    
    report += """
### 💼 ビジネス・投資動向
"""
    
    business_topics = []
    for category, articles in data.items():
        if category == 'business_startup':
            for article in articles:
                title = article.get('basic', {}).get('title', '')
                business_topics.append(title)
    
    for topic in business_topics[:5]:
        report += f"- {topic}\n"
    
    # アクションアイテム
    report += """

---

## 📋 推奨アクション

### 🎯 短期アクション（今週）
1. **AI技術動向の追跡**: GPT-5、Claude、Geminiの最新アップデートを確認
2. **規制動向の把握**: AI関連の新しい政策・規制情報をチェック
3. **競合分析**: 主要AI企業の戦略変更を分析

### 🚀 中長期アクション（来月）
1. **技術導入検討**: 新しいAIツール・プラットフォームの評価
2. **人材戦略見直し**: AI関連スキルの社内育成計画
3. **パートナーシップ**: AI企業との協業機会の探索

---

## 📞 お問い合わせ

このレポートに関するご質問・ご要望は、システム管理者までお問い合わせください。

**次回更新予定**: 24時間後（自動実行）

---
*このレポートは Free Scraping Platform により自動生成されました*
"""
    
    return report

def main():
    """メイン実行"""
    # 最新の分析ファイルを検索
    analysis_files = list(Path('.').glob('comprehensive_analysis_*.json'))
    
    if not analysis_files:
        print("❌ 分析ファイルが見つかりません")
        print("先に python run_comprehensive_analysis.py を実行してください")
        return
    
    # 最新ファイルを使用
    latest_file = max(analysis_files, key=lambda f: f.stat().st_mtime)
    print(f"📊 分析ファイル: {latest_file}")
    
    # レポート生成
    report = generate_user_summary(str(latest_file))
    
    # ファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Markdownファイル
    md_file = f"user_summary_report_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # テキストファイル
    txt_file = f"user_summary_report_{timestamp}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ ユーザーレポート生成完了:")
    print(f"   📄 Markdown: {md_file}")
    print(f"   📄 テキスト: {txt_file}")
    
    # 要約表示
    print("\n" + "="*60)
    print("📋 レポートサマリー")
    print("="*60)
    print(report[:1000] + "...")
    print("\n詳細は生成されたファイルをご確認ください。")

if __name__ == "__main__":
    main()