#!/usr/bin/env bash
# Render start script for backend

set -o errexit

echo "Starting Worker Productivity Dashboard Backend..."

# Run database initialization and seeding
python -c "
from app.database import init_db
from app.seed_data import seed_all_data
from app.database import get_db

print('Initializing database...')
init_db()

# Check if database needs seeding
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM events')
    count = cursor.fetchone()['count']
    if count == 0:
        print('Database is empty. Seeding with data...')
        seed_all_data(days=7)
        print('Database seeded successfully!')
    else:
        print(f'Database already contains {count} events')
"

# Start the FastAPI server
echo "Starting FastAPI server on port ${PORT:-8000}..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
