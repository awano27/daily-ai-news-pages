#!/usr/bin/env python3
"""
Setup GitHub Actions workflow for daily-ai-news-pages repository
"""
import subprocess
import os
from pathlib import Path

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("⚙️ Setup GitHub Actions for Pages Repository")
        print("=" * 50)
        
        # 1. Create .github/workflows directory
        workflows_dir = Path('.github/workflows')
        workflows_dir.mkdir(parents=True, exist_ok=True)
        print("📁 Created .github/workflows directory")
        
        # 2. Create GitHub Pages workflow
        workflow_content = """name: Deploy AI News to GitHub Pages

on:
  push:
    branches: [ main ]
  schedule:
    # Run daily at 7:00 JST (22:00 UTC)
    - cron: '0 22 * * *'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt || pip install feedparser pyyaml deep-translator==1.11.4 beautifulsoup4 requests google-generativeai>=0.3.0
        
    - name: Set environment variables
      run: |
        echo "TRANSLATE_TO_JA=1" >> $GITHUB_ENV
        echo "TRANSLATE_ENGINE=google" >> $GITHUB_ENV
        echo "HOURS_LOOKBACK=24" >> $GITHUB_ENV
        echo "MAX_ITEMS_PER_CATEGORY=25" >> $GITHUB_ENV
        
    - name: Build AI News Site
      timeout-minutes: 10
      run: |
        echo "🔨 Building AI News site with enhanced ranking..."
        python build_simple_ranking.py
        
        echo "📊 Verifying build output..."
        if [ -f "index.html" ]; then
          file_size=$(stat -c%s index.html)
          echo "✅ index.html generated ($file_size bytes)"
          
          if [ "$file_size" -gt 10000 ]; then
            echo "✅ Build verification passed"
          else
            echo "⚠️ Build file seems small but continuing..."
          fi
        else
          echo "❌ index.html not generated!"
          exit 1
        fi
        
    - name: Setup Pages
      uses: actions/configure-pages@v3
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v2
      with:
        path: '.'
        
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v2
      
    - name: Display results
      run: |
        echo "🎉 Deployment completed!"
        echo "🌐 Site URL: https://awano27.github.io/daily-ai-news-pages/"
        echo "📅 Expected: Current date with enhanced features"
        echo "🖱️ Expected: Working tab functionality"
"""
        
        workflow_file = workflows_dir / 'deploy-pages.yml'
        with open(workflow_file, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        print("✅ Created deploy-pages.yml workflow")
        
        # 3. Create/update requirements.txt if needed
        requirements_content = """feedparser
pyyaml
deep-translator==1.11.4
beautifulsoup4
requests
google-generativeai>=0.3.0
"""
        
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print("✅ Created/updated requirements.txt")
        
        # 4. Create .nojekyll file for GitHub Pages
        with open('.nojekyll', 'w') as f:
            f.write('')
        print("✅ Created .nojekyll file")
        
        # 5. Add all new files
        print("📝 Adding workflow files...")
        subprocess.run(['git', 'add', '.github/', 'requirements.txt', '.nojekyll'], check=True)
        
        # 6. Commit workflow
        commit_msg = "feat: Add GitHub Actions workflow for automatic Pages deployment"
        print("💾 Committing workflow...")
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # 7. Push to trigger first workflow
        print("📤 Pushing workflow to GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n🎉 GitHub Actions Workflow Setup Complete!")
        print("=" * 50)
        print("✅ Created deploy-pages.yml workflow")
        print("✅ Setup automatic daily builds at 7:00 JST")
        print("✅ Enabled manual workflow trigger")
        print("✅ Configured GitHub Pages deployment")
        
        print("\n📋 What Happens Next:")
        print("  1. 🔄 GitHub Actions will start building (~2-3 minutes)")
        print("  2. 🏗️ Site will be built using build_simple_ranking.py")
        print("  3. 🚀 HTML will be deployed to GitHub Pages")
        print("  4. 📅 Daily automatic updates at 7:00 JST")
        
        print("\n🌐 Expected Results (5-10 minutes):")
        print("  • Site: https://awano27.github.io/daily-ai-news-pages/")
        print("  • Date: 2025-08-23 (current)")
        print("  • Tabs: Business/Tools/Posts working")
        print("  • Cards: Enhanced structure with priorities")
        
        print("\n🔍 Monitor Progress:")
        print("  • Actions: https://github.com/awano27/daily-ai-news-pages/actions")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Workflow setup completed!")
        print("The site will now update automatically and immediately.")
        print("Check GitHub Actions for build progress.")
        exit(0)
    else:
        exit(1)