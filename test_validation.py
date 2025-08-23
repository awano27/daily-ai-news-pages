#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick validation test for build_simple_ranking.py
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        # Test basic Python modules
        import json, time, html, csv, io
        print("✅ Basic Python modules: OK")
        
        # Test scientific/data modules
        import yaml, feedparser, requests
        print("✅ Scientific modules: OK")
        
        # Test enhanced X processor
        try:
            from enhanced_x_processor import EnhancedXProcessor
            print("✅ Enhanced X Processor: Available")
        except ImportError:
            print("⚠️ Enhanced X Processor: Not available (will use fallback)")
        
        # Test translation module
        try:
            from deep_translator import GoogleTranslator
            print("✅ Translation module: Available")
        except ImportError:
            print("⚠️ Translation module: Not available")
            
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_ranking_system():
    """Test the ranking system class"""
    try:
        # Import the ranking system
        sys.path.append(os.getcwd())
        from build_simple_ranking import SimpleEngineerRanking
        
        # Test score calculation
        test_item = {
            'title': 'New Python API for Machine Learning',
            'summary': 'This tutorial shows how to implement a REST API using Python and Docker for AI model deployment.',
            'source': 'Test'
        }
        
        score = SimpleEngineerRanking.calculate_score(test_item)
        print(f"✅ Ranking system: Score calculation works (score: {score:.1f})")
        
        # Test priority classification
        icon, cls, text = SimpleEngineerRanking.get_priority(score)
        print(f"✅ Priority system: {icon} {text} ({cls})")
        
        return True
        
    except Exception as e:
        print(f"❌ Ranking system error: {e}")
        return False

def test_enhanced_x_processor():
    """Test Enhanced X Processor functionality"""
    try:
        from enhanced_x_processor import EnhancedXProcessor
        
        processor = EnhancedXProcessor()
        print("✅ Enhanced X Processor: Instance created successfully")
        
        # Test content hash creation
        test_text = "This is a test tweet about AI and machine learning"
        hash_val = processor.create_content_hash(test_text)
        print(f"✅ Content hash: {hash_val}")
        
        return True
        
    except ImportError:
        print("⚠️ Enhanced X Processor: Not available (this is OK, fallback will be used)")
        return True
    except Exception as e:
        print(f"❌ Enhanced X Processor error: {e}")
        return False

def main():
    print("🔍 Daily AI News - Validation Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
        
    if test_ranking_system():
        tests_passed += 1
        
    if test_enhanced_x_processor():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("✅ All systems ready for build!")
        return True
    else:
        print("⚠️ Some issues detected, but build may still work")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)