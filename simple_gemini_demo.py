#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def load_env():
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def main():
    print("🧠 Simple Gemini Demo")
    
    # Load environment
    load_env()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    print("✅ API Key found")
    
    try:
        from gemini_url_context import GeminiURLContextClient
        
        client = GeminiURLContextClient()
        print("✅ Gemini client initialized")
        
        # Simple URL context test with AI news
        test_urls = [
            "https://techcrunch.com/category/artificial-intelligence/",
        ]
        
        result = client.generate_from_urls(
            prompt="Analyze this AI news page and provide a brief summary in Japanese.",
            urls=test_urls
        )
        
        if result.get('text'):
            print("\n📝 Analysis Result:")
            print("=" * 50)
            print(result['text'])
            print("=" * 50)
            
            usage = result.get('usage_metadata')
            if usage:
                tokens = getattr(usage, 'total_token_count', 0)
                print(f"📊 Tokens used: {tokens}")
            
            print("🎉 Demo completed successfully!")
        else:
            print(f"❌ Analysis failed: {result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()