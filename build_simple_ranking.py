# -*- coding: utf-8 -*-
"""
Simple Enhanced Daily AI News - 確実に動作するランキングシステム
元の build.py をベースに、情報量を維持しつつランキング機能を追加

HTML Structure Fix Applied: 2025-08-23
- Enhanced card template with priority system
- Proper HTML tag structure and closure
- CSS generation included for styling
- Tab functionality JavaScript fixed (hidden class logic)
- Force GitHub Actions to use this updated version
"""

import os, re, sys, json, time, html, csv, io
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
import yaml
import feedparser
import requests
import random
from bs4 import BeautifulSoup

# 基本設定
HOURS_LOOKBACK = int(os.getenv('HOURS_LOOKBACK', '24'))
MAX_ITEMS_PER_CATEGORY = int(os.getenv('MAX_ITEMS_PER_CATEGORY', '25'))
TOP_PICKS_COUNT = int(os.getenv('TOP_PICKS_COUNT', '10'))
TRANSLATE_TO_JA = os.getenv('TRANSLATE_TO_JA', '1') == '1'
TRANSLATE_ENGINE = os.getenv('TRANSLATE_ENGINE', 'google')
X_POSTS_CSV = os.getenv('X_POSTS_CSV', 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0')

# 翻訳機能
try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
    TRANSLATE_AVAILABLE = True
    print("✅ 翻訳機能: 利用可能")
except ImportError:
    print("⚠️ 翻訳機能: deep-translator未インストール")
    TRANSLATE_AVAILABLE = False

class SimpleEngineerRanking:
    """AIエンジニア/業務効率化 有用度ランキング"""
    
    # エンジニア重要キーワード（重み付き）
    TECH_KEYWORDS = {
        # 高優先度 (3.0倍)
        'code': 3.0, 'api': 3.0, 'sdk': 3.0, 'github': 3.0, 'implementation': 3.0,
        'tutorial': 3.0, 'framework': 3.0, 'library': 3.0, 'sample': 2.8,
        
        # AI/ML (2.5倍)
        'pytorch': 2.5, 'tensorflow': 2.5, 'huggingface': 2.5, 'gpt': 2.5, 
        'llm': 2.5, 'openai': 2.5, 'anthropic': 2.5, 'model': 2.5, 'ai': 2.5,
        
        # インフラ (2.0倍)
        'docker': 2.0, 'kubernetes': 2.0, 'aws': 2.0, 'azure': 2.0, 'gcp': 2.0,
        'deployment': 2.0, 'production': 2.0, 'mlops': 2.0,
        
        # パフォーマンス (1.8倍)
        'performance': 1.8, 'benchmark': 1.8, 'optimization': 1.8, 'speed': 1.8,
        'memory': 1.8, 'gpu': 1.8, 'cuda': 1.8,
        
        # 研究 (1.5倍) 
        'research': 1.5, 'paper': 1.5, 'arxiv': 1.5, 'algorithm': 1.5,
        'method': 1.5, 'evaluation': 1.5
    }

    # 業務効率化・実務活用のキーワード（重み付き）
    EFFICIENCY_KEYWORDS = {
        # 強い意図（3.0倍）
        'automation': 3.0, 'automate': 3.0, 'workflow': 3.0, 'rpa': 3.0,
        'copilot': 3.0, 'prompt': 2.6, 'prompt engineering': 2.8,
        'zapier': 2.8, 'make.com': 2.4, 'notion': 2.2, 'slack': 2.0,
        'excel': 2.4, 'spreadsheet': 2.2, 'power automate': 2.6,
        'powerapps': 2.2, 'power bi': 2.2, 'apps script': 2.4, 'gas': 2.4,

        # 日本語キーワード（2.0-3.0倍）
        '自動化': 3.0, '効率化': 2.8, '業務効率': 2.6, '省力化': 2.4,
        'ワークフロー': 2.6, '手順': 2.0, 'テンプレート': 2.0, '導入事例': 2.4,
        '活用事例': 2.4, 'コツ': 2.0, '使い方': 2.2, '時短': 2.2,
        'スクリプト': 2.2, 'マクロ': 2.2,
    }
    
    # 信頼できるソース
    TRUSTED_DOMAINS = [
        'arxiv.org', 'github.com', 'pytorch.org', 'tensorflow.org', 
        'huggingface.co', 'openai.com', 'anthropic.com', 'deepmind.com',
        'ai.googleblog.com', 'research.facebook.com', 'cloud.google.com',
        'learn.microsoft.com', 'devblogs.microsoft.com', 'powerautomate.microsoft.com',
        'zapier.com', 'notion.so', 'workspaceupdates.googleblog.com',
        'salesforce.com', 'atlassian.com', 'ibm.com'
    ]
    
    @classmethod
    def calculate_score(cls, item):
        """AIエンジニア/業務効率化の有用度スコア (0-10)"""
        title = item.get('title', '').lower()
        summary = item.get('summary', '').lower()
        url = item.get('url', '').lower()
        
        content = f"{title} {summary}"
        score = 0.0
        
        # キーワードマッチング
        for keyword, weight in cls.TECH_KEYWORDS.items():
            if keyword in content:
                score += weight
                if keyword in title:
                    score += weight * 0.5
        for keyword, weight in cls.EFFICIENCY_KEYWORDS.items():
            if keyword in content:
                score += weight
                if keyword in title:
                    score += weight * 0.6
        
        # 信頼できるソースボーナス
        domain = urlparse(url).netloc.lower()
        for trusted in cls.TRUSTED_DOMAINS:
            if trusted in domain:
                score *= 1.25
                break
        
        # 実装/ハウツー/コードの特別ボーナス
        howto_indicators = [
            'how to', 'step-by-step', 'guide', 'tutorial', 'best practices',
            'チュートリアル', '手順', '入門', '使い方', '導入事例', '活用事例'
        ]
        code_indicators = ['```', 'code example', 'implementation', 'github.com', 'gist.github.com']
        if any(x in content for x in howto_indicators + code_indicators):
            score *= 1.15
        
        # 10点満点に正規化
        return min(score, 10.0)

def load_translation_cache():
    """翻訳キャッシュを読み込み"""
    cache_file = Path('_cache/translations.json')
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_translation_cache(cache):
    """翻訳キャッシュを保存"""
    cache_dir = Path('_cache')
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / 'translations.json'
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def translate_text(text, target_lang='ja', cache=None):
    """テキストを翻訳（キャッシュ対応）"""
    if not TRANSLATE_AVAILABLE or not TRANSLATE_TO_JA:
        return text
    
    if cache is None:
        cache = {}
    
    # キャッシュチェック
    cache_key = f"{text[:100]}_{target_lang}"
    if cache_key in cache:
        return cache[cache_key]
    
    try:
        if TRANSLATE_ENGINE == 'google':
            translator = GoogleTranslator(source='auto', target=target_lang)
        else:
            translator = MyMemoryTranslator(source='auto', target=target_lang)
        
        result = translator.translate(text[:500])  # 長いテキストは切り詰め
        cache[cache_key] = result
        return result
    except:
        return text

def load_feeds_config():
    """フィード設定を読み込み"""
    feeds_file = Path('feeds.yml')
    if feeds_file.exists():
        with open(feeds_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    # デフォルト設定
    return {
        'business': [
            {'url': 'https://techcrunch.com/feed/', 'name': 'TechCrunch'},
            {'url': 'https://aws.amazon.com/blogs/machine-learning/feed/', 'name': 'AWS ML Blog'},
            {'url': 'https://ai.googleblog.com/feeds/posts/default', 'name': 'Google AI Blog'}
        ],
        'tools': [
            {'url': 'https://huggingface.co/blog/feed.xml', 'name': 'Hugging Face'},
            {'url': 'https://pytorch.org/blog/feed.xml', 'name': 'PyTorch Blog'},
            {'url': 'https://blog.openai.com/rss/', 'name': 'OpenAI Blog'}
        ],
        'posts': [
            {'url': 'https://www.reddit.com/r/MachineLearning/.rss', 'name': 'Reddit ML'},
            {'url': 'https://arxiv.org/rss/cs.AI', 'name': 'ArXiv AI'},
            {'url': 'https://arxiv.org/rss/cs.LG', 'name': 'ArXiv Learning'}
        ]
    }

def is_recent(published_date, hours_back=24):
    """指定時間内の記事かチェック"""
    if not published_date:
        return True
    
    try:
        if isinstance(published_date, str):
            # ISO形式や一般的な形式をパース
            from dateutil import parser
            pub_time = parser.parse(published_date)
        else:
            # struct_time の場合
            pub_time = datetime(*published_date[:6], tzinfo=timezone.utc)
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        return pub_time > cutoff_time
    except:
        return True

def fetch_feed_items(url, source_name, max_items=25):
    """フィードから記事を取得"""
    try:
        print(f"📡 取得中: {source_name} ({url})")
        
        # User-Agentを設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AI-News-Bot/1.0)'
        }
        
        # タイムアウト付きで取得
        import urllib.request
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            feed_data = response.read()
        
        # feedparserで解析
        feed = feedparser.parse(feed_data)
        items = []
        
        for entry in feed.entries[:max_items]:
            # 最近の記事のみ
            if not is_recent(entry.get('published_parsed'), HOURS_LOOKBACK):
                continue
            
            item = {
                'title': entry.get('title', '').strip(),
                'url': entry.get('link', ''),
                'summary': entry.get('summary', entry.get('description', '')),
                'published': entry.get('published', ''),
                'source': source_name,
                'engineer_score': 0.0
            }
            
            # HTMLタグを除去
            item['summary'] = re.sub(r'<[^>]+>', '', item['summary'])
            item['summary'] = html.unescape(item['summary']).strip()
            
            # エンジニア関連度スコア計算
            item['engineer_score'] = SimpleEngineerRanking.calculate_score(item)
            
            items.append(item)
        
        print(f"✅ {source_name}: {len(items)}件取得")
        return items
        
    except Exception as e:
        print(f"❌ {source_name} エラー: {e}")
        return []

def _clean_tweet_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"https?://\S+", "", text)  # URLs削除
    text = re.sub(r"\s+", " ", text).strip()  # 余分な空白を圧縮
    text = re.sub(r"(#[\w一-龥ぁ-んァ-ンー]+\s*)+$", "", text)  # 末尾のハッシュタグ群を削除
    text = re.sub(r"(@[\w_]+\s*)+$", "", text)  # 末尾のメンション群を削除
    return text.strip()

def _extract_external_url(text: str) -> str | None:
    if not text:
        return None
    urls = re.findall(r"https?://\S+", text)
    for u in urls:
        try:
            host = urlparse(u).netloc.lower()
            if any(x in host for x in ["x.com", "twitter.com", "t.co"]):
                continue
            return u
        except Exception:
            continue
    return None

def _fetch_og_title(url: str, timeout: int = 8) -> str | None:
    if not url:
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; AI-News-Bot/1.0)'}
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        tag = soup.find('meta', attrs={'property': 'og:title'})
        if tag and tag.get('content'):
            return tag.get('content').strip()
        if soup.title and soup.title.string:
            return soup.title.string.strip()
    except Exception:
        return None
    return None

def _username_from_status_url(x_status_url: str) -> str | None:
    try:
        p = urlparse(x_status_url)
        parts = [seg for seg in p.path.split('/') if seg]
        if len(parts) >= 2 and parts[0].lower() not in ("i",):
            return parts[0]
    except Exception:
        return None
    return None

def _guess_tag(text: str) -> str | None:
    t = (text or '').lower()
    jp = (text or '')
    # 実装/チュートリアル系
    if any(k in t for k in ['how to', 'tutorial', 'guide', 'step-by-step']) or any(k in jp for k in ['使い方', '手順', '入門', 'チュートリアル']):
        return '実装'
    # 業務効率化/自動化系
    if any(k in t for k in ['workflow', 'automation', 'automate', 'copilot', 'zapier', 'notion', 'excel', 'apps script', 'power automate', 'prompt']) or any(k in jp for k in ['効率化', '自動化', '時短']):
        return '効率化'
    # 研究/論文系
    if any(k in t for k in ['arxiv', 'paper', 'research']) or any(k in jp for k in ['論文', '研究']):
        return '研究'
    # リリース/発表
    if any(k in t for k in ['release', 'launch', 'announce', 'announced']) or any(k in jp for k in ['発表', 'リリース']):
        return '発表'
    return None

def _build_readable_summary(cleaned: str, og_title: str | None, domain: str | None) -> str:
    tag = _guess_tag((og_title or '') + ' ' + (cleaned or ''))
    parts = []
    if tag:
        parts.append(f"[{tag}]")
    if og_title:
        parts.append(og_title.strip())
    # 投稿要約は重複しないときのみ添える
    if cleaned:
        if not og_title or og_title.lower() not in cleaned.lower():
            # 短く整形
            brief = cleaned.strip()
            if len(brief) > 140:
                brief = brief[:140] + '...'
            parts.append(f"投稿要約: {brief}")
    if domain:
        parts.append(f"出典: {domain}")
    # 仕上げ（全角区切りで視認性向上）
    summary = ' ｜ '.join(p for p in parts if p)
    # 最終長さ上限
    if len(summary) > 280:
        summary = summary[:277] + '...'
    return summary

def fetch_x_posts():
    """X(Twitter)投稿を取得"""
    try:
        print(f"📱 X投稿取得中: {X_POSTS_CSV}")
        
        response = requests.get(X_POSTS_CSV, timeout=30)
        print(f"🌐 HTTP Response: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ HTTP Status: {response.status_code}")
            return []
        
        content = response.text.strip()
        print(f"📄 受信データサイズ: {len(content)} 文字")
        print(f"📄 データ先頭100文字: {content[:100]}")
        
        # CSVかテキストかを判定
        if content.startswith('"Timestamp"') or ',' in content[:200]:
            print("📋 CSV形式として処理中...")
            return fetch_x_posts_from_csv(content)
        else:
            print("📄 テキスト形式として処理中...")
            return fetch_x_posts_from_text(content)
            
    except Exception as e:
        print(f"❌ X投稿取得エラー: {e}")
        import traceback
        traceback.print_exc()
        return []

def fetch_x_posts_from_csv(csv_content):
    """CSV形式のXポストを処理"""
    try:
        reader = csv.DictReader(io.StringIO(csv_content))
        
        posts = []
        og_cache: dict[str, str] = {}
        for row in reader:
            tweet_content = (row.get('Tweet Content', '') or '').strip()
            username = (row.get('Username', '') or '').strip()
            timestamp_str = (row.get('Timestamp', '') or '').strip()
            if not tweet_content:
                continue
            try:
                from dateutil import parser
                post_date = parser.parse(timestamp_str)
                if not is_recent(post_date.strftime('%Y-%m-%d %H:%M:%S'), HOURS_LOOKBACK):
                    continue
            except Exception as e:
                print(f"⚠️ 日付解析エラー: {timestamp_str} - {e}")
                continue

            cleaned = _clean_tweet_text(tweet_content)
            ext_url = row.get('Source Link 1', '').strip() or row.get('Source Link 2', '').strip()
            if not ext_url:
                ext_url = _extract_external_url(tweet_content)

            domain = urlparse(ext_url).netloc if ext_url else ''
            og_title = None
            if ext_url:
                og_title = og_cache.get(ext_url)
                if og_title is None:
                    og_title = _fetch_og_title(ext_url)
                    if og_title:
                        og_cache[ext_url] = og_title

            if og_title:
                title = f"{og_title}（{domain}）"
            else:
                title = cleaned if len(cleaned) <= 100 else (cleaned[:100] + '...')

            summary = _build_readable_summary(cleaned, og_title, domain)

            source_label = f"X @{username}" if username else "X (Twitter)"
            score_payload = {'title': title, 'summary': summary or cleaned, 'url': ext_url or ''}

            posts.append({
                'title': title,
                'url': ext_url or '',
                'summary': summary or cleaned,
                'published': timestamp_str,
                'source': source_label,
                'engineer_score': SimpleEngineerRanking.calculate_score(score_payload)
            })
        
        print(f"✅ CSV形式X投稿: {len(posts)}件取得")
        return posts[:MAX_ITEMS_PER_CATEGORY]
        
    except Exception as e:
        print(f"❌ CSV処理エラー: {e}")
        return []

def fetch_x_posts_from_text(text_content):
    """テキスト形式のXポストを処理"""
    try:
        import re
        
        # 日付パターンでポストを分割
        posts = []
        
        # August XX, 2025 形式の日付を検索
        date_pattern = r'(August \d{1,2}, 2025 at \d{1,2}:\d{2}[AP]M)'
        username_pattern = r'@([a-zA-Z0-9_]+)'
        url_pattern = r'https?://[^\s,"]+'
        
        # テキストを行で分割して処理
        lines = text_content.split('\n')
        current_post = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 日付を検出
            date_match = re.search(date_pattern, line)
            if date_match:
                # 前のポストを保存
                if current_post.get('content'):
                    posts.append(current_post.copy())
                
                # 新しいポストを開始
                current_post = {
                    'timestamp': date_match.group(1),
                    'content': '',
                    'urls': [],
                    'username': ''
                }
                continue
            
            # ユーザー名を検出
            username_match = re.search(username_pattern, line)
            if username_match and not current_post.get('username'):
                current_post['username'] = username_match.group(1)
            
            # URLを検出
            url_matches = re.findall(url_pattern, line)
            for url in url_matches:
                if url not in current_post['urls']:
                    current_post['urls'].append(url)
            
            # コンテンツを蓄積
            if not re.search(date_pattern, line):  # 日付行以外
                if current_post.get('content'):
                    current_post['content'] += ' ' + line
                else:
                    current_post['content'] = line
        
        # 最後のポストを追加
        if current_post.get('content'):
            posts.append(current_post)
        
        # ポストオブジェクトに変換
        converted_posts = []
        og_cache: dict[str, str] = {}
        for post_data in posts[:MAX_ITEMS_PER_CATEGORY]:
            if not post_data.get('content'):
                continue
            
            # 日付チェック（最近48時間以内）
            try:
                from dateutil import parser
                post_date = parser.parse(post_data['timestamp'])
                if not is_recent(post_date.strftime('%Y-%m-%d %H:%M:%S'), HOURS_LOOKBACK):
                    continue
            except:
                continue
            
            cleaned = _clean_tweet_text(post_data['content'])
            ext_url = None
            for u in post_data.get('urls', []):
                host = urlparse(u).netloc.lower()
                if not any(x in host for x in ["x.com", "twitter.com", "t.co"]):
                    ext_url = u
                    break
            domain = urlparse(ext_url).netloc if ext_url else ''
            og_title = None
            if ext_url:
                og_title = og_cache.get(ext_url)
                if og_title is None:
                    og_title = _fetch_og_title(ext_url)
                    if og_title:
                        og_cache[ext_url] = og_title

            if og_title:
                title = f"{og_title}（{domain}）"
            else:
                title = cleaned if len(cleaned) <= 100 else (cleaned[:100] + '...')

            summary = _build_readable_summary(cleaned, og_title, domain)

            source_label = f"X @{post_data.get('username', 'unknown')}"
            score_payload = {'title': title, 'summary': summary or cleaned, 'url': ext_url or ''}
            converted_posts.append({
                'title': title,
                'url': ext_url or '',
                'summary': summary or cleaned,
                'published': post_data['timestamp'],
                'source': source_label,
                'engineer_score': SimpleEngineerRanking.calculate_score(score_payload)
            })
        
        print(f"✅ テキスト形式X投稿: {len(converted_posts)}件取得")
        return converted_posts
        
    except Exception as e:
        print(f"❌ テキスト処理エラー: {e}")
        import traceback
        traceback.print_exc()
        return []

def format_time_ago(published_str):
    """経過時間を日本語で表示"""
    if not published_str:
        return ""
    
    try:
        from dateutil import parser
        pub_time = parser.parse(published_str)
        now = datetime.now(timezone.utc)
        
        if pub_time.tzinfo is None:
            pub_time = pub_time.replace(tzinfo=timezone.utc)
        
        diff = now - pub_time
        hours = diff.total_seconds() / 3600
        
        if hours < 1:
            return "1時間未満"
        elif hours < 24:
            return f"{int(hours)}時間前"
        else:
            return f"{int(hours // 24)}日前"
    except:
        return ""

def generate_css():
    """CSSファイルを生成"""
    css_content = '''/* Digital.gov compliance deployed at 2025-08-23 */
:root{
  /* Digital.gov準拠: WCAG AAA対応カラーシステム */
  --fg:#0f172a; --bg:#ffffff; --muted:#475569; --line:#e2e8f0;
  --brand:#1e40af; --brand-weak:#f1f5f9; --chip:#f8fafc;
  --brand-hover:#1e3a8a; --brand-light:#bfdbfe; --brand-dark:#1e3a8a;
  --success:#15803d; --warning:#ca8a04; --danger:#dc2626;
  --info:#0369a1; --neutral:#64748b;
  
  /* 段階的背景色（彩度を下げた背景） */
  --bg-subtle:#f8fafc; --bg-muted:#f1f5f9; --bg-emphasis:#e2e8f0;
  
  /* グラデーション（彩度調整済み） */
  --gradient:linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  --gradient-subtle:linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  
  /* シャドウ */
  --shadow:0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg:0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  
  /* レイアウト変数 */
  --border-radius: 12px;
  --spacing-xs: 4px; --spacing-sm: 8px; --spacing-md: 16px; 
  --spacing-lg: 24px; --spacing-xl: 32px; --spacing-2xl: 48px;
  
  /* タイポグラフィ */
  --font-size-xs: 12px; --font-size-sm: 14px; --font-size-base: 16px;
  --font-size-lg: 18px; --font-size-xl: 20px; --font-size-2xl: 24px;
  --font-size-3xl: 32px; --font-size-4xl: 36px;
  
  /* フォーカス表示 */
  --focus-ring: 0 0 0 3px rgba(59, 130, 246, 0.5);
  --focus-ring-offset: 2px;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:var(--bg);
  color:var(--fg);
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,'Noto Sans JP',sans-serif;
  font-size:var(--font-size-base);
  line-height:1.6;
  scroll-behavior:smooth;
}
.container{
  max-width:1000px;
  margin:0 auto;
  padding:var(--spacing-lg) var(--spacing-md);
  display:flex;
  flex-direction:column;
  gap:var(--spacing-lg);
}

/* ヘッダー */
.site-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:var(--spacing-md);
  background:var(--bg-subtle);
  border-bottom:1px solid var(--line);
  margin-bottom:var(--spacing-lg);
}
.brand{
  font-size:var(--font-size-xl);
  font-weight:700;
  color:var(--brand);
}
.updated{
  color:var(--muted);
  font-size:var(--font-size-sm);
}

/* メインコンテンツ */
.page-title{
  font-size:var(--font-size-3xl);
  font-weight:800;
  text-align:center;
  margin:0 0 var(--spacing-md);
  background:var(--gradient);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
}
.lead{
  text-align:center;
  color:var(--muted);
  font-size:var(--font-size-lg);
  margin:0 0 var(--spacing-xl);
  max-width:600px;
  margin-left:auto;
  margin-right:auto;
}

/* KPIグリッド */
.kpi-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:var(--spacing-md);
  margin-bottom:var(--spacing-xl);
}
.kpi-card{
  background:var(--bg-subtle);
  padding:var(--spacing-md);
  border-radius:var(--border-radius);
  text-align:center;
  border:1px solid var(--line);
}
.kpi-value{
  font-size:var(--font-size-2xl);
  font-weight:800;
  color:var(--brand);
}
.kpi-label{
  font-size:var(--font-size-sm);
  color:var(--muted);
  margin-top:var(--spacing-xs);
}
.kpi-note{
  font-size:var(--font-size-xs);
  color:var(--success);
  margin-top:var(--spacing-xs);
}

/* フィルターコントロール */
.filters{
  display:flex;
  flex-wrap:wrap;
  gap:var(--spacing-sm);
  align-items:center;
  padding:var(--spacing-md);
  background:var(--bg-subtle);
  border-radius:var(--border-radius);
  margin-bottom:var(--spacing-lg);
}
.filter-group{
  display:flex;
  align-items:center;
  gap:var(--spacing-sm);
}
.filter-label{
  font-size:var(--font-size-sm);
  color:var(--muted);
  font-weight:600;
}
.filter-select, .filter-input{
  padding:var(--spacing-xs) var(--spacing-sm);
  border:1px solid var(--line);
  border-radius:calc(var(--border-radius) / 2);
  font-size:var(--font-size-sm);
  background:var(--bg);
}
.filter-select:focus, .filter-input:focus{
  outline:none;
  border-color:var(--brand);
  box-shadow:var(--focus-ring);
}

/* タブナビゲーション */
.tabs{
  display:flex;
  border-bottom:2px solid var(--line);
  margin-bottom:var(--spacing-lg);
  overflow-x:auto;
}
.tab-button{
  background:none;
  border:none;
  padding:var(--spacing-md) var(--spacing-lg);
  font-size:var(--font-size-base);
  font-weight:600;
  color:var(--muted);
  cursor:pointer;
  border-bottom:3px solid transparent;
  white-space:nowrap;
  transition:all 0.2s;
}
.tab-button:hover{
  color:var(--fg);
  background:var(--bg-subtle);
}
.tab-button.active{
  color:var(--brand);
  border-bottom-color:var(--brand);
  background:var(--brand-weak);
}
.tab-button:focus{
  outline:none;
  box-shadow:var(--focus-ring);
}

/* タブコンテンツ */
.tab-content{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
  gap:var(--spacing-md);
}
.tab-panel{
  transition:opacity 0.3s ease;
}
.tab-panel.hidden{
  display:none;
}

/* カード */
.enhanced-card{
  background:var(--bg);
  border:1px solid var(--line);
  border-radius:var(--border-radius);
  padding:var(--spacing-md);
  box-shadow:var(--shadow);
  transition:all 0.3s ease;
  position:relative;
}
.enhanced-card:hover{
  transform:translateY(-2px);
  box-shadow:var(--shadow-lg);
  border-color:var(--brand-light);
}
.card-priority{
  position:absolute;
  top:var(--spacing-sm);
  right:var(--spacing-sm);
  background:var(--brand);
  color:white;
  padding:var(--spacing-xs) var(--spacing-sm);
  border-radius:calc(var(--border-radius) / 2);
  font-size:var(--font-size-xs);
  font-weight:600;
}
.card-priority.high{background:var(--success)}
.card-priority.medium{background:var(--warning)}
.card-priority.low{background:var(--neutral)}
.card-header{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  margin-bottom:var(--spacing-sm);
}
.card-title{
  font-size:var(--font-size-lg);
  font-weight:700;
  line-height:1.3;
  margin:0;
}
.card-title a{
  color:var(--fg);
  text-decoration:none;
}
.card-title a:hover{
  color:var(--brand);
  text-decoration:underline;
}
.card-meta{
  display:flex;
  gap:var(--spacing-sm);
  font-size:var(--font-size-xs);
  color:var(--muted);
  margin-bottom:var(--spacing-sm);
}
.card-source{
  background:var(--chip);
  padding:var(--spacing-xs) var(--spacing-sm);
  border-radius:calc(var(--border-radius) / 3);
  font-weight:600;
}
.card-summary{
  color:var(--fg);
  line-height:1.5;
  margin:var(--spacing-sm) 0;
}
.card-footer{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-top:var(--spacing-sm);
  padding-top:var(--spacing-sm);
  border-top:1px solid var(--line);
}
.card-score{
  font-size:var(--font-size-sm);
  font-weight:600;
  color:var(--info);
}
.card-time{
  font-size:var(--font-size-xs);
  color:var(--muted);
}

/* レスポンシブ */
@media (max-width: 768px) {
  .container{
    padding:var(--spacing-md) var(--spacing-sm);
  }
  .page-title{
    font-size:var(--font-size-2xl);
  }
  .lead{
    font-size:var(--font-size-base);
  }
  .filters{
    flex-direction:column;
    align-items:stretch;
  }
  .filter-group{
    justify-content:space-between;
  }
  .tabs{
    justify-content:space-around;
  }
  .tab-button{
    flex:1;
    padding:var(--spacing-sm);
    font-size:var(--font-size-sm);
  }
  .tab-content{
    grid-template-columns:1fr;
  }
}

/* アクセシビリティ */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* ハイコントラストモード対応 */
@media (prefers-contrast: high) {
  :root {
    --line: #000000;
    --muted: #000000;
  }
  .enhanced-card {
    border-width: 2px;
  }
}

/* ダークモード対応 */
@media (prefers-color-scheme: dark) {
  :root {
    --fg: #f1f5f9;
    --bg: #0f172a;
    --muted: #94a3b8;
    --line: #334155;
    --bg-subtle: #1e293b;
    --bg-muted: #334155;
    --chip: #1e293b;
  }
}
'''
    return css_content

def main():
    """メイン処理"""
    print("🚀 Simple Enhanced Daily AI News Builder")
    print("=" * 50)
    
    # JST時間を取得
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst).strftime('%Y-%m-%d %H:%M JST')
    
    print(f"📅 生成日時: {now}")
    print(f"⏰ 過去 {HOURS_LOOKBACK} 時間の記事を収集")
    print(f"📊 カテゴリ別最大 {MAX_ITEMS_PER_CATEGORY} 件")
    print(f"🌍 翻訳: {'有効' if TRANSLATE_TO_JA else '無効'}")
    
    # 翻訳キャッシュ読み込み
    translation_cache = load_translation_cache()
    
    # フィード設定読み込み
    feeds_config = load_feeds_config()
    
    # 各カテゴリのデータ収集
    all_categories = {}
    
    for category, feeds in feeds_config.items():
        print(f"\n📂 {category.upper()} カテゴリ処理中...")
        
        category_items = []
        for feed_config in feeds:
            items = fetch_feed_items(
                feed_config['url'], 
                feed_config['name'], 
                MAX_ITEMS_PER_CATEGORY
            )
            category_items.extend(items)
        
        # X投稿も追加（postsカテゴリのみ）
        if category == 'posts':
            print(f"🔍 DEBUG: postsカテゴリでX投稿取得開始...")
            print(f"🔍 DEBUG: X_POSTS_CSV環境変数 = {X_POSTS_CSV}")
            print(f"🔍 DEBUG: HOURS_LOOKBACK = {HOURS_LOOKBACK}")
            
            x_items = fetch_x_posts()
            print(f"🔍 DEBUG: X投稿取得完了 - {len(x_items)}件")
            
            if x_items:
                # Xポストのスコアを強制的に高くして優先表示
                for i, item in enumerate(x_items):
                    item['engineer_score'] = 10.0  # 最高スコア設定
                    print(f"🔍 DEBUG: Xポスト[{i+1}] - タイトル: {item['title'][:50]}... (スコア: {item['engineer_score']})")
                    print(f"🔍 DEBUG: Xポスト[{i+1}] - URL: {item.get('url', 'N/A')}")
                
                # Xポストを category_items に追加
                category_items.extend(x_items)
                print(f"🔍 DEBUG: Xポスト統合後の総記事数: {len(category_items)}件")
            else:
                print(f"⚠️ DEBUG: X投稿が取得されませんでした - 原因調査が必要")
        
        # エンジニア関連度でソート
        category_items.sort(key=lambda x: x['engineer_score'], reverse=True)
        category_items = category_items[:MAX_ITEMS_PER_CATEGORY]
        
        # 翻訳処理
        if TRANSLATE_TO_JA:
            print(f"🌍 {category} カテゴリ翻訳中...")
            for item in category_items:
                if item['title'] and not all(ord(c) < 128 for c in item['title']):
                    # すでに日本語の場合はスキップ
                    continue
                    
                item['title_ja'] = translate_text(item['title'], 'ja', translation_cache)
                if item['summary']:
                    item['summary_ja'] = translate_text(item['summary'], 'ja', translation_cache)
        
        all_categories[category.lower()] = category_items
        print(f"✅ {category}: {len(category_items)}件 (平均スコア: {sum(item['engineer_score'] for item in category_items) / len(category_items):.1f})")
        print(f"   → all_categories['{category.lower()}'] に保存")
    
    # 翻訳キャッシュ保存
    if TRANSLATE_TO_JA:
        save_translation_cache(translation_cache)
        print("💾 翻訳キャッシュ保存完了")
    
    # 統計情報
    total_items = sum(len(items) for items in all_categories.values())
    high_priority = sum(1 for items in all_categories.values() for item in items if item['engineer_score'] >= 7.0)
    
    print(f"\n📊 収集結果:")
    print(f"   総記事数: {total_items}件")
    print(f"   高優先度: {high_priority}件")
    print(f"   情報源: {sum(len(feeds) for feeds in feeds_config.values())}個")
    
    # Top Picks（全カテゴリ横断の上位）
    all_items_flat = [it for items in all_categories.values() for it in items]
    # URL重複除去（先に高スコアに並べてからユニーク化）
    all_items_flat.sort(key=lambda x: x['engineer_score'], reverse=True)
    seen = set()
    top_picks = []
    for it in all_items_flat:
        u = it.get('url')
        if u and u not in seen:
            top_picks.append(it)
            seen.add(u)
        if len(top_picks) >= TOP_PICKS_COUNT:
            break

    # HTMLテンプレート
    html_template = f'''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Daily AI News — {now}</title>
  <link rel="stylesheet" href="style.css"/>
</head>
<body>
  <header class="site-header">
    <div class="brand">📰 Daily AI News</div>
    <div class="updated">最終更新：{now}</div>
  </header>

  <main class="container">
    <h1 class="page-title">今日の最新AI情報</h1>
    <p class="lead">
        有用度スコアでランキング表示（AIエンジニア/業務効率化向け）。実装可能性・効率化効果・学習価値を重視して自動ソート。
        豊富な情報量（{total_items}件）を維持しつつ、重要度で整理表示。
    </p>

    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value">{total_items}件</div>
        <div class="kpi-label">総記事数</div>
        <div class="kpi-note">情報量維持</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{high_priority}件</div>
        <div class="kpi-label">高優先度記事</div>
        <div class="kpi-note">スコア7.0+</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{sum(len(feeds) for feeds in feeds_config.values())}個</div>
        <div class="kpi-label">情報源</div>
        <div class="kpi-note">多角的収集</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{HOURS_LOOKBACK}h</div>
        <div class="kpi-label">収集範囲</div>
        <div class="kpi-note">最新性重視</div>
      </div>
    </section>

    <!-- Top Picks: 有用度上位 -->
    <section class="top-picks" aria-label="Top Picks">
      <h2 class="section-title">🏆 Top Picks — 有用度上位（上位 {min(TOP_PICKS_COUNT, len(top_picks))} 件）</h2>
      <div class="tab-content">
'''

    for item in top_picks:
        score = item['engineer_score']
        if score >= 7.0:
            priority = 'high'; priority_text = '高'
        elif score >= 4.0:
            priority = 'medium'; priority_text = '中'
        else:
            priority = 'low'; priority_text = '低'

        display_title = item.get('title_ja', item['title'])
        display_summary = item.get('summary_ja', item['summary'])
        time_ago = format_time_ago(item['published'])

        html_template += f'''
        <article class="enhanced-card" data-score="{score:.1f}" data-source="{item['source']}" data-time="{item['published']}">
          <div class="card-priority {priority}">{priority_text} {score:.1f}</div>
          <header class="card-header">
            <h3 class="card-title">
              <a href="{item['url']}" target="_blank" rel="noopener">{html.escape(display_title)}</a>
            </h3>
          </header>
          <div class="card-meta">
            <span class="card-source">{item['source']}</span>
            {f'<span class="card-time">{time_ago}</span>' if time_ago else ''}
          </div>
          <div class="card-summary">{html.escape(display_summary[:200] + '...' if len(display_summary) > 200 else display_summary)}</div>
          <footer class="card-footer">
            <span class="card-score">有用度: {score:.1f}</span>
            <span class="card-time">{time_ago}</span>
          </footer>
        </article>
'''

    html_template += '''
      </div>
    </section>

    <section class="filters">
      <div class="filter-group">
        <label class="filter-label">検索:</label>
        <input type="text" id="searchInput" class="filter-input" placeholder="キーワード検索..."/>
      </div>
      <div class="filter-group">
        <label class="filter-label">重要度:</label>
        <select id="importanceFilter" class="filter-select">
          <option value="all">すべて</option>
          <option value="high">高 (7.0+)</option>
          <option value="medium">中 (4.0-6.9)</option>
          <option value="low">低 (0-3.9)</option>
        </select>
      </div>
      <div class="filter-group">
        <label class="filter-label">並び順:</label>
        <select id="sortBy" class="filter-select">
          <option value="score">重要度順</option>
          <option value="time">新着順</option>
          <option value="source">情報源順</option>
        </select>
      </div>
    </section>

    <nav class="tabs">
      <button class="tab-button active" data-tab="business">
        📈 Business ({len(all_categories.get('business', []))})
      </button>
      <button class="tab-button" data-tab="tools">
        🔧 Tools ({len(all_categories.get('tools', []))})
      </button>
      <button class="tab-button" data-tab="posts">
        💬 Posts ({len(all_categories.get('posts', []))})
      </button>
    </nav>
'''
    
    # 各カテゴリのコンテンツ生成（businessを最初に確実に表示）
    category_order = ['business', 'tools', 'posts']
    for category_name in category_order:
        # カテゴリが存在しない場合は空のリストとして扱う
        items = all_categories.get(category_name, [])
        print(f"DEBUG: {category_name} カテゴリ - {len(items)}件の記事")
        is_active = category_name == 'business'
        panel_class = 'tab-panel' if is_active else 'tab-panel hidden'
        
        html_template += f'''
    <section class="{panel_class}" data-category="{category_name.lower()}">
      <div class="tab-content">
'''
        
        for item in items:
            # 優先度ラベル
            score = item['engineer_score']
            if score >= 7.0:
                priority = 'high'
                priority_text = '高'
            elif score >= 4.0:
                priority = 'medium' 
                priority_text = '中'
            else:
                priority = 'low'
                priority_text = '低'
            
            # タイトルと要約（翻訳版があれば使用）
            display_title = item.get('title_ja', item['title'])
            display_summary = item.get('summary_ja', item['summary'])
            
            # 時間表示
            time_ago = format_time_ago(item['published'])
            
            html_template += f'''
        <article class="enhanced-card" data-score="{score:.1f}" data-source="{item['source']}" data-time="{item['published']}">
          <div class="card-priority {priority}">{priority_text} {score:.1f}</div>
          <header class="card-header">
            <h3 class="card-title">
              <a href="{item['url']}" target="_blank" rel="noopener">{html.escape(display_title)}</a>
            </h3>
          </header>
          <div class="card-meta">
            <span class="card-source">{item['source']}</span>
            {f'<span class="card-time">{time_ago}</span>' if time_ago else ''}
          </div>
          <div class="card-summary">{html.escape(display_summary[:200] + '...' if len(display_summary) > 200 else display_summary)}</div>
          <footer class="card-footer">
            <span class="card-score">有用度: {score:.1f}</span>
            <span class="card-time">{time_ago}</span>
          </footer>
        </article>
'''
        
        html_template += '''
      </div>
    </section>
'''
    
    # JavaScript追加
    html_template += '''
  </main>

<script>
// タブ切り替え機能
class TabController {
  constructor() {
    this.activeTab = 'business';
    this.init();
  }
  
  init() {
    // タブボタンのイベントリスナー
    document.querySelectorAll('.tab-button').forEach(button => {
      button.addEventListener('click', (e) => {
        const tab = e.target.dataset.tab;
        this.switchTab(tab);
      });
    });
    
    // フィルター機能
    this.setupFilters();
    
    // 初期表示：businessタブを明示的に表示
    this.switchTab('business');
  }
  
  switchTab(tabName) {
    if (this.activeTab === tabName) return;
    
    // ボタンの状態更新
    document.querySelectorAll('.tab-button').forEach(btn => {
      btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // パネルの表示切り替え（hidden class使用）
    document.querySelectorAll('.tab-panel').forEach(panel => {
      panel.classList.add('hidden');
    });
    document.querySelector(`[data-category="${tabName}"]`).classList.remove('hidden');
    
    this.activeTab = tabName;
    this.updateTabCounts(); // タブカウント更新
    this.applyFilters(); // フィルター再適用
  }
  
  updateTabCounts() {
    // 各タブの記事数をカウントして表示更新
    const tabs = ['business', 'tools', 'posts'];
    const tabLabels = {
      'business': '📈 Business',
      'tools': '🔧 Tools', 
      'posts': '💬 Posts'
    };
    
    tabs.forEach(tabName => {
      const panel = document.querySelector(`[data-category="${tabName}"]`);
      const count = panel ? panel.querySelectorAll('.enhanced-card').length : 0;
      const button = document.querySelector(`[data-tab="${tabName}"]`);
      if (button) {
        button.textContent = `${tabLabels[tabName]} (${count})`;
      }
    });
  }
  
  setupFilters() {
    // 検索フィルター
    document.getElementById('searchInput').addEventListener('input', () => {
      this.applyFilters();
    });
    
    // 重要度フィルター
    document.getElementById('importanceFilter').addEventListener('change', () => {
      this.applyFilters();
    });
    
    // ソート
    document.getElementById('sortBy').addEventListener('change', () => {
      this.applySorting();
    });
  }
  
  applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const importance = document.getElementById('importanceFilter').value;
    
    // 現在アクティブなタブのカードのみ処理
    const activePanel = document.querySelector(`[data-category="${this.activeTab}"]`);
    const cards = activePanel.querySelectorAll('.enhanced-card');
    
    cards.forEach(card => {
      let showCard = true;
      
      // 検索フィルター
      if (searchTerm) {
        const title = card.querySelector('.card-title a').textContent.toLowerCase();
        const summary = card.querySelector('.card-summary').textContent.toLowerCase();
        const source = card.querySelector('.card-source').textContent.toLowerCase();
        
        showCard = title.includes(searchTerm) || 
                  summary.includes(searchTerm) || 
                  source.includes(searchTerm);
      }
      
      // 重要度フィルター
      if (showCard && importance !== 'all') {
        const score = parseFloat(card.dataset.score);
        if (importance === 'high' && score < 7.0) showCard = false;
        if (importance === 'medium' && (score < 4.0 || score >= 7.0)) showCard = false;
        if (importance === 'low' && score >= 4.0) showCard = false;
      }
      
      card.style.display = showCard ? 'block' : 'none';
    });
  }
  
  applySorting() {
    const sortBy = document.getElementById('sortBy').value;
    const activePanel = document.querySelector(`[data-category="${this.activeTab}"]`);
    const container = activePanel.querySelector('.tab-content');
    const cards = Array.from(container.querySelectorAll('.enhanced-card'));
    
    cards.sort((a, b) => {
      if (sortBy === 'score') {
        return parseFloat(b.dataset.score) - parseFloat(a.dataset.score);
      } else if (sortBy === 'time') {
        const timeA = new Date(a.dataset.time || 0);
        const timeB = new Date(b.dataset.time || 0);
        return timeB - timeA;
      } else if (sortBy === 'source') {
        return a.dataset.source.localeCompare(b.dataset.source);
      }
      return 0;
    });
    
    // DOM再構築
    cards.forEach(card => container.appendChild(card));
    
    // フィルター再適用
    this.applyFilters();
  }
}

// 初期化
document.addEventListener('DOMContentLoaded', () => {
  new TabController();
});
</script>

</body>
</html>
'''
    
    # ファイル出力
    output_file = Path('index.html')
    output_file.write_text(html_template, encoding='utf-8')
    
    # CSS生成
    css_content = generate_css()
    css_file = Path('style.css')
    css_file.write_text(css_content, encoding='utf-8')
    print("✅ CSS file generated")
    
    print(f"✅ 生成完了: {output_file}")
    print(f"📊 総記事数: {total_items}件")
    print(f"🏆 高優先度: {high_priority}件")
    print(f"⭐ 平均スコア: {sum(item['engineer_score'] for items in all_categories.values() for item in items) / total_items:.1f}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Daily AI News 生成成功!")
            print("🌐 GitHub Pages にデプロイしてご確認ください")
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 処理が中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)
