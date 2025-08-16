#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Import and run the comprehensive dashboard
try:
    import generate_comprehensive_dashboard
    print("Running comprehensive dashboard generation...")
    success = generate_comprehensive_dashboard.main()
    if success:
        print("Dashboard generated successfully!")
    else:
        print("Dashboard generation failed.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()