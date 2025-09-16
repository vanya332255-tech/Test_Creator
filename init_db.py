#!/usr/bin/env python3
"""
Database initialization script for Render deployment
"""
import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import create_app
from app.extensions import db, migrate

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        print("Initializing database...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created!")
        
        # Run migrations
        try:
            migrate.upgrade()
            print("✅ Migrations applied!")
        except Exception as e:
            print(f"⚠️ Migration warning: {e}")
        
        print("🎉 Database initialization complete!")
