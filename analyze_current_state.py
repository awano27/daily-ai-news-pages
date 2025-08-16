#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze current state of the daily-ai-news site
"""
import re
import requests
from datetime import datetime, timezone, timedelta

def count_x_posts_in_html():
    """Count X posts in current index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences of "Xポスト"
        x_post_count = len(re.findall(r'Xポスト', content))
        
        # Extract the SNS/論文ポスト count from KPI section
        kpi_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">SNS/論文ポスト</div>', content)
        kpi_count = int(kpi_match.group(1)) if kpi_match else 0
        
        # Extract last update time
        update_match = re.search(r'最終更新：([^<]+)', content)
        last_update = update_match.group(1).strip() if update_match else "Unknown"
        
        return x_post_count, kpi_count, last_update
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return 0, 0, "Error"

def fetch_csv_data():
    """Fetch and analyze CSV data"""
    csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    
    try:
        print(f"Fetching CSV from: {csv_url}")
        response = requests.get(csv_url, timeout=30)
        response.raise_for_status()
        
        content = response.text
        lines = content.strip().split('\n')
        total_rows = len(lines)
        
        print(f"Total CSV rows: {total_rows}")
        
        # Show first few rows
        print("Sample CSV data:")
        for i, line in enumerate(lines[:5]):
            print(f"  Row {i+1}: {line[:100]}...")
        
        # Count rows with dates >= 8/14/2025
        jst = timezone(timedelta(hours=9))
        aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=jst)
        
        recent_count = 0
        date_formats = [
            "%B %d, %Y at %I:%M%p",  # "August 10, 2025 at 02:41AM"
            "%B %d, %Y"               # "August 13, 2025"
        ]
        
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.split(',')
                if len(parts) >= 1:
                    date_str = parts[0].strip('"')
                    
                    for fmt in date_formats:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            dt = dt.replace(tzinfo=jst)
                            if dt >= aug14_jst:
                                recent_count += 1
                            break
                        except:
                            continue
        
        print(f"Entries with dates >= Aug 14, 2025: {recent_count}")
        return total_rows, recent_count
        
    except Exception as e:
        print(f"Error fetching CSV: {e}")
        return 0, 0

def main():
    print("=" * 60)
    print("Current State Analysis")
    print("=" * 60)
    
    # Analyze current HTML
    x_posts_html, kpi_count, last_update = count_x_posts_in_html()
    print(f"Current index.html state:")
    print(f"  X posts in HTML: {x_posts_html}")
    print(f"  KPI count: {kpi_count}")
    print(f"  Last update: {last_update}")
    print()
    
    # Analyze CSV data
    print("CSV Data Analysis:")
    total_csv, recent_csv = fetch_csv_data()
    print(f"  Total CSV entries: {total_csv}")
    print(f"  Recent entries (>= Aug 14): {recent_csv}")
    print()
    
    print("=" * 60)
    print("Analysis Summary:")
    print(f"  Current site shows {kpi_count} SNS posts (last updated: {last_update})")
    print(f"  CSV has {total_csv} total entries, {recent_csv} from Aug 14+")
    print(f"  Expected with MAX_ITEMS_PER_CATEGORY=30: up to 30 posts")
    print(f"  Expected filtering: only Aug 14+ posts (8/14+ filter)")
    
    if recent_csv > 0:
        print(f"  ✓ CSV has recent data available for processing")
    else:
        print(f"  ⚠ No recent data found in CSV")
    
    if kpi_count >= 15:
        print(f"  ✓ Site shows good number of posts")
    else:
        print(f"  ⚠ Site shows fewer posts than expected")

if __name__ == "__main__":
    main()