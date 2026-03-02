"""Database configuration and connection management."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DATABASE_URL = "factory_productivity.db"


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Create Workers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            worker_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Workstations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workstations (
            station_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            worker_id TEXT,
            workstation_id TEXT,
            event_type TEXT NOT NULL,
            confidence REAL,
            count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (worker_id) REFERENCES workers(worker_id),
            FOREIGN KEY (workstation_id) REFERENCES workstations(station_id)
        )
    """)
    
    # Create indexes for better query performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_timestamp 
        ON events(timestamp)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_worker 
        ON events(worker_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_workstation 
        ON events(workstation_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_type 
        ON events(event_type)
    """)
    
    conn.commit()
    conn.close()


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
