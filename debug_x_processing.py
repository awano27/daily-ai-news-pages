#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug X Processing - X投稿処理の詳細デバッグ
"""
import os
import csv
import io
import requests
from pathlib import Path

def load_env():
    """環境変数を.envファイルから読み込み"""
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def test_csv_access():
    """CSVアクセスのテスト"""
    print("🌐 Google Sheets CSV直接アクセステスト")
    print("-" * 50)
    
    url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"📡 アクセス中: {url[:60]}...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"✅ HTTPステータス: {response.status_code}")
        print(f"📊 レスポンスサイズ: {len(response.content)} bytes")
        
        if response.status_code == 200:
            content = response.text
            lines = content.strip().split('\n')
            print(f"📋 CSV行数: {len(lines)}行")
            
            # 最初の5行を表示
            print("\n📝 CSV内容（最初の5行）:")
            for i, line in enumerate(lines[:5], 1):
                print(f"   {i}. {line[:100]}{'...' if len(line) > 100 else ''}")
            
            # CSVパース
            try:
                reader = csv.DictReader(io.StringIO(content))
                headers = reader.fieldnames
                print(f"\n📋 CSVヘッダー: {headers}")
                
                rows = list(reader)
                print(f"📊 データ行数: {len(rows)}行")
                
                if rows:
                    print("\n📝 最初のデータ行:")
                    first_row = rows[0]
                    for key, value in first_row.items():
                        print(f"   {key}: {value[:50]}{'...' if len(str(value)) > 50 else ''}")
                
                return True, rows
            except Exception as e:
                print(f"❌ CSVパースエラー: {e}")
                return False, []
        else:
            print(f"❌ HTTPエラー: {response.status_code}")
            return False, []
            
    except Exception as e:
        print(f"❌ アクセスエラー: {e}")
        return False, []

def test_enhanced_processor():
    """Enhanced X Processorのテスト"""
    print("\n🧪 Enhanced X Processor詳細テスト")
    print("-" * 50)
    
    try:
        from enhanced_x_processor import EnhancedXProcessor
        
        processor = EnhancedXProcessor()
        print("✅ EnhancedXProcessor初期化成功")
        
        # メソッドをテスト
        test_text = "これはテスト投稿です。AI技術について議論しています。"
        hash_result = processor.create_content_hash(test_text)
        print(f"📊 コンテンツハッシュテスト: {hash_result}")
        
        # 類似性テスト
        text1 = "OpenAIの新しいモデルについて"
        text2 = "OpenAIの最新モデルに関して"
        similarity = processor.is_similar_content(text1, text2)
        print(f"📊 類似性テスト: {similarity}")
        
        return processor
        
    except Exception as e:
        print(f"❌ Enhanced X Processorエラー: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_process_x_posts_detailed(processor, sample_data):
    """X投稿処理の詳細テスト"""
    print("\n🔄 X投稿処理詳細テスト")
    print("-" * 50)
    
    if not processor or not sample_data:
        print("⚠️ プロセッサまたはサンプルデータがありません")
        return
    
    try:
        # サンプルデータをCSV形式で処理
        print(f"📊 サンプルデータ: {len(sample_data)}行")
        
        processed_count = 0
        valid_posts = []
        
        for i, row in enumerate(sample_data[:5], 1):  # 最初の5行をテスト
            print(f"\n🔄 行 {i} を処理中...")
            
            date_str = row.get('Date', '')
            username = row.get('Username', '')
            text = row.get('Post Text', '')
            post_url = row.get('Post URL', '')
            
            print(f"   日付: {date_str}")
            print(f"   ユーザー: {username}")
            print(f"   テキスト長: {len(text)}文字")
            print(f"   URL: {post_url[:50]}{'...' if len(post_url) > 50 else ''}")
            
            # 基本的な有効性チェック
            if text and len(text.strip()) > 5:
                content_hash = processor.create_content_hash(text)
                print(f"   ✅ 有効な投稿 - ハッシュ: {content_hash}")
                
                valid_posts.append({
                    'username': username.replace('@', ''),
                    'text': text,
                    'url': post_url,
                    'date': date_str
                })
                processed_count += 1
            else:
                print(f"   ❌ 無効な投稿 - テキスト不足")
        
        print(f"\n📊 処理結果: {processed_count}件の有効な投稿")
        
        if valid_posts:
            # build形式に変換
            build_items = processor.convert_to_build_format(valid_posts)
            print(f"✅ build形式変換: {len(build_items)}件")
            
            for item in build_items:
                summary = item.get('_summary', '')
                print(f"   要約文字数: {len(summary)}文字")
                print(f"   要約: {summary[:50]}...")
        
    except Exception as e:
        print(f"❌ 処理テストエラー: {e}")
        import traceback
        traceback.print_exc()

def main():
    """メインテスト"""
    print("🔍 Enhanced X Processing Debug Tool")
    print("=" * 60)
    
    # 環境変数読み込み
    load_env()
    
    # 1. CSV直接アクセステスト
    csv_success, sample_data = test_csv_access()
    
    # 2. Enhanced Processorテスト
    processor = test_enhanced_processor()
    
    # 3. 詳細処理テスト
    if csv_success and processor:
        test_process_x_posts_detailed(processor, sample_data)
    
    # 4. 実際のprocess_x_postsメソッドテスト
    if processor:
        print("\n🚀 実際のprocess_x_postsメソッドテスト")
        print("-" * 50)
        
        try:
            csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
            posts = processor.process_x_posts(csv_url, max_posts=3)
            
            print(f"📊 最終結果: {len(posts)}件の投稿")
            
            if not posts:
                print("⚠️ 投稿が0件です。原因を調査中...")
                
                # より詳細なログを有効にして再試行
                print("\n🔄 詳細ログ付きで再試行...")
                
        except Exception as e:
            print(f"❌ process_x_postsエラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")