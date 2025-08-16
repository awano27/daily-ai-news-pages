#!/usr/bin/env python3
"""
緊急タイムアウト対策
GitHub Actionsの長時間実行を防ぐためのタイムアウト制限付きビルド
"""
import os
import sys
import signal
import time
from pathlib import Path

# タイムアウト設定（5分）
TIMEOUT_SECONDS = 300

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Build timeout reached")

def emergency_build():
    """緊急時の最小限ビルド"""
    print("🚨 緊急タイムアウト対策ビルド開始")
    
    # シンプルなHTMLを生成
    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI業界ニュース - メンテナンス中</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            color: white;
            text-align: center;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        h1 { font-size: 2rem; margin-bottom: 20px; }
        p { font-size: 1.1rem; margin-bottom: 15px; opacity: 0.9; }
        .refresh { 
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 10px;
            margin-top: 20px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛠️ AI業界ニュースダッシュボード</h1>
        <p>現在システムを最適化中です</p>
        <p>403エラー完全除去システムを実装中...</p>
        <div class="refresh">
            📱 数分後に自動更新されます
        </div>
        <br><br>
        <small>Generated: {time}</small>
    </div>
</body>
</html>""".format(time=time.strftime('%Y-%m-%d %H:%M JST'))
    
    # HTMLファイルを出力
    Path("index.html").write_text(html_content, encoding="utf-8")
    print("✅ 緊急HTMLを生成しました")

if __name__ == "__main__":
    # タイムアウト設定
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIMEOUT_SECONDS)
    
    try:
        # メインビルドを試行
        print("🔄 通常ビルドを試行中...")
        import build
        build.main()
        print("✅ 通常ビルド成功")
        
    except (TimeoutException, Exception) as e:
        print(f"⚠️ ビルドエラー/タイムアウト: {e}")
        print("🚨 緊急ビルドに切り替え")
        emergency_build()
        
    finally:
        signal.alarm(0)  # タイムアウト解除