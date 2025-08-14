#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run AI News Dashboard Generator
"""
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 今日のAIニュースダッシュボードを生成します...")
    
    try:
        # ダッシュボード生成を実行
        result = subprocess.run([sys.executable, 'generate_dashboard.py'], 
                              capture_output=True, text=True, timeout=120)
        
        print("=" * 60)
        print("DASHBOARD GENERATION OUTPUT:")
        print("=" * 60)
        print(result.stdout)
        
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        # 生成されたファイルを確認
        dashboard_file = Path('ai_news_dashboard.html')
        json_file = Path('dashboard_data.json')
        
        if dashboard_file.exists():
            size = dashboard_file.stat().st_size
            print(f"\n✅ ダッシュボード生成成功!")
            print(f"📁 ファイル: {dashboard_file.name} ({size:,} bytes)")
            
            if json_file.exists():
                json_size = json_file.stat().st_size
                print(f"📊 データファイル: {json_file.name} ({json_size:,} bytes)")
            
            print(f"\n🌐 ブラウザで以下のファイルを開いてください:")
            print(f"   {dashboard_file.absolute()}")
            
            # ファイルの先頭を少し表示
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'AI News Dashboard' in content:
                    print("\n✅ ダッシュボードHTMLが正常に生成されました!")
                else:
                    print("\n⚠️ ダッシュボードHTMLに問題がある可能性があります")
            
        else:
            print("\n❌ ダッシュボードファイルが生成されませんでした")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ タイムアウト: ダッシュボード生成に時間がかかりすぎています")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()