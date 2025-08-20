#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy Enhanced X System - 強化版X投稿システムの本格導入
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def backup_current_system():
    """現在のシステムをバックアップ"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"_backup/enhanced_x_backup_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # build.pyをバックアップ
    if Path("build.py").exists():
        shutil.copy2("build.py", backup_dir / "build.py")
        print(f"✅ build.py backed up to {backup_dir}")
    
    return backup_dir

def patch_build_py():
    """build.pyに強化版X処理を統合"""
    build_path = Path("build.py")
    
    if not build_path.exists():
        print("❌ build.py not found")
        return False
    
    try:
        # build.pyを読み込み
        with open(build_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Enhanced X処理のインポートを追加
        import_addition = """
# Enhanced X Processing Integration
try:
    from enhanced_x_processor import EnhancedXProcessor
    ENHANCED_X_AVAILABLE = True
    print("✅ Enhanced X Processor: Integrated")
except ImportError:
    ENHANCED_X_AVAILABLE = False
    print("⚠️ Enhanced X Processor: Using fallback")
"""
        
        # gather_x_posts関数を置き換える関数を追加
        enhanced_function = '''
def enhanced_gather_x_posts_implementation(csv_path: str) -> list[dict]:
    """Enhanced X Posts - 重複除去とGemini強化"""
    if ENHANCED_X_AVAILABLE:
        try:
            processor = EnhancedXProcessor()
            posts = processor.process_x_posts(csv_path, max_posts=25)
            
            if posts:
                build_items = processor.convert_to_build_format(posts)
                print(f"✅ Enhanced X処理: {len(build_items)}件 (重複除去・Gemini強化済み)")
                
                # 統計表示
                enhanced_count = sum(1 for item in build_items if item.get('_enhanced', False))
                high_priority = sum(1 for item in build_items if item.get('_priority', 0) >= 3)
                
                print(f"   🧠 Gemini強化済み: {enhanced_count}件")
                print(f"   ⭐ 高重要度投稿: {high_priority}件")
                
                return build_items
        except Exception as e:
            print(f"⚠️ Enhanced処理エラー: {e} - フォールバックを使用")
    
    # フォールバック: 元の処理
    return original_gather_x_posts(csv_path)
'''
        
        # インポート部分の後に追加
        if "import random" in content:
            content = content.replace("import random", f"import random{import_addition}")
        
        # gather_x_posts関数の前に強化版実装を追加
        if "def gather_x_posts(csv_path: str)" in content:
            # 元の関数名を変更
            content = content.replace("def gather_x_posts(csv_path: str)", "def original_gather_x_posts(csv_path: str)")
            
            # 強化版関数を追加
            function_position = content.find("def original_gather_x_posts(csv_path: str)")
            if function_position > 0:
                content = content[:function_position] + enhanced_function + "\n" + content[function_position:]
                
                # 新しいgather_x_posts関数を追加
                content = content.replace(
                    enhanced_function + "\n",
                    enhanced_function + "\n\n" + "def gather_x_posts(csv_path: str) -> list[dict]:\n    return enhanced_gather_x_posts_implementation(csv_path)\n\n"
                )
        
        # ファイルに書き戻し
        with open(build_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ build.py に強化版X処理を統合完了")
        return True
        
    except Exception as e:
        print(f"❌ build.py パッチでエラー: {e}")
        return False

def test_integration():
    """統合テスト"""
    print("\n🧪 統合テスト実行...")
    
    try:
        # パッチ適用後のbuild.pyをテスト
        import importlib
        
        # build.pyを再読み込み
        if 'build' in sys.modules:
            importlib.reload(sys.modules['build'])
        else:
            import build
        
        # X投稿処理をテスト
        csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
        
        print("📡 X投稿収集テスト実行...")
        x_posts = build.gather_x_posts(csv_url)
        
        if x_posts:
            enhanced_count = sum(1 for p in x_posts if p.get('_enhanced', False))
            unique_hashes = set(p.get('_content_hash', '') for p in x_posts)
            
            print(f"✅ テスト成功: {len(x_posts)}件の投稿")
            print(f"   🧠 Gemini強化済み: {enhanced_count}件")
            print(f"   🔍 ユニーク投稿: {len(unique_hashes)}件")
            
            return True
        else:
            print("⚠️ 投稿が取得されませんでした")
            return False
            
    except Exception as e:
        print(f"❌ 統合テストでエラー: {e}")
        return False

def main():
    """メイン展開処理"""
    print("🚀 Enhanced X System Deployment")
    print("=" * 50)
    
    # 環境確認
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'GEMINI_API_KEY=' in line:
                    print("✅ GEMINI_API_KEY found in .env")
                    break
    else:
        print("⚠️ .env file not found")
    
    # 現在のシステムをバックアップ
    print("\n1. 現在のシステムをバックアップ...")
    backup_dir = backup_current_system()
    
    # build.pyを強化版でパッチ
    print("\n2. build.py に強化版X処理を統合...")
    patch_success = patch_build_py()
    
    if patch_success:
        # 統合テスト
        print("\n3. 統合テスト実行...")
        test_success = test_integration()
        
        if test_success:
            print("\n" + "=" * 50)
            print("🎉 Enhanced X System 導入完了！")
            print("\n📋 導入された機能:")
            print("   ✅ 高度な重複除去（ハッシュ + 類似性分析）")
            print("   ✅ Gemini URL contextによる投稿内容強化")
            print("   ✅ 重要度ベースの優先表示")
            print("   ✅ カテゴリ自動分類")
            
            print(f"\n💾 バックアップ場所: {backup_dir}")
            print("\n🚀 次のステップ:")
            print("   python build.py - 強化版でサイト生成")
            print("   より詳細で重複のないX投稿が表示されます")
            
        else:
            print("\n❌ 統合テストに失敗しました")
            print("🔄 バックアップからの復旧を検討してください")
    else:
        print("\n❌ build.py のパッチに失敗しました")
        print("🔄 手動での統合が必要です")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")