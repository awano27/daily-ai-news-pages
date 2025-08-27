import requests
import csv
import io

# X投稿の直接テスト
url = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

print("X投稿データ取得テスト")
print("="*40)

try:
    response = requests.get(url, timeout=30)
    print(f"HTTP Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.text
        print(f"データサイズ: {len(content)} 文字")
        
        # CSV解析
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        print(f"CSV行数: {len(rows)}")
        
        if rows:
            print(f"ヘッダー: {rows[0]}")
            
            # 有効な投稿をカウント
            valid_count = 0
            for row in rows[1:]:
                if len(row) >= 3 and row[2].strip():
                    valid_count += 1
                    if valid_count <= 3:  # 最初の3つを表示
                        print(f"投稿{valid_count}: {row[2][:50]}...")
            
            print(f"有効な投稿数: {valid_count}")
            
            if valid_count == 0:
                print("❌ 有効な投稿が見つかりません")
                print("先頭5行の詳細:")
                for i, row in enumerate(rows[:5]):
                    print(f"  行{i}: {row}")
            else:
                print("✅ X投稿データ取得成功")
        
    else:
        print(f"❌ HTTPエラー: {response.status_code}")
        
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()