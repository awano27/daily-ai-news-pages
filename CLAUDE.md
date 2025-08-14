# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static site generator for a Japanese AI news aggregation website. It automatically fetches AI-related news from multiple RSS feeds, translates summaries to Japanese, and generates a static HTML site hosted on GitHub Pages.

## Key Commands

### Local Development
```bash
# Install dependencies
pip install feedparser pyyaml deep-translator==1.11.4

# Set environment variables (Windows Command Prompt)
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=8

# Optional: Use DeepL instead of Google Translate
set DEEPL_API_KEY=your_api_key_here

# Build the site
python build.py

# Fix language indicators in generated HTML
python fix_lang_chips.py
```

### Testing Changes
```bash
# Generate the site locally
python build.py

# Open index.html in browser to preview
# Check console for JavaScript errors
# Verify all tabs work correctly
```

## Architecture

### Core Components

1. **build.py**: Main generator that:
   - Fetches RSS feeds from sources defined in `feeds.yml`
   - Filters content by time window (HOURS_LOOKBACK)
   - Translates English summaries to Japanese
   - Generates tabbed HTML interface
   - Caches translations in `_cache/translations.json`

2. **feeds.yml**: RSS feed configuration with three categories:
   - Business: Tech company blogs and business news
   - Tools: Developer-focused content and frameworks
   - Posts: Academic papers and research blogs
   - Sources marked with `general: true` are filtered for AI-related keywords

3. **GitHub Actions** (.github/workflows/build.yml):
   - Runs daily at 07:00 JST
   - Automatically commits generated HTML with `[skip ci]` flag
   - Uses Google Translate by default (configurable to DeepL)

### Translation System

- Primary: Google Translate (via deep-translator library)
- Fallback: MyMemory Translation API
- Optional: DeepL API (requires API key)
- Caching: Translations stored in `_cache/translations.json` to avoid repeated API calls

### Content Processing Flow

1. RSS feeds fetched based on `feeds.yml` configuration
2. General news sources filtered for AI-related keywords
3. Content from last 24 hours selected
4. English summaries translated to Japanese
5. HTML generated with tabbed interface
6. Post-processing with `fix_lang_chips.py` if needed
7. Automatic commit and deployment to GitHub Pages

## Important Considerations

- **Translation Cache**: Always preserve `_cache/translations.json` to avoid unnecessary API calls
- **Commit Messages**: Use `[skip ci]` in automated commits to prevent workflow loops
- **GitHub Pages**: `.nojekyll` file required to serve files starting with underscore
- **Rate Limits**: Google Translate has rate limits; cache helps mitigate this
- **Character Encoding**: Ensure UTF-8 encoding for Japanese text
- **RSS Feed Reliability**: Some feeds may be unavailable; handle gracefully