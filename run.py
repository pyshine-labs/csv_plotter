#!/usr/bin/env python3
"""
Convenience script to launch the CSV Plotter application.
"""
import sys
import os

# Ensure src is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    from src.main import main
    main()