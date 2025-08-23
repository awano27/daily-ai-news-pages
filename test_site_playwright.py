#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Playwright test for https://awano27.github.io/daily-ai-news-pages/
"""

import asyncio
from playwright.async_api import async_playwright
import sys
import time

async def test_daily_ai_news_site():
    """Test the daily AI news site with Playwright"""
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set to True for headless mode
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🌐 Testing https://awano27.github.io/daily-ai-news-pages/")
            print("=" * 60)
            
            # Navigate to the site
            print("1. 📍 Loading site...")
            response = await page.goto("https://awano27.github.io/daily-ai-news-pages/", wait_until="networkidle")
            print(f"   ✅ Page loaded - Status: {response.status}")
            
            # Wait for page to fully load
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(2)
            
            # Check page title
            title = await page.title()
            print(f"2. 📰 Page title: {title}")
            
            # Check if CSS is loaded correctly
            print("3. 🎨 Checking CSS...")
            css_link = await page.query_selector('link[rel="stylesheet"]')
            if css_link:
                href = await css_link.get_attribute('href')
                print(f"   ✅ CSS file: {href}")
            else:
                print("   ❌ No CSS link found")
            
            # Check for JavaScript
            print("4. 🔧 Checking JavaScript...")
            script_tags = await page.query_selector_all('script')
            inline_scripts = [s for s in script_tags if not await s.get_attribute('src')]
            if inline_scripts:
                print(f"   ✅ Found {len(inline_scripts)} inline script(s)")
            else:
                print("   ❌ No inline scripts found")
            
            # Check for tabs
            print("5. 📑 Checking tab structure...")
            tabs = await page.query_selector_all('.tab')
            if tabs:
                print(f"   ✅ Found {len(tabs)} tab(s)")
                
                # Get tab text
                for i, tab in enumerate(tabs[:4]):  # First 4 tabs
                    tab_text = await tab.inner_text()
                    print(f"     - Tab {i+1}: {tab_text}")
            else:
                print("   ❌ No tabs found")
            
            # Check for tab panels
            print("6. 📋 Checking tab panels...")
            panels = await page.query_selector_all('.tab-panel')
            if panels:
                print(f"   ✅ Found {len(panels)} panel(s)")
            else:
                print("   ❌ No tab panels found")
            
            # Test tab functionality
            print("7. 🖱️ Testing tab functionality...")
            if tabs and len(tabs) >= 2:
                # Click first tab
                await tabs[0].click()
                await asyncio.sleep(1)
                
                # Check if first tab is active
                first_tab_class = await tabs[0].get_attribute('class')
                print(f"   First tab classes: {first_tab_class}")
                
                # Click second tab
                await tabs[1].click()
                await asyncio.sleep(1)
                
                # Check if second tab is active
                second_tab_class = await tabs[1].get_attribute('class')
                print(f"   Second tab classes: {second_tab_class}")
                
                if 'active' in second_tab_class:
                    print("   ✅ Tab switching works!")
                else:
                    print("   ❌ Tab switching may not work")
            
            # Check for articles/content
            print("8. 📰 Checking content...")
            articles = await page.query_selector_all('.news-item')
            if articles:
                print(f"   ✅ Found {len(articles)} news item(s)")
            else:
                print("   ⚠️ No articles found (checking alternative selectors)")
                
                # Try alternative selectors
                alt_selectors = ['.item', '.card', '.post', 'article']
                for selector in alt_selectors:
                    items = await page.query_selector_all(selector)
                    if items:
                        print(f"   ✅ Found {len(items)} items with selector '{selector}'")
                        break
            
            # Check filter controls
            print("9. 🔍 Checking filter controls...")
            filter_btns = await page.query_selector_all('.filter-btn')
            if filter_btns:
                print(f"   ✅ Found {len(filter_btns)} filter button(s)")
            else:
                print("   ❌ No filter buttons found")
            
            # Check search box
            search_box = await page.query_selector('#searchBox')
            if search_box:
                print("   ✅ Search box found")
            else:
                print("   ❌ Search box not found")
            
            # Test responsive design
            print("10. 📱 Testing responsive design...")
            await page.set_viewport_size({"width": 375, "height": 667})  # Mobile size
            await asyncio.sleep(1)
            print("    ✅ Mobile viewport set")
            
            await page.set_viewport_size({"width": 1920, "height": 1080})  # Desktop size
            await asyncio.sleep(1)
            print("    ✅ Desktop viewport restored")
            
            # Take screenshot
            print("11. 📸 Taking screenshot...")
            await page.screenshot(path="site_test_screenshot.png", full_page=True)
            print("    ✅ Screenshot saved as 'site_test_screenshot.png'")
            
            print("\n🎉 Test completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            return False
        
        finally:
            await browser.close()
    
    return True

async def main():
    """Main function"""
    print("🧪 Playwright Test for Daily AI News Site")
    print("Testing https://awano27.github.io/daily-ai-news-pages/")
    print("=" * 60)
    
    try:
        success = await test_daily_ai_news_site()
        if success:
            print("\n✅ All tests completed!")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())