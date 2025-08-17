# Task Completion Checklist

When completing a coding task in this project, follow these steps:

## Before Starting
1. Check if environment variables are set correctly
2. Ensure dependencies are installed: `pip install feedparser pyyaml deep-translator==1.11.4`
3. Pull latest changes from GitHub: `git pull origin main`

## During Development
1. Follow existing code patterns and style
2. Preserve UTF-8 encoding for Japanese text
3. Test locally with `python build.py` before committing
4. Check for 403 errors and handle gracefully
5. Update cache files if modifying translation logic

## After Implementation
1. **Test the changes**:
   - Run `python build.py` to ensure site builds correctly
   - Check generated `index.html` in browser
   - Verify Japanese translations are working
   - Test dashboard generation if modified

2. **Validate output**:
   - Ensure no broken HTML
   - Check console for JavaScript errors
   - Verify all tabs work correctly
   - Confirm translations are cached

3. **Git operations**:
   - Add changes: `git add -A`
   - Commit with descriptive message and `[skip ci]` flag for automated commits
   - Use co-authoring if generated via Claude Code
   - Push to main branch

4. **Deployment checklist**:
   - Ensure `.nojekyll` file exists for GitHub Pages
   - Check GitHub Actions workflow status
   - Verify site updates on GitHub Pages URL

## Common Issues to Check
- Character encoding issues with Japanese text
- 403 errors from Google News RSS feeds
- Translation API rate limits
- Cache file corruption
- GitHub Actions timeout (8 minutes limit)

## Important Notes
- NEVER commit API keys or secrets
- Always preserve `_cache/translations.json` to avoid repeated API calls
- Use `[skip ci]` in automated commits to prevent workflow loops
- Handle missing RSS feeds gracefully