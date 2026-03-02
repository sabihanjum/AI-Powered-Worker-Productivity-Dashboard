#!/usr/bin/env python3
"""
Simple startup script for Render - initializes DB and starts Uvicorn
"""
import sys
import os
import subprocess

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

print("=" * 50)
print("Worker Productivity Backend - Starting")
print("=" * 50)

# Initialize database and seed data
print("\n🔧 Initializing database and seeding data...")
try:
    from app.database import init_db, get_db
    from app.seed_data import seed_all_data
    
    print("✅ Modules imported successfully")
    
    # Initialize database
    print("📊 Initializing database schema...")
    init_db()
    print("✅ Database initialized")
    
    # Check if we need to seed data
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM events')
        result = cursor.fetchone()
        count = result['count'] if result else 0
        
        if count == 0:
            print("📦 Database is empty. Seeding with sample data...")
            seed_all_data(days=7)
            print("✅ Data seeding completed successfully!")
        else:
            print(f"📊 Database already has {count} events. Skipping seed.")
            
except Exception as e:
    print(f"❌ Error during initialization: {e}")
    sys.exit(1)

# Start the Uvicorn server
print("\n🚀 Starting Uvicorn server...")
port = os.getenv('PORT', '5000')
print(f"📡 Listening on 0.0.0.0:{port}")

os.chdir(backend_dir)
os.execvp('uvicorn', ['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', str(port)])
