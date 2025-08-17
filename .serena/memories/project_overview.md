# Daily AI News - Project Overview

## Purpose
This is a static site generator for a Japanese AI news aggregation website. It automatically fetches AI-related news from multiple RSS feeds, translates summaries to Japanese, and generates a static HTML site hosted on GitHub Pages.

## Tech Stack
- **Language**: Python 3.11+
- **Key Libraries**:
  - feedparser - RSS feed parsing
  - pyyaml - Configuration file handling
  - deep-translator==1.11.4 - Translation services
  - requests - HTTP requests
  - beautifulsoup4 (implied) - HTML parsing

- **Infrastructure**:
  - GitHub Actions for automated daily builds
  - GitHub Pages for hosting
  - Google Sheets integration for X/Twitter posts

## Main Architecture
1. **Data Sources**: RSS feeds from various AI news sources (Google AI, OpenAI, Meta, etc.)
2. **Processing Pipeline**:
   - Fetch RSS feeds from sources defined in `feeds.yml`
   - Filter content by time window (HOURS_LOOKBACK)
   - Translate English summaries to Japanese
   - Generate tabbed HTML interface
   - Cache translations in `_cache/translations.json`
3. **Output**: Static HTML files for GitHub Pages

## Key Files
- `build.py` - Main generator script
- `feeds.yml` - RSS feed configuration with three categories (Business, Tools, Posts)
- `style.css` - Website styling
- `.github/workflows/build.yml` - GitHub Actions workflow
- `CLAUDE.md` - Project instructions for Claude Code
- `url_filter.py` - URL filtering for avoiding 403 errors
- `generate_comprehensive_dashboard.py` - Dashboard generation

## Translation System
- Primary: Google Translate (via deep-translator library)
- Fallback: MyMemory Translation API
- Optional: DeepL API (requires API key)
- Caching: Translations stored in `_cache/translations.json`

## Environment Variables
- `HOURS_LOOKBACK` - Time window for fetching news (default: 24)
- `MAX_ITEMS_PER_CATEGORY` - Max items per category (default: 8)
- `TRANSLATE_TO_JA` - Enable Japanese translation (default: 1)
- `TRANSLATE_ENGINE` - Translation engine (google|mymemory|deepl)
- `X_POSTS_CSV` - Path/URL to X/Twitter posts CSV
- `TZ` - Timezone (Asia/Tokyo)