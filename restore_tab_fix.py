#!/usr/bin/env python3
"""
Restore tab fix after git pull if it was overwritten
"""
import subprocess
import os
from pathlib import Path

def check_and_restore_tab_fix():
    """Check if tab fix exists and restore if needed"""
    
    build_file = Path("build_simple_ranking.py")
    
    if not build_file.exists():
        print("❌ build_simple_ranking.py not found!")
        return False
    
    # Read current file
    with open(build_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if tab fix is present
    has_hidden_logic = 'p.classList.add(\'hidden\')' in content
    has_hidden_class = 'class="tab-panel {hidden}"' in content or 'class="tab-panel ${hidden}"' in content
    has_not_hidden_selector = 'tab-panel:not(.hidden)' in content
    
    print("🔍 Checking tab fix status...")
    print(f"   Hidden logic in JS: {'✅' if has_hidden_logic else '❌'}")
    print(f"   Hidden class in HTML: {'✅' if has_hidden_class else '❌'}")
    print(f"   Not hidden selector: {'✅' if has_not_hidden_selector else '❌'}")
    
    if has_hidden_logic and has_not_hidden_selector:
        print("✅ Tab fix is intact!")
        return True
    
    print("⚠️ Tab fix was overwritten. Restoring...")
    
    # Apply tab fixes
    fixed = False
    
    # Fix 1: JavaScript logic
    if 'p.classList.remove(\'active\')' in content and not has_hidden_logic:
        print("🔧 Fixing JavaScript tab logic...")
        content = content.replace(
            'panels.forEach(p => {\n            p.classList.remove(\'active\');\n          });',
            'panels.forEach(p => {\n            p.classList.add(\'hidden\');\n          });'
        )
        content = content.replace(
            'targetPanel.classList.add(\'active\');',
            'targetPanel.classList.remove(\'hidden\');'
        )
        fixed = True
    
    # Fix 2: HTML generation
    if 'tab-panel active' in content or 'tab-panel {active}' in content:
        print("🔧 Fixing HTML tab panel generation...")
        content = content.replace(
            'active = \'active\' if i == 0 else \'\'',
            'hidden = \'\' if i == 0 else \'hidden\''
        )
        content = content.replace(
            'class="tab-panel {active}"',
            'class="tab-panel {hidden}"'
        )
        content = content.replace(
            'class="tab-panel ${active}"',
            'class="tab-panel ${hidden}"'
        )
        fixed = True
    
    # Fix 3: Filter function
    if 'tab-panel.active' in content and not has_not_hidden_selector:
        print("🔧 Fixing filter function...")
        content = content.replace(
            'tab-panel.active',
            'tab-panel:not(.hidden)'
        )
        fixed = True
    
    if fixed:
        # Add marker comment
        if 'Tab functionality JavaScript fixed' not in content:
            content = content.replace(
                'Force GitHub Actions to use this updated version',
                'Tab functionality JavaScript fixed (hidden class logic)\n- Force GitHub Actions to use this updated version'
            )
        
        # Write fixed content
        with open(build_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Tab fix restored!")
        return True
    else:
        print("❌ Could not restore tab fix automatically")
        return False

def main():
    print("🔧 Tab Fix Restoration Script")
    print("=" * 40)
    
    if check_and_restore_tab_fix():
        print("\n📝 Adding restored changes...")
        subprocess.run(['git', 'add', 'build_simple_ranking.py'], check=True)
        
        print("💾 Committing tab fix...")
        commit_msg = "fix: Restore tab functionality after merge - hidden class logic"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        print("📤 Pushing to GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n🎉 Tab fix successfully restored and deployed!")
        print("🔄 GitHub Actions will rebuild in ~30 seconds")
        print("🌐 Check: https://awano27.github.io/daily-ai-news-pages/")
        return True
    else:
        print("\n❌ Failed to restore tab fix")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)