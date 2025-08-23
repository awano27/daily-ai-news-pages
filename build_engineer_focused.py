#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI Tech Radar - Engineer-focused News Aggregator
エンジニア向けに最適化されたAIニュース収集・生成システム
"""

import os
import json
import yaml
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import re
from urllib.parse import urlparse
from deep_translator import GoogleTranslator
import time

# Configuration
@dataclass
class Config:
    """Configuration for the news aggregator"""
    hours_lookback: int = 24
    max_items_per_category: int = 15
    translate_to_ja: bool = True
    cache_dir: Path = Path("_cache")
    output_file: Path = Path("index_engineer_focused.html")
    feeds_file: Path = Path("feeds_engineer.yml")
    
    # Engineer-specific settings
    min_technical_score: float = 0.6
    prioritize_code_examples: bool = True
    include_implementation_difficulty: bool = True
    
    # Categories optimized for engineers
    categories: List[str] = field(default_factory=lambda: [
        "implementation",  # Tools, frameworks, libraries
        "research",        # Papers, algorithms, theory
        "production",      # MLOps, deployment, scaling
        "tutorials",       # Guides, how-tos, examples
        "releases",        # New versions, updates
    ])

@dataclass
class Article:
    """Enhanced article with engineer-focused metadata"""
    title: str
    url: str
    summary: str
    published: datetime
    source: str
    category: str
    
    # Engineer-specific fields
    technical_score: float = 0.0
    implementation_difficulty: str = "medium"
    estimated_read_time: int = 5
    has_code: bool = False
    tech_stack: List[str] = field(default_factory=list)
    is_trending: bool = False
    github_stars: Optional[int] = None
    performance_metrics: Dict[str, Any] = field(default_factory=dict)

class TechnicalAnalyzer:
    """Analyze articles for technical content and relevance"""
    
    # Keywords that indicate technical content
    TECH_KEYWORDS = {
        'implementation': ['code', 'api', 'sdk', 'library', 'framework', 'tutorial', 'example', 'snippet'],
        'architecture': ['design', 'pattern', 'scalable', 'distributed', 'microservice', 'pipeline'],
        'performance': ['optimization', 'speed', 'latency', 'throughput', 'benchmark', 'efficient'],
        'ml_specific': ['model', 'training', 'inference', 'dataset', 'accuracy', 'loss', 'gradient'],
        'tools': ['pytorch', 'tensorflow', 'langchain', 'huggingface', 'openai', 'anthropic'],
        'deployment': ['docker', 'kubernetes', 'aws', 'gcp', 'azure', 'production', 'deploy'],
    }
    
    # Programming languages and frameworks
    TECH_STACK_PATTERNS = {
        'Python': r'\b(python|pytorch|tensorflow|numpy|pandas|scikit)\b',
        'JavaScript': r'\b(javascript|typescript|node|react|vue|next)\b',
        'Rust': r'\b(rust|cargo|tokio)\b',
        'Go': r'\b(golang|go\s+lang)\b',
        'CUDA': r'\b(cuda|gpu|nvidia)\b',
        'Docker': r'\b(docker|container|kubernetes)\b',
    }
    
    @classmethod
    def calculate_technical_score(cls, article: Article) -> float:
        """Calculate how technical/relevant an article is for engineers"""
        score = 0.0
        text = f"{article.title} {article.summary}".lower()
        
        # Check for technical keywords
        for category, keywords in cls.TECH_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in text)
            score += matches * 0.1
        
        # Check for code indicators
        if any(indicator in text for indicator in ['```', 'code', 'github', 'implementation']):
            score += 0.3
            article.has_code = True
        
        # Check for metrics/benchmarks
        if re.search(r'\d+[%x]|\d+ms|\d+gb', text):
            score += 0.2
        
        # Papers and research get bonus
        if 'arxiv' in article.url or 'paper' in text:
            score += 0.2
        
        return min(score, 1.0)
    
    @classmethod
    def detect_tech_stack(cls, article: Article) -> List[str]:
        """Detect technologies mentioned in the article"""
        text = f"{article.title} {article.summary}".lower()
        detected = []
        
        for tech, pattern in cls.TECH_STACK_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(tech)
        
        return detected
    
    @classmethod
    def estimate_difficulty(cls, article: Article) -> str:
        """Estimate implementation difficulty"""
        text = f"{article.title} {article.summary}".lower()
        
        # Advanced indicators
        if any(word in text for word in ['advanced', 'complex', 'deep dive', 'expert', 'optimization']):
            return "hard"
        
        # Beginner indicators
        if any(word in text for word in ['introduction', 'getting started', 'beginner', 'basic', 'simple']):
            return "easy"
        
        return "medium"
    
    @classmethod
    def estimate_read_time(cls, article: Article) -> int:
        """Estimate reading time in minutes"""
        word_count = len(article.summary.split())
        
        # Technical content takes longer to read
        if article.has_code:
            word_count *= 1.5
        
        # Average reading speed: 200 words per minute for technical content
        return max(1, int(word_count / 200))

class EngineerFeedProcessor:
    """Process feeds with engineer-specific enhancements"""
    
    def __init__(self, config: Config):
        self.config = config
        self.translator = GoogleTranslator(source='en', target='ja') if config.translate_to_ja else None
        self.cache_dir = config.cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        
    def load_feeds(self) -> Dict[str, List[str]]:
        """Load engineer-optimized feed sources"""
        feeds_file = self.config.feeds_file
        
        # Create default feeds if file doesn't exist
        if not feeds_file.exists():
            return self.create_default_feeds()
        
        with open(feeds_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def create_default_feeds(self) -> Dict[str, List[str]]:
        """Create default engineer-focused feeds"""
        feeds = {
            'implementation': [
                'https://news.ycombinator.com/rss',
                'https://www.reddit.com/r/MachineLearning/.rss',
                'https://huggingface.co/blog/feed.xml',
                'https://blog.langchain.dev/rss/',
            ],
            'research': [
                'https://arxiv.org/rss/cs.AI',
                'https://arxiv.org/rss/cs.LG',
                'https://arxiv.org/rss/cs.CL',
            ],
            'production': [
                'https://engineering.fb.com/feed/',
                'https://netflixtechblog.com/feed',
                'https://aws.amazon.com/blogs/machine-learning/feed/',
            ],
            'releases': [
                'https://github.com/trending/python?since=daily',
                'https://pypi.org/rss/updates.xml',
            ]
        }
        
        # Save to file
        with open(self.config.feeds_file, 'w', encoding='utf-8') as f:
            yaml.dump(feeds, f)
        
        return feeds
    
    def fetch_articles(self) -> List[Article]:
        """Fetch and process articles from all feeds"""
        feeds = self.load_feeds()
        all_articles = []
        cutoff_time = datetime.now() - timedelta(hours=self.config.hours_lookback)
        
        for category, feed_urls in feeds.items():
            for feed_url in feed_urls:
                try:
                    articles = self.process_feed(feed_url, category, cutoff_time)
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"Error processing {feed_url}: {e}")
        
        # Analyze and score articles
        for article in all_articles:
            article.technical_score = TechnicalAnalyzer.calculate_technical_score(article)
            article.tech_stack = TechnicalAnalyzer.detect_tech_stack(article)
            article.implementation_difficulty = TechnicalAnalyzer.estimate_difficulty(article)
            article.estimated_read_time = TechnicalAnalyzer.estimate_read_time(article)
        
        # Filter by technical score
        all_articles = [a for a in all_articles if a.technical_score >= self.config.min_technical_score]
        
        # Sort by technical score and recency
        all_articles.sort(key=lambda a: (a.technical_score, a.published), reverse=True)
        
        # Mark trending articles (top 20%)
        trending_threshold = int(len(all_articles) * 0.2)
        for i, article in enumerate(all_articles[:trending_threshold]):
            article.is_trending = True
        
        return all_articles
    
    def process_feed(self, feed_url: str, category: str, cutoff_time: datetime) -> List[Article]:
        """Process a single feed"""
        feed = feedparser.parse(feed_url)
        articles = []
        
        for entry in feed.entries[:self.config.max_items_per_category]:
            try:
                # Parse publication date
                published = datetime.now()
                if hasattr(entry, 'published_parsed'):
                    published = datetime(*entry.published_parsed[:6])
                
                # Skip old articles
                if published < cutoff_time:
                    continue
                
                # Create article
                article = Article(
                    title=entry.get('title', 'No title'),
                    url=entry.get('link', ''),
                    summary=self.clean_summary(entry.get('summary', '')),
                    published=published,
                    source=self.get_source_name(feed_url),
                    category=category
                )
                
                # Translate if needed
                if self.translator and article.summary:
                    article.summary = self.translate_with_cache(article.summary)
                
                articles.append(article)
                
            except Exception as e:
                print(f"Error processing entry: {e}")
        
        return articles
    
    def clean_summary(self, summary: str) -> str:
        """Clean and truncate summary"""
        # Remove HTML tags
        summary = re.sub(r'<[^>]+>', '', summary)
        # Truncate to reasonable length
        if len(summary) > 300:
            summary = summary[:297] + '...'
        return summary.strip()
    
    def get_source_name(self, url: str) -> str:
        """Extract readable source name from URL"""
        domain = urlparse(url).netloc
        domain = domain.replace('www.', '').replace('.com', '').replace('.org', '')
        return domain.title()
    
    def translate_with_cache(self, text: str) -> str:
        """Translate with caching to avoid repeated API calls"""
        cache_key = hashlib.md5(text.encode()).hexdigest()
        cache_file = self.cache_dir / f"trans_{cache_key}.txt"
        
        if cache_file.exists():
            return cache_file.read_text(encoding='utf-8')
        
        try:
            translated = self.translator.translate(text)
            cache_file.write_text(translated, encoding='utf-8')
            time.sleep(0.1)  # Rate limiting
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return text

class HTMLGenerator:
    """Generate the engineer-focused HTML output"""
    
    @staticmethod
    def generate(articles: List[Article], config: Config) -> None:
        """Generate the complete HTML file"""
        # Group articles by category
        categorized = {}
        for article in articles:
            if article.category not in categorized:
                categorized[article.category] = []
            categorized[article.category].append(article)
        
        # Generate HTML
        html = HTMLGenerator.generate_html(categorized)
        
        # Write to file
        config.output_file.write_text(html, encoding='utf-8')
        print(f"Generated: {config.output_file}")
    
    @staticmethod
    def generate_html(categorized: Dict[str, List[Article]]) -> str:
        """Generate the HTML content"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
        
        # Count statistics
        total_articles = sum(len(articles) for articles in categorized.values())
        trending_count = sum(1 for articles in categorized.values() for a in articles if a.is_trending)
        
        html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>AI Tech Radar — {now}</title>
  <link rel="stylesheet" href="style_engineer.css"/>
</head>
<body>
  <header class="site-header">
    <div class="header-content">
      <div class="brand">
        <span class="brand-icon">⚡</span>
        <span class="brand-text">AI Tech Radar</span>
        <span class="brand-tagline">Engineering Intelligence</span>
      </div>
      <nav class="header-nav">
        <button class="theme-toggle" aria-label="テーマ切り替え">🌓</button>
        <a href="#dashboard" class="nav-link premium">📊 Dashboard</a>
      </nav>
    </div>
  </header>

  <div class="hero-section">
    <div class="hero-content">
      <h1 class="hero-title">
        <span class="gradient-text">エンジニアのための</span>
        <span class="highlight">最新AI技術情報</span>
      </h1>
      <p class="hero-description">
        実装可能な最新AI技術・ツール・論文を厳選配信。
        技術スコア {Config().min_technical_score:.0%} 以上の高品質コンテンツのみを掲載。
      </p>
      
      <div class="quick-stats">
        <div class="stat-item pulse">
          <span class="stat-icon">🔥</span>
          <span class="stat-value">{trending_count}</span>
          <span class="stat-label">Trending</span>
        </div>
        <div class="stat-item">
          <span class="stat-icon">📚</span>
          <span class="stat-value">{total_articles}</span>
          <span class="stat-label">Articles</span>
        </div>
        <div class="stat-item">
          <span class="stat-icon">🕒</span>
          <span class="stat-value">24h</span>
          <span class="stat-label">Coverage</span>
        </div>
      </div>
    </div>
  </div>

  <main class="container">
    <section class="filter-section">
      <div class="search-bar">
        <input type="text" id="searchInput" placeholder="🔍 キーワード、技術、企業名で検索..." />
      </div>
      
      <div class="filter-tags">
        <span class="filter-tag active" data-filter="all">すべて</span>
        <span class="filter-tag" data-filter="implementation">実装</span>
        <span class="filter-tag" data-filter="research">研究</span>
        <span class="filter-tag" data-filter="production">本番環境</span>
      </div>
    </section>

    <div class="content-tabs">
      <div class="tab-nav">
"""
        
        # Generate tab buttons
        for i, (category, articles) in enumerate(categorized.items()):
            active = 'active' if i == 0 else ''
            icon = HTMLGenerator.get_category_icon(category)
            html += f"""        <button class="tab-btn {active}" data-tab="{category}">
          <span class="tab-icon">{icon}</span>
          <span class="tab-text">{category.title()}</span>
          <span class="tab-count">{len(articles)}</span>
        </button>
"""
        
        html += """      </div>

"""
        
        # Generate tab content
        for i, (category, articles) in enumerate(categorized.items()):
            active = 'active' if i == 0 else ''
            html += f"""      <div class="tab-content {active}" id="{category}">
        <div class="cards-grid">
"""
            
            for article in articles[:15]:  # Limit articles per category
                html += HTMLGenerator.generate_article_card(article)
            
            html += """        </div>
      </div>
"""
        
        html += """    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4>AI Tech Radar</h4>
        <p>エンジニアのための最新AI技術情報を毎日配信</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 AI Tech Radar. Built with ❤️ for Engineers.</p>
      <p class="update-time">最終更新: """ + now + """</p>
    </div>
  </footer>

  <script src="script_engineer.js"></script>
</body>
</html>"""
        
        return html
    
    @staticmethod
    def get_category_icon(category: str) -> str:
        """Get icon for category"""
        icons = {
            'implementation': '⚙️',
            'research': '🔬',
            'production': '🚀',
            'tutorials': '📖',
            'releases': '🎉',
            'business': '💼',
            'tools': '🛠️',
        }
        return icons.get(category, '📄')
    
    @staticmethod
    def get_difficulty_badge(difficulty: str) -> str:
        """Get difficulty badge HTML"""
        colors = {
            'easy': ('初級', 'difficulty-easy'),
            'medium': ('中級', 'difficulty-medium'),
            'hard': ('上級', 'difficulty-hard'),
        }
        label, cls = colors.get(difficulty, ('中級', 'difficulty-medium'))
        return f'<span class="badge {cls}">{label}</span>'
    
    @staticmethod
    def generate_article_card(article: Article) -> str:
        """Generate HTML for a single article card"""
        # Format time
        time_ago = HTMLGenerator.format_time_ago(article.published)
        
        # Generate badges
        badges = []
        if article.is_trending:
            badges.append('<span class="badge hot">🔥 Hot</span>')
        if article.has_code:
            badges.append('<span class="badge new">Code</span>')
        badges.append(HTMLGenerator.get_difficulty_badge(article.implementation_difficulty))
        
        # Generate tech stack tags
        tech_tags = ''.join(f'<span class="tech-tag">{tech}</span>' for tech in article.tech_stack[:4])
        
        # Truncate summary
        summary = article.summary[:200] + '...' if len(article.summary) > 200 else article.summary
        
        return f"""          <article class="article-card" data-category="{article.category}">
            <div class="card-header">
              <div class="card-badges">
                {' '.join(badges)}
              </div>
              <button class="bookmark-btn" aria-label="ブックマーク">🔖</button>
            </div>

            <h3 class="card-title">
              <a href="{article.url}" target="_blank">{article.title}</a>
            </h3>

            <div class="card-meta">
              <span class="meta-item">📅 {time_ago}</span>
              <span class="meta-item">📖 {article.source}</span>
              <span class="meta-item">⏱️ {article.estimated_read_time}分</span>
            </div>

            <p class="card-summary">{summary}</p>

            <div class="tech-stack">
              {tech_tags}
            </div>

            <div class="card-actions">
              <a href="{article.url}" class="action-link primary" target="_blank">
                <span>📖 詳細を読む</span>
              </a>
            </div>
          </article>
"""
    
    @staticmethod
    def format_time_ago(dt: datetime) -> str:
        """Format datetime as relative time"""
        now = datetime.now()
        diff = now - dt
        
        hours = int(diff.total_seconds() / 3600)
        if hours < 1:
            return "今"
        elif hours < 24:
            return f"{hours}時間前"
        else:
            days = hours // 24
            return f"{days}日前"

def main():
    """Main execution function"""
    # Load configuration from environment
    config = Config(
        hours_lookback=int(os.getenv('HOURS_LOOKBACK', '24')),
        max_items_per_category=int(os.getenv('MAX_ITEMS_PER_CATEGORY', '15')),
        translate_to_ja=os.getenv('TRANSLATE_TO_JA', '1') == '1'
    )
    
    print(f"AI Tech Radar - Engineer Edition")
    print(f"Configuration: {config.hours_lookback}h lookback, {config.max_items_per_category} items/category")
    
    # Process feeds
    processor = EngineerFeedProcessor(config)
    articles = processor.fetch_articles()
    
    print(f"Fetched {len(articles)} high-quality technical articles")
    
    # Generate HTML
    HTMLGenerator.generate(articles, config)
    
    print("Build complete!")

if __name__ == "__main__":
    main()