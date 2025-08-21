# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A static site generator for a Japanese AI news aggregation website that:
- Fetches AI-related news from multiple RSS feeds (Business, Tools, Posts categories)
- Translates summaries to Japanese using Google Translate or DeepL
- Integrates X (Twitter) posts from Google Sheets
- Uses Gemini API for enhanced content analysis and URL context
- Generates static HTML hosted on GitHub Pages

## Key Commands

### Build and Deploy
```bash
# Install all dependencies
pip install -r requirements.txt

# Windows environment setup
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=8
set GEMINI_API_KEY=your_key_here

# Build the site
python build.py

# Generate comprehensive dashboard
python generate_comprehensive_dashboard.py

# Run comprehensive test
python comprehensive_test.py

# Deploy to GitHub Pages
python deploy.py
```

### Testing
```bash
# Run comprehensive system test
python comprehensive_test.py

# Test production build
python final_production_test.py

# Test dashboard generation
python test_dashboard.py

# Test Gemini integration
python test_gemini.py
```

### Batch Scripts (Windows)
```bash
# Run full test and build
run_test.bat

# Deploy to GitHub
simple_deploy.bat

# Generate daily report
run_daily_report.bat

# Run dashboard with SNS integration
run_sns_enhanced.bat
```

## Architecture

### Core Build Pipeline

1. **build.py**: Main generator
   - Fetches RSS feeds from `feeds.yml`
   - Filters by HOURS_LOOKBACK (default: 24 hours)
   - Translates summaries via Google Translate/DeepL
   - Integrates X posts from Google Sheets CSV
   - Generates tabbed HTML interface
   - Caches translations in `_cache/translations.json`

2. **enhanced_x_processor.py**: X/Twitter integration
   - Fetches posts from Google Sheets CSV URL
   - Deduplicates posts by content similarity
   - Formats posts with proper links and metadata

3. **gemini_url_context.py**: Gemini API integration
   - Analyzes URLs for additional context
   - Enhances summaries with AI-generated insights
   - Requires GEMINI_API_KEY environment variable

### Configuration Files

- **feeds.yml**: RSS feed sources organized by category
  - Business: Company blogs, tech news
  - Tools: Developer tools, frameworks
  - Posts: Academic papers, research
  - Sources with `general: true` filtered for AI keywords

- **requirements.txt**: Python dependencies including:
  - feedparser, pyyaml
  - deep-translator==1.11.4
  - google-generativeai>=0.3.0
  - beautifulsoup4, requests

### GitHub Actions Workflow

`.github/workflows/build.yml`:
- Runs daily at 07:00 JST (22:00 UTC)
- Sets environment variables for translation and content limits
- Executes build pipeline with timeout protection
- Auto-commits with `[skip ci]` to prevent loops

### Translation System

- **Primary**: Google Translate (deep-translator library)
- **Alternative**: DeepL API (requires DEEPL_API_KEY)
- **Fallback**: MyMemory Translation API
- **Caching**: `_cache/translations.json` persists translations

### X Posts Integration

Environment variable: `X_POSTS_CSV`
- Default: Google Sheets export URL
- Format: CSV with columns for content, links, timestamps
- Deduplication: Similarity threshold to avoid duplicates

## Important Considerations

- **Translation Cache**: Preserve `_cache/translations.json` to minimize API calls
- **Commit Messages**: Use `[skip ci]` flag to prevent workflow loops
- **GitHub Pages**: `.nojekyll` file enables underscore-prefixed files
- **Rate Limits**: Translation APIs have limits; caching mitigates this
- **Encoding**: UTF-8 required for Japanese text
- **Error Handling**: Timeouts set for all external API calls
- **Google Sheets Access**: Public CSV export URL required for X posts