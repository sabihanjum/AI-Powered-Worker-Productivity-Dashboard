#!/usr/bin/env python3
"""
Startup script for the Worker Productivity Dashboard backend.
This script initializes the database, seeds data, and starts the FastAPI server.
"""
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("=" * 60)
    print("Worker Productivity Dashboard - Backend Startup")
    print("=" * 60)
    
    # Import after path is set
    from app.database import init_db
    from app.seed_data import seed_all_data
    import uvicorn
    
    # Check if database exists
    db_path = Path("factory_productivity.db")
    db_exists = db_path.exists()
    
    print("\n1. Initializing database...")
    init_db()
    print("   ✓ Database initialized")
    
    # Seed data if database is new or empty
    if not db_exists:
        print("\n2. Database is new. Seeding with sample data...")
        seed_all_data(days=7)
        print("   ✓ Sample data loaded")
    else:
        print("\n2. Database found. Checking for data...")
        from app.database import get_db
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM events")
            count = cursor.fetchone()["count"]
            if count == 0:
                print("   Database is empty. Seeding with sample data...")
                seed_all_data(days=7)
                print("   ✓ Sample data loaded")
            else:
                print(f"   ✓ Database contains {count} events")
    
    print("\n3. Starting FastAPI server...")
    print("   API: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   -" * 60)
    print("   Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
