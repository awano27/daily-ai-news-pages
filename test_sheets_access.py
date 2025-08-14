#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Google Sheets CSV access
"""
from urllib.request import urlopen
import csv
import io

def test_sheets_access():
    # Convert Google Sheets URL to CSV export URL
    original_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/edit?gid=0#gid=0"
    
    # Extract spreadsheet ID and gid
    sheet_id = "1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg"
    gid = "0"  # Default sheet
    
    # Generate CSV export URL
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    print("=" * 60)
    print("Testing Google Sheets CSV Access")
    print("=" * 60)
    print(f"Original URL: {original_url}")
    print(f"CSV Export URL: {csv_url}")
    
    try:
        print("\nFetching data from Google Sheets...")
        with urlopen(csv_url) as response:
            data = response.read()
            
        print(f"✓ Successfully fetched {len(data)} bytes")
        
        # Decode and parse CSV
        for enc in ('utf-8-sig', 'utf-8', 'cp932'):
            try:
                text = data.decode(enc)
                break
            except Exception:
                continue
        else:
            text = data.decode('utf-8', errors='ignore')
        
        # Parse CSV and show first few rows
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        
        print(f"✓ Parsed {len(rows)} rows")
        
        if rows:
            print("\nFirst 5 rows:")
            for i, row in enumerate(rows[:5]):
                if len(row) >= 2:
                    print(f"  Row {i+1}: {row[0][:30]}... | {row[1][:20]}...")
                else:
                    print(f"  Row {i+1}: {row}")
        
        # Check for recent dates (August 2025)
        recent_count = 0
        for row in rows:
            if row and "August" in str(row[0]) and "2025" in str(row[0]):
                recent_count += 1
        
        print(f"\n✓ Found {recent_count} rows with August 2025 dates")
        
        # Look for X/Twitter URLs
        x_urls = []
        for row in rows:
            for cell in row:
                if "twitter.com" in str(cell) or "x.com" in str(cell):
                    x_urls.append(cell)
        
        print(f"✓ Found {len(x_urls)} X/Twitter URLs")
        
        if x_urls:
            print("\nSample X URLs:")
            for url in x_urls[:3]:
                print(f"  - {url}")
        
        return csv_url
        
    except Exception as e:
        print(f"✗ Error accessing Google Sheets: {e}")
        return None

if __name__ == "__main__":
    test_sheets_access()