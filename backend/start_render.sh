#!/usr/bin/env bash
# Backend startup script for Render
# This script initializes the database, seeds data, and starts the server

set -e  # Exit on error

echo "==========================================="
echo "Worker Productivity Backend - Starting"
echo "==========================================="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"
echo "📋 Listing app directory:"
ls -la app/ || echo "⚠️  Warning: app directory not found"
echo ""

# Initialize database and seed data in Python
echo "🔧 Initializing database and seeding data..."
python3 << 'PYTHON_SCRIPT'
import sys
import os

# Ensure we can import from app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
            print("✅ Database seeded successfully!")
        else:
            print(f"✅ Database already contains {count} events")
            
except Exception as e:
    print(f"❌ Error during initialization: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("✨ Initialization complete!")
PYTHON_SCRIPT

if [ $? -ne 0 ]; then
    echo "❌ Database initialization failed"
    exit 1
fi

echo ""
echo "🚀 Starting FastAPI server..."
echo "   Host: 0.0.0.0"
echo "   Port: ${PORT:-8000}"
echo ""

# Start the FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info
