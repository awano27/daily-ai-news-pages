#!/usr/bin/env python3
import sys

print("Python version:", sys.version)
print("\nChecking dependencies:\n")

try:
    import feedparser
    print("✓ feedparser installed")
except ImportError:
    print("✗ feedparser NOT installed - run: pip install feedparser")

try:
    import yaml
    print("✓ yaml (PyYAML) installed")
except ImportError:
    print("✗ yaml NOT installed - run: pip install pyyaml")

try:
    from deep_translator import GoogleTranslator
    print("✓ deep_translator installed")
except ImportError:
    print("✗ deep_translator NOT installed - run: pip install deep-translator==1.11.4")

print("\nDone!")