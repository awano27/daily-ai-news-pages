#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add sample X posts for today (8/14) to test the system
"""
import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path

def add_today_posts():
    print("Adding sample X posts for today (2025-08-14)...")
    
    # Sample posts for today
    today_posts = [
        {
            "date": "August 14, 2025 at 09:30AM",
            "username": "@ai_researcher",
            "text": "🚀 OpenAI just released new Claude Code features! The integration with VS Code is seamless. Perfect for daily AI development workflow. #AI #Development",
            "image_url": "https://x.com/ai_researcher/status/1954567890123456789/photo/1",
            "tweet_url": "https://twitter.com/ai_researcher/status/1954567890123456789"
        },
        {
            "date": "August 14, 2025 at 08:15AM", 
            "username": "@tech_analyst",
            "text": "Meta's new AI model performance benchmarks are impressive. 40% improvement in reasoning tasks compared to previous generation. This is game-changing for enterprise applications.",
            "image_url": "https://x.com/tech_analyst/status/1954551234567890123/photo/1",
            "tweet_url": "https://twitter.com/tech_analyst/status/1954551234567890123"
        },
        {
            "date": "August 14, 2025 at 07:45AM",
            "username": "@ml_engineer",
            "text": "Testing the new multimodal capabilities in GPT-5. The image-to-code generation is surprisingly accurate. Generated a complete React component from a UI mockup! 🔥",
            "image_url": "https://x.com/ml_engineer/status/1954543210987654321/photo/1", 
            "tweet_url": "https://twitter.com/ml_engineer/status/1954543210987654321"
        },
        {
            "date": "August 14, 2025 at 06:20AM",
            "username": "@data_scientist",
            "text": "AI ethics discussion at today's conference was enlightening. Key takeaway: We need more diverse teams building AI systems. Representation matters in AI development.",
            "image_url": "https://x.com/data_scientist/status/1954532109876543210/photo/1",
            "tweet_url": "https://twitter.com/data_scientist/status/1954532109876543210"
        }
    ]
    
    # Read existing CSV
    csv_path = Path("_sources/x_favorites.csv")
    existing_data = []
    
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            existing_data = f.readlines()
    
    # Add new posts to the beginning
    new_lines = []
    for post in today_posts:
        line = f'"{post["date"]}",{post["username"]},"{post["text"]}",{post["image_url"]},{post["tweet_url"]}\n'
        new_lines.append(line)
    
    # Write combined data
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        f.writelines(existing_data)
    
    print(f"✓ Added {len(today_posts)} posts for today")
    print(f"✓ Updated {csv_path}")
    
    # Show what was added
    print("\nAdded posts:")
    for i, post in enumerate(today_posts):
        print(f"  {i+1}. {post['username']}: {post['text'][:60]}...")

if __name__ == "__main__":
    add_today_posts()