#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Set environment
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '24'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'

print("🚀 AIニュースダッシュボード生成開始...")

try:
    # Import and run dashboard generation
    import generate_dashboard
    
    print("📊 ダッシュボードデータを分析中...")
    dashboard_data = generate_dashboard.analyze_ai_news()
    
    print("🎨 HTMLダッシュボードを生成中...")
    html_content = generate_dashboard.generate_dashboard_html(dashboard_data)
    
    # Save files
    dashboard_path = Path("ai_news_dashboard.html")
    dashboard_path.write_text(html_content, encoding='utf-8')
    
    json_path = Path("dashboard_data.json")
    import json
    json_path.write_text(json.dumps(dashboard_data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print("✅ ダッシュボード生成完了!")
    print(f"📁 ファイル: {dashboard_path.absolute()}")
    print(f"📄 データ: {json_path.absolute()}")
    print("\n🌐 ブラウザで ai_news_dashboard.html を開いてダッシュボードを確認してください!")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()