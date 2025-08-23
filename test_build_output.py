#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify build_simple_ranking.py produces correct HTML
"""

import sys
import os
from pathlib import Path

def check_build_script():
    """Check if build script has correct references"""
    build_script = Path("build_simple_ranking.py")
    
    if not build_script.exists():
        print("❌ build_simple_ranking.py not found!")
        return False
    
    print("🔍 Checking build_simple_ranking.py...")
    
    with open(build_script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check CSS reference
    if 'style_enhanced_ranking.css' in content:
        print("❌ Found incorrect CSS reference: style_enhanced_ranking.css")
        return False
    elif 'style.css' in content:
        print("✅ Correct CSS reference found: style.css")
    else:
        print("⚠️ No CSS reference found")
    
    # Check JS reference
    if 'script_enhanced_ranking.js' in content:
        print("❌ Found external JS reference: script_enhanced_ranking.js")
        return False
    elif '<script>' in content and 'document.addEventListener' in content:
        print("✅ Inline JavaScript found")
    else:
        print("⚠️ No JavaScript found")
    
    return True

def simulate_build_output():
    """Simulate what the build script would produce"""
    print("\n🔨 Simulating build output...")
    
    # Import the build script's HTML generation function
    try:
        sys.path.append('.')
        from build_simple_ranking import generate_html_template
        
        # Generate sample HTML
        sample_data = {
            'business': [],
            'tools': [],  
            'posts': [],
            'x_posts': []
        }
        
        html = generate_html_template(sample_data)
        
        # Check the generated HTML
        if 'style_enhanced_ranking.css' in html:
            print("❌ Generated HTML contains incorrect CSS reference!")
            return False
        elif 'style.css' in html:
            print("✅ Generated HTML has correct CSS reference")
        
        if 'script_enhanced_ranking.js' in html:
            print("❌ Generated HTML contains external JS reference!")
            return False
        elif 'document.addEventListener' in html:
            print("✅ Generated HTML has inline JavaScript")
        
        return True
        
    except ImportError as e:
        print(f"⚠️ Could not import build script: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking build output: {e}")
        return False

def main():
    print("🧪 Testing Build Output")
    print("=" * 30)
    
    # Check build script
    if not check_build_script():
        print("\n❌ Build script check failed!")
        return False
    
    # Test build output
    if not simulate_build_output():
        print("\n❌ Build output test failed!")
        return False
    
    print("\n✅ All tests passed!")
    print("The build script should produce correct HTML with:")
    print("  - CSS reference: style.css")
    print("  - Inline JavaScript for tab functionality")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)