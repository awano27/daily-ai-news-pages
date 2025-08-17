# Code Style and Conventions

## Python Style
- **Encoding**: UTF-8 with encoding header `# -*- coding: utf-8 -*-`
- **Imports**: Standard library first, then third-party, grouped logically
- **Docstrings**: Module-level docstrings explaining purpose and environment variables
- **Variable Naming**: UPPER_CASE for constants, snake_case for functions and variables
- **Type Hints**: Not consistently used across the codebase
- **Line Length**: No strict limit, but generally kept reasonable
- **Comments**: Inline comments in both English and Japanese

## Project Patterns
- **Configuration**: Environment variables for runtime configuration
- **Caching**: JSON file-based caching for translations and data
- **Error Handling**: Try-except blocks with fallback mechanisms
- **File Operations**: Using pathlib.Path for file paths
- **Time Handling**: JST timezone awareness with explicit timezone objects

## HTML Generation
- Template strings with placeholders
- Inline CSS and JavaScript for single-file distribution
- Bootstrap-based responsive design

## Git Conventions
- Commit messages with prefixes: `feat:`, `fix:`, `chore:`, `docs:`
- Use `[skip ci]` flag in automated commits to prevent workflow loops
- Co-authoring with Claude when generated via Claude Code

## File Naming
- Python scripts: snake_case.py
- Batch files: snake_case.bat or snake_case.ps1
- Configuration: feeds.yml, .env files
- Generated files: index.html, dashboard_data.json

## Special Considerations
- Character encoding: Always ensure UTF-8 for Japanese text
- .nojekyll file required for GitHub Pages to serve files starting with underscore
- Handle 403 errors gracefully from certain RSS feeds (Google News)