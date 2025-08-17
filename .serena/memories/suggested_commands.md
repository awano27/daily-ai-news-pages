# Suggested Commands

## Development Commands

### Install Dependencies
```bash
# Windows Command Prompt
pip install feedparser pyyaml deep-translator==1.11.4 requests beautifulsoup4

# Or use requirements.txt if available
pip install -r requirements.txt
```

### Local Development (Windows)
```bash
# Set environment variables (Command Prompt)
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=8
set TZ=Asia/Tokyo

# PowerShell
$env:TRANSLATE_TO_JA="1"
$env:TRANSLATE_ENGINE="google"
$env:HOURS_LOOKBACK="24"
$env:MAX_ITEMS_PER_CATEGORY="8"
$env:TZ="Asia/Tokyo"

# Build the site
python build.py

# Generate dashboard
python generate_comprehensive_dashboard.py

# Fix language indicators (if needed)
python fix_lang_chips.py
```

### Testing
```bash
# Test build process
python test_build.py

# Test dashboard generation
python test_dashboard.py

# Quick test
python quick_test.py

# Run test batch script
run_test.bat
```

### Deployment (Manual)
```bash
# Simple deploy
simple_deploy.bat

# Deploy with dashboard
run_dashboard.bat

# Quick deploy
quick_deploy.bat

# Force deploy
force_deploy.bat
```

### Git Commands (Windows)
```bash
# Check status
git status

# Add all changes
git add -A

# Commit with skip CI flag
git commit -m "chore: update site content [skip ci]"

# Push to main
git push origin main

# Pull latest changes
git pull origin main
```

### System Commands (Windows)
```bash
# List directory contents
dir

# Change directory
cd directory_name

# Copy files
copy source.txt destination.txt

# Delete file
del filename.txt

# Create directory
mkdir new_folder

# View file contents
type filename.txt

# Find text in files
findstr "search_text" *.py
```

### Python Scripts Available
- `build.py` - Main site generator
- `generate_comprehensive_dashboard.py` - Dashboard generator
- `fix_lang_chips.py` - Fix language indicators
- `url_filter.py` - Filter 403 URLs
- `test_*.py` - Various test scripts
- `deploy_*.py` - Deployment scripts
- `run_*.py` - Execution scripts

### Batch Scripts Available
- `run_test.bat` - Run tests
- `run_dashboard.bat` - Generate dashboard
- `simple_deploy.bat` - Simple deployment
- `force_deploy.bat` - Force deployment
- `quick_deploy.bat` - Quick deployment