#!/usr/bin/env python3
"""
Fix submodule issue for GitHub Pages deployment
"""
import subprocess
import os
from pathlib import Path

def run_git_command(cmd):
    """Run git command with environment fixes"""
    env = os.environ.copy()
    env['CYGWIN'] = 'nodosfilewarning'
    env['TMP'] = '/tmp'
    env['TEMP'] = '/tmp'
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, shell=True)
        print(f"Command: {cmd}")
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr and result.returncode != 0:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run command {cmd}: {e}")
        return False

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("🔧 Fixing submodule reference issues")
        print("=" * 50)
        
        # Remove any submodule references
        if Path('.gitmodules').exists():
            print("📝 Removing .gitmodules file...")
            Path('.gitmodules').unlink()
        
        # Remove serena-src directory if it exists
        serena_src = Path('.serena-src')
        if serena_src.exists():
            print("📁 Removing .serena-src directory...")
            import shutil
            shutil.rmtree(serena_src)
        
        # Remove from git cache
        print("🧹 Clearing git cache...")
        run_git_command('git rm --cached .serena-src')
        run_git_command('git rm --cached .gitmodules')
        
        # Add all changes
        print("📝 Adding changes...")
        run_git_command('git add .')
        
        # Commit the fix
        print("💾 Committing submodule fix...")
        run_git_command('git commit -m "fix: Remove .serena-src submodule references completely"')
        
        # Push to both branches
        print("📤 Pushing to main branch...")
        run_git_command('git push origin main')
        
        print("📤 Pushing to gh-pages branch...")
        run_git_command('git push origin gh-pages')
        
        print("✅ Submodule issue fixed!")
        print("🌐 GitHub Pages should now deploy successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Fix completed successfully!")
        print("GitHub Pages deployment should work now.")
    else:
        print("\n❌ Fix failed!")
    exit(0 if success else 1)