#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ダッシュボードをメインページ（index.html）に、詳細ニュースをサブページに変更
"""
import shutil
from pathlib import Path

def swap_pages():
    """ページの役割を入れ替える"""
    
    print("🔄 ページ構造を変更中...")
    
    # 1. 現在のファイルをバックアップ
    index_path = Path("index.html")
    dashboard_path = Path("ai_news_dashboard.html")
    
    if index_path.exists():
        shutil.copy2(index_path, "news_detail.html")
        print("✅ 現在のindex.html → news_detail.html に移動")
    
    if dashboard_path.exists():
        shutil.copy2(dashboard_path, "index_new.html")
        print("✅ ダッシュボード → index_new.html として準備")
    
    # 2. ナビゲーションリンクを更新
    
    # news_detail.html のリンクを更新（ダッシュボードへ戻る）
    if Path("news_detail.html").exists():
        with open("news_detail.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # ダッシュボードリンクをホームに変更
        content = content.replace(
            '<a href="ai_news_dashboard.html" class="nav-link">📊 ダッシュボード</a>',
            '<a href="index.html" class="nav-link">📊 ダッシュボードへ戻る</a>'
        )
        
        with open("news_detail.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ news_detail.html のナビゲーション更新")
    
    # index_new.html のリンクを更新（詳細ページへ）
    if Path("index_new.html").exists():
        with open("index_new.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # フッターに詳細ページへのリンクを追加
        content = content.replace(
            '</div>\n</body>',
            '''        </div>
        
        <!-- 詳細ニュースへのCTA -->
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin-top: 30px;">
            <h2 style="color: white; margin-bottom: 15px;">📰 詳細なニュース記事を確認</h2>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 20px;">
                各カテゴリの全記事、要約、ソースリンクは詳細ページでご覧いただけます
            </p>
            <a href="news_detail.html" style="
                display: inline-block;
                padding: 12px 30px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                font-size: 1.1rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                📄 詳細ニュース一覧へ →
            </a>
        </div>
    </div>
</body>'''
        )
        
        # ヘッダーも修正
        content = content.replace(
            '<h1>🌏 AI業界全体像ダッシュボード</h1>',
            '<h1>🌏 Daily AI News - 業界全体像ダッシュボード</h1>'
        )
        
        with open("index_new.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ index_new.html に詳細ページへのリンク追加")
    
    # 3. build.pyを更新して出力先を変更
    build_path = Path("build.py")
    if build_path.exists():
        with open(build_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # index.html → news_detail.html に出力先を変更
        content = content.replace(
            'Path("index.html").write_text(html_out, encoding="utf-8")',
            'Path("news_detail.html").write_text(html_out, encoding="utf-8")'
        )
        
        with open(build_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ build.py の出力先を news_detail.html に変更")
    
    # 4. generate_comprehensive_dashboard.py を更新
    gen_path = Path("generate_comprehensive_dashboard.py")
    if gen_path.exists():
        with open(gen_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # ai_news_dashboard.html → index.html に出力先を変更
        content = content.replace(
            'dashboard_path = Path("ai_news_dashboard.html")',
            'dashboard_path = Path("index.html")'
        )
        
        with open(gen_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ generate_comprehensive_dashboard.py の出力先を index.html に変更")
    
    # 5. 最終的なファイル配置
    if Path("index_new.html").exists():
        shutil.move("index_new.html", "index.html")
        print("✅ 新しいダッシュボードを index.html として設定")
    
    print("\n🎯 ページ構造の変更完了！")
    print("  📊 index.html: ダッシュボード（最初のランディングページ）")
    print("  📄 news_detail.html: 詳細ニュース一覧")
    
    return True

def update_github_workflow():
    """GitHub Actions ワークフローを更新"""
    
    workflow_path = Path(".github/workflows/build.yml")
    if not workflow_path.exists():
        print("⚠️ GitHub Actions ワークフローが見つかりません")
        return False
    
    with open(workflow_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # ダッシュボード生成を追加
    if "generate_comprehensive_dashboard.py" not in content:
        content = content.replace(
            "python build.py",
            """python build.py
        python generate_comprehensive_dashboard.py"""
        )
        
        with open(workflow_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ GitHub Actions ワークフローを更新")
    
    return True

def main():
    print("=" * 60)
    print("🔄 サイト構造変更: ダッシュボード → メインページ")
    print("=" * 60)
    
    # ページを入れ替え
    if not swap_pages():
        print("❌ ページの入れ替えに失敗しました")
        return False
    
    # GitHub Actions も更新
    update_github_workflow()
    
    print("\n" + "=" * 60)
    print("✅ サイト構造の変更完了!")
    print("=" * 60)
    print("\n📋 新しいサイト構造:")
    print("  1. index.html (ダッシュボード) - 最初に訪問")
    print("     ↓")
    print("  2. news_detail.html (詳細ニュース) - 詳細を確認")
    print("\n🚀 次のステップ:")
    print("  1. python generate_comprehensive_dashboard.py を実行")
    print("  2. git add .")
    print("  3. git commit -m 'feat: Dashboard as landing page'")
    print("  4. git push origin main")
    
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)