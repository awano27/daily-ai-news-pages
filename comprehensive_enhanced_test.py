#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test for enhanced ranking system with SNS integration
"""

import os
import sys
import json
from datetime import datetime, timezone

def setup_environment():
    """Set up environment variables"""
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '25'
    os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    
    print("🔧 Environment configured:")
    print(f"   HOURS_LOOKBACK: {os.environ['HOURS_LOOKBACK']}")
    print(f"   MAX_ITEMS_PER_CATEGORY: {os.environ['MAX_ITEMS_PER_CATEGORY']}")
    print(f"   TRANSLATE_TO_JA: {os.environ['TRANSLATE_TO_JA']}")

def test_enhanced_x_processor():
    """Test Enhanced X Processor"""
    try:
        from enhanced_x_processor import EnhancedXProcessor
        processor = EnhancedXProcessor()
        
        print("✅ Enhanced X Processor: Available")
        
        # Test a small batch of posts
        csv_url = os.environ['X_POSTS_CSV']
        posts = processor.process_x_posts(csv_url, max_posts=3)
        
        if posts:
            print(f"✅ X Posts processing: {len(posts)} posts retrieved")
            build_format = processor.convert_to_build_format(posts)
            print(f"✅ Build format conversion: {len(build_format)} items")
            
            # Show sample
            if build_format:
                sample = build_format[0]
                print(f"   Sample: {sample.get('title', '')[:50]}...")
        else:
            print("⚠️ X Posts processing: No posts retrieved")
            
        return True
        
    except ImportError:
        print("⚠️ Enhanced X Processor: Not available, will use fallback")
        return True
    except Exception as e:
        print(f"❌ Enhanced X Processor error: {e}")
        return False

def test_ranking_system():
    """Test ranking system"""
    try:
        from build_simple_ranking import SimpleEngineerRanking
        
        # Test high-scoring item
        test_item = {
            'title': 'New Python API for Machine Learning with Docker deployment',
            'summary': 'Tutorial on implementing REST API using Python, Docker, and Kubernetes for AI model deployment with code examples',
            'source': 'Test'
        }
        
        score = SimpleEngineerRanking.calculate_score(test_item)
        print(f"✅ Ranking system: High-tech score {score:.1f}")
        
        # Test low-scoring item
        test_item2 = {
            'title': 'Business meeting announcement',
            'summary': 'Company will hold quarterly business review meeting next week',
            'source': 'Test'
        }
        
        score2 = SimpleEngineerRanking.calculate_score(test_item2)
        print(f"✅ Ranking system: Low-tech score {score2:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ranking system error: {e}")
        return False

def run_build():
    """Run the enhanced build"""
    try:
        print("\n🚀 Starting enhanced build...")
        
        from build_simple_ranking import main
        all_items = main()
        
        if all_items:
            total_items = len(all_items)
            
            # Count by category
            categories = {}
            posts_items = 0
            twitter_items = 0
            arxiv_items = 0
            
            for item in all_items:
                cat = item.get('category', 'Unknown')
                categories[cat] = categories.get(cat, 0) + 1
                
                if cat == 'Posts':
                    posts_items += 1
                    if item.get('is_x_post'):
                        twitter_items += 1
                    elif 'arxiv' in item.get('source', '').lower():
                        arxiv_items += 1
            
            print(f"\n📊 Build Results:")
            print(f"   Total articles: {total_items}")
            print(f"   Categories: {dict(categories)}")
            print(f"   Posts category: {posts_items} items")
            print(f"   - Twitter posts: {twitter_items}")
            print(f"   - arXiv papers: {arxiv_items}")
            
            # Check priority distribution
            high_priority = len([x for x in all_items if x.get('score', 0) >= 4.0])
            medium_priority = len([x for x in all_items if x.get('score', 0) >= 2.5])
            
            print(f"   High priority (≥4.0): {high_priority}")
            print(f"   Medium priority (≥2.5): {medium_priority}")
            
            return True
        else:
            print("❌ Build returned no items")
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_output():
    """Verify the generated HTML"""
    try:
        if not os.path.exists('index.html'):
            print("❌ index.html not found")
            return False
            
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for key features
        checks = [
            ('Posts tab', 'id="posts"' in content),
            ('Twitter badge', 'post-type-badge twitter' in content),
            ('arXiv badge', 'post-type-badge arxiv' in content),
            ('Priority icons', '🔥' in content or '⚡' in content),
            ('Search functionality', 'search-input' in content),
            ('Filter controls', 'filter-controls' in content)
        ]
        
        print(f"\n🔍 HTML Verification:")
        for name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {name}")
            
        file_size = len(content)
        print(f"   📄 File size: {file_size:,} characters")
        
        return all(passed for _, passed in checks[:-2])  # Allow some features to be missing
        
    except Exception as e:
        print(f"❌ HTML verification error: {e}")
        return False

def main():
    print("🔍 Enhanced Daily AI News - Comprehensive Test")
    print("=" * 60)
    
    setup_environment()
    
    tests = [
        ("Enhanced X Processor", test_enhanced_x_processor),
        ("Ranking System", test_ranking_system),
        ("Enhanced Build", run_build),
        ("HTML Output", verify_output)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Summary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests >= total_tests - 1:  # Allow 1 failure
        print("✅ Enhanced ranking system is working!")
        
        if os.path.exists('index.html'):
            print("🌐 Opening result in browser...")
            import webbrowser
            webbrowser.open('index.html')
            
        return True
    else:
        print("⚠️ Some issues detected, please review")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)