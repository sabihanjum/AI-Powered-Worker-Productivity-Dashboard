#!/usr/bin/env python3
"""
Simple startup script for Render - initializes DB and starts Uvicorn
Run from backend directory
"""
import sys
import os

print("=" * 50)
print("Worker Productivity Backend - Starting")
print("=" * 50)
print(f"📁 Current directory: {os.getcwd()}")

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
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Start the Uvicorn server
print("\n🚀 Starting Uvicorn server...")
port = os.getenv('PORT', '5000')
print(f"📡 Listening on 0.0.0.0:{port}")

os.execvp('uvicorn', ['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', str(port)])
