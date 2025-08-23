#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test for https://awano27.github.io/daily-ai-news-pages/
"""

import requests
import re
from bs4 import BeautifulSoup
import sys

def test_site():
    """Test the site with simple HTTP requests"""
    
    print("🧪 Testing https://awano27.github.io/daily-ai-news-pages/")
    print("=" * 60)
    
    try:
        # Request the site
        print("1. 📍 Loading site...")
        response = requests.get("https://awano27.github.io/daily-ai-news-pages/", timeout=15)
        print(f"   ✅ Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Site returned status {response.status_code}")
            return False
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check title
        title = soup.find('title')
        if title:
            print(f"2. 📰 Title: {title.get_text()}")
        else:
            print("2. ❌ No title found")
        
        # Check CSS reference
        print("3. 🎨 Checking CSS...")
        css_links = soup.find_all('link', rel='stylesheet')
        if css_links:
            for css in css_links:
                href = css.get('href', '')
                print(f"   ✅ CSS: {href}")
                if 'style_enhanced_ranking.css' in href:
                    print("   ❌ Found old CSS reference!")
                elif 'style.css' in href:
                    print("   ✅ Correct CSS reference found!")
        else:
            print("   ❌ No CSS links found")
        
        # Check JavaScript
        print("4. 🔧 Checking JavaScript...")
        external_scripts = soup.find_all('script', src=True)
        inline_scripts = soup.find_all('script', src=False)
        
        if external_scripts:
            print(f"   External scripts: {len(external_scripts)}")
            for script in external_scripts:
                src = script.get('src', '')
                print(f"     - {src}")
                if 'script_enhanced_ranking.js' in src:
                    print("     ❌ Found old JS reference!")
        
        if inline_scripts:
            print(f"   ✅ Inline scripts: {len(inline_scripts)}")
            for script in inline_scripts:
                script_content = script.get_text()
                if 'document.addEventListener' in script_content:
                    print("     ✅ Tab functionality JavaScript found!")
                if 'DOMContentLoaded' in script_content:
                    print("     ✅ DOM ready handler found!")
        
        # Check tab structure
        print("5. 📑 Checking tabs...")
        tabs = soup.find_all(class_=re.compile(r'tab'))
        tab_buttons = soup.find_all('button', class_=re.compile(r'tab'))
        
        if tab_buttons:
            print(f"   ✅ Found {len(tab_buttons)} tab buttons")
            for i, tab in enumerate(tab_buttons[:4]):
                tab_text = tab.get_text().strip()
                data_target = tab.get('data-target', '')
                print(f"     - Tab {i+1}: {tab_text} (target: {data_target})")
        else:
            print("   ❌ No tab buttons found")
        
        # Check tab panels
        panels = soup.find_all(class_=re.compile(r'tab-panel'))
        if panels:
            print(f"   ✅ Found {len(panels)} tab panels")
            for i, panel in enumerate(panels[:4]):
                panel_id = panel.get('id', '')
                print(f"     - Panel {i+1}: {panel_id}")
        else:
            print("   ❌ No tab panels found")
        
        # Check filter controls
        print("6. 🔍 Checking filter controls...")
        filter_buttons = soup.find_all('button', class_=re.compile(r'filter-btn'))
        if filter_buttons:
            print(f"   ✅ Found {len(filter_buttons)} filter buttons")
            for btn in filter_buttons[:3]:
                btn_text = btn.get_text().strip()
                print(f"     - {btn_text}")
        else:
            print("   ❌ No filter buttons found")
        
        # Check search box
        search_box = soup.find('input', id='searchBox')
        if search_box:
            print("   ✅ Search box found")
        else:
            print("   ❌ Search box not found")
        
        # Check content
        print("7. 📰 Checking content...")
        
        # Try different content selectors
        content_selectors = [
            ('.news-item', 'news items'),
            ('.item', 'items'),
            ('.card', 'cards'),
            ('article', 'articles'),
            ('.post-item', 'post items')
        ]
        
        total_content = 0
        for selector, name in content_selectors:
            items = soup.select(selector)
            if items:
                print(f"   ✅ Found {len(items)} {name}")
                total_content += len(items)
        
        if total_content == 0:
            print("   ⚠️ No content items found with standard selectors")
        
        # Check for specific content indicators
        if 'AI' in html or 'ニュース' in html:
            print("   ✅ AI/News content detected")
        
        # Check encoding
        print("8. 🔤 Checking encoding...")
        charset = response.encoding
        print(f"   Charset: {charset}")
        
        # Look for Japanese content
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', html):
            print("   ✅ Japanese content detected")
        else:
            print("   ⚠️ No Japanese content found")
        
        # Check meta tags
        print("9. 🏷️ Checking meta tags...")
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            print("   ✅ Viewport meta tag found")
        
        charset_meta = soup.find('meta', attrs={'charset': True})
        if charset_meta:
            charset_value = charset_meta.get('charset', '')
            print(f"   ✅ Charset meta: {charset_value}")
        
        print("\n🎉 Site analysis completed!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    success = test_site()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()