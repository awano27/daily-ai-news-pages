#!/usr/bin/env python3
import subprocess
import sys
import os

def test_improved_ui():
    """改善版UIをテスト実行"""
    print("🎨 改善版UI/UXダッシュボードテスト実行中...")
    
    try:
        # カレントディレクトリを設定
        os.chdir(r"C:\Users\yoshitaka\daily-ai-news")
        
        # Python実行
        result = subprocess.run([
            sys.executable, 
            "generate_improved_ui_dashboard.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 実行成功")
            if result.stdout:
                print(f"📋 出力: {result.stdout}")
        else:
            print(f"❌ 実行失敗: {result.stderr}")
            
        # 生成されたファイルの確認
        if os.path.exists("index_improved.html"):
            size = os.path.getsize("index_improved.html")
            print(f"📄 index_improved.html 生成完了 ({size:,} bytes)")
            
            # 最初の500文字を表示
            with open("index_improved.html", "r", encoding="utf-8") as f:
                content = f.read()[:500]
                print(f"📝 内容プレビュー:\n{content}...")
        else:
            print("❌ index_improved.html が生成されませんでした")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    test_improved_ui()
    input("Press Enter to exit...")