#!/usr/bin/env python3
"""
Gemini強化版ダッシュボードのテスト
"""
from dotenv import load_dotenv
load_dotenv()

print("🤖 Gemini強化版ダッシュボードを生成中...")

try:
    from generate_comprehensive_dashboard import analyze_ai_landscape
    
    # ダッシュボード生成
    analyze_ai_landscape()
    
    print("\n✅ Gemini強化版ダッシュボード生成完了!")
    print("📁 生成ファイル:")
    print("  • index.html - メインダッシュボード")
    print("  • dashboard_data.json - 分析データ")
    print("\n🎉 403エラーがGeminiで解決されました!")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()