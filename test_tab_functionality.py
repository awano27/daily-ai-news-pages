#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright test for Daily AI News tab functionality
"""

import asyncio
from playwright.async_api import async_playwright

async def test_tab_functionality():
    """Test tab switching functionality on the live site"""
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set to True for headless
        context = await browser.new_context()
        page = await context.new_page()
        
        print("🌐 Opening Daily AI News site...")
        await page.goto("https://awano27.github.io/daily-ai-news/")
        
        # Wait for page to load
        await page.wait_for_load_state('networkidle')
        
        print("✅ Page loaded successfully")
        
        # Check if tabs exist
        tabs = await page.query_selector_all('.tab')
        if not tabs:
            print("❌ No tabs found on the page")
            await browser.close()
            return False
            
        print(f"📋 Found {len(tabs)} tabs")
        
        # Test each tab and collect article titles for comparison
        tab_names = ['Business', 'Tools', 'Posts']
        tab_content = {}
        
        for i, tab_name in enumerate(tab_names):
            print(f"\n🔍 Testing {tab_name} tab...")
            
            # Click the tab
            tab_button = tabs[i]
            await tab_button.click()
            
            # Wait a moment for the content to switch
            await page.wait_for_timeout(1000)
            
            # Check if tab is active
            is_active = await tab_button.evaluate('el => el.classList.contains("active")')
            
            if is_active:
                print(f"✅ {tab_name} tab is now active")
            else:
                print(f"❌ {tab_name} tab failed to become active")
                
            # Check if corresponding panel is visible
            panel_id = f"#{tab_name.lower()}"
            panel = await page.query_selector(panel_id)
            
            if panel:
                is_panel_active = await panel.evaluate('el => el.classList.contains("active")')
                
                # Get visible articles (not hidden by display:none)
                visible_articles = await page.evaluate(f'''
                    () => {{
                        const panel = document.querySelector("{panel_id}");
                        if (!panel) return [];
                        const articles = panel.querySelectorAll('.card');
                        return Array.from(articles)
                            .filter(article => getComputedStyle(article).display !== 'none')
                            .map(article => {{
                                const titleEl = article.querySelector('.card-title');
                                const sourceEl = article.querySelector('.meta-source');
                                return {{
                                    title: titleEl ? titleEl.textContent.trim() : 'No title',
                                    source: sourceEl ? sourceEl.textContent.trim() : 'No source',
                                    visible: getComputedStyle(article).display !== 'none'
                                }};
                            }});
                    }}
                ''')
                
                if is_panel_active:
                    print(f"✅ {tab_name} panel is visible")
                    print(f"📄 {len(visible_articles)} visible articles in {tab_name} panel")
                    
                    # Store first few article titles for comparison
                    tab_content[tab_name] = visible_articles[:3]  # First 3 articles
                    print(f"📋 Sample articles in {tab_name}:")
                    for j, article in enumerate(visible_articles[:3]):
                        print(f"   {j+1}. {article['title'][:60]}...")
                        print(f"      Source: {article['source']}")
                else:
                    print(f"❌ {tab_name} panel is not visible")
                    tab_content[tab_name] = []
            else:
                print(f"❌ {tab_name} panel not found")
                tab_content[tab_name] = []
        
        # Compare content between tabs to verify they're actually different
        print(f"\n🔍 Verifying tabs show different content...")
        
        tabs_are_different = True
        for i, tab1 in enumerate(tab_names):
            for j, tab2 in enumerate(tab_names):
                if i >= j:  # Skip same tab and already compared pairs
                    continue
                    
                content1 = [article['title'] for article in tab_content[tab1]]
                content2 = [article['title'] for article in tab_content[tab2]]
                
                # Check if any articles are the same
                common_articles = set(content1) & set(content2)
                
                if content1 == content2:
                    print(f"❌ {tab1} and {tab2} tabs show identical content!")
                    tabs_are_different = False
                elif len(common_articles) > 0:
                    print(f"⚠️  {tab1} and {tab2} tabs have {len(common_articles)} articles in common")
                else:
                    print(f"✅ {tab1} and {tab2} tabs show completely different content")
        
        if not tabs_are_different:
            print(f"❌ CRITICAL: Tab content is not switching properly!")
            return False
        else:
            print(f"✅ All tabs show different content as expected")
        
        # Test filter functionality
        print(f"\n🔍 Testing filter functionality...")
        
        # Check if filter buttons exist
        filter_buttons = await page.query_selector_all('.filter-btn')
        print(f"📋 Found {len(filter_buttons)} filter buttons")
        
        if filter_buttons:
            # Test first filter button (should be "all")
            first_filter = filter_buttons[0]
            filter_text = await first_filter.inner_text()
            print(f"🔍 Testing filter: {filter_text}")
            
            await first_filter.click()
            await page.wait_for_timeout(500)
            
            # Check if filter is active
            is_filter_active = await first_filter.evaluate('el => el.classList.contains("active")')
            if is_filter_active:
                print(f"✅ Filter '{filter_text}' is active")
            else:
                print(f"❌ Filter '{filter_text}' failed to activate")
        
        # Test search functionality if search box exists
        search_box = await page.query_selector('#searchBox')
        if search_box:
            print(f"\n🔍 Testing search functionality...")
            await search_box.fill('AI')
            await page.wait_for_timeout(500)
            
            # Count visible articles after search
            visible_articles = await page.evaluate('''
                () => {
                    const articles = document.querySelectorAll('.card');
                    return Array.from(articles).filter(article => 
                        getComputedStyle(article).display !== 'none'
                    ).length;
                }
            ''')
            print(f"📄 {visible_articles} articles visible after searching 'AI'")
            
            # Clear search
            await search_box.fill('')
            await page.wait_for_timeout(500)
        else:
            print("ℹ️ No search box found")
        
        # Take a screenshot
        await page.screenshot(path='tab_test_screenshot.png')
        print("📸 Screenshot saved as tab_test_screenshot.png")
        
        print(f"\n✅ Tab functionality test completed!")
        
        await browser.close()
        return True

async def main():
    """Main test function"""
    print("🧪 Starting Playwright tab functionality test...")
    print("=" * 50)
    
    try:
        success = await test_tab_functionality()
        if success:
            print("\n🎉 All tests completed successfully!")
        else:
            print("\n❌ Some tests failed!")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())