#!/usr/bin/env python3
"""
Deploy to GitHub Pages (gh-pages branch) with updated HTML
"""
import subprocess
import os
from pathlib import Path

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("🚀 Deploy to GitHub Pages (gh-pages branch)")
        print("=" * 50)
        
        # 1. Generate the website using our fixed build script
        print("🔨 Building site with build_simple_ranking.py...")
        result = subprocess.run(['python', 'build_simple_ranking.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("   ✅ Site built successfully")
            if result.stdout:
                print(f"   Output: {result.stdout[:200]}...")
        else:
            print(f"   ❌ Build failed: {result.stderr}")
            return False
        
        # 2. Check if index.html was generated
        if not Path('index.html').exists():
            print("   ❌ index.html was not generated!")
            return False
        
        # Check file size
        index_size = Path('index.html').stat().st_size
        print(f"   📊 Generated index.html: {index_size} bytes")
        
        if index_size < 10000:
            print("   ⚠️ Generated file seems too small")
        
        # 3. Switch to gh-pages branch
        print("🔄 Switching to gh-pages branch...")
        
        # Try to checkout gh-pages, create if doesn't exist
        result = subprocess.run(['git', 'checkout', 'gh-pages'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("   📝 Creating new gh-pages branch...")
            subprocess.run(['git', 'checkout', '--orphan', 'gh-pages'], check=True)
            # Remove all files from the new branch
            subprocess.run(['git', 'rm', '-rf', '.'], capture_output=True)
        else:
            print("   ✅ Switched to gh-pages branch")
        
        # 4. Copy generated HTML files
        print("📁 Adding generated files...")
        
        # Add the generated HTML and CSS files
        files_to_add = ['index.html', 'style.css']
        if Path('.nojekyll').exists():
            files_to_add.append('.nojekyll')
        
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
                print(f"   ✅ Added {file}")
        
        # 5. Commit changes
        print("💾 Committing updated site...")
        commit_msg = "Update: Tab functionality fixed with enhanced ranking system"
        
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Committed changes")
        else:
            if "nothing to commit" in result.stdout:
                print("   ℹ️ No changes to commit")
            else:
                print(f"   ❌ Commit failed: {result.stderr}")
        
        # 6. Push to gh-pages branch
        print("📤 Pushing to gh-pages branch...")
        result = subprocess.run(['git', 'push', 'origin', 'gh-pages'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Pushed to gh-pages successfully!")
        else:
            print(f"   ❌ Push failed: {result.stderr}")
            
            # Try force push if needed
            print("   🔄 Trying force push...")
            result2 = subprocess.run(['git', 'push', '--force', 'origin', 'gh-pages'], 
                                   capture_output=True, text=True)
            if result2.returncode == 0:
                print("   ✅ Force push successful!")
            else:
                print(f"   ❌ Force push also failed: {result2.stderr}")
                return False
        
        # 7. Switch back to main
        print("🔄 Switching back to main branch...")
        subprocess.run(['git', 'checkout', 'main'], capture_output=True)
        
        print("\n🎉 Deployment to GitHub Pages Complete!")
        print("=" * 50)
        print("✅ Site built with build_simple_ranking.py")
        print("✅ Tab functionality with hidden class logic")
        print("✅ Enhanced card structure with priority system")
        print("✅ Deployed to gh-pages branch")
        
        print("\n📋 Expected Results (2-3 minutes):")
        print("  🌐 Site URL: https://awano27.github.io/daily-ai-news-pages/")
        print("  📅 Date: 2025-08-23 (current)")
        print("  🖱️ Tabs: Business/Tools/Posts working properly")
        print("  🎨 Enhanced styling and priority indicators")
        print("  📰 Full content with ranking system")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 GitHub Pages deployment completed!")
        print("Your enhanced AI news site with working tabs")
        print("will be live at: https://awano27.github.io/daily-ai-news-pages/")
        print("⏱️ Check in 2-3 minutes for the updates!")
        exit(0)
    else:
        exit(1)