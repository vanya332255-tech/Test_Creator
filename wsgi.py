#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import create_app

# Create Flask app
app = create_app()

if __name__ == "__main__":
    app.run()
