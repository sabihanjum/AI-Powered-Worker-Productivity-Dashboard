"""FastAPI application for Worker Productivity Dashboard."""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import uvicorn

from .database import init_db, get_db
from .models import (
    Worker, Workstation, Event,
    WorkerMetrics, WorkstationMetrics, FactoryMetrics,
    DashboardResponse
)
from .metrics import get_worker_metrics, get_workstation_metrics, get_factory_metrics
from .seed_data import seed_all_data

# Initialize FastAPI app
app = FastAPI(
    title="Worker Productivity Dashboard API",
    description="API for AI-powered worker productivity monitoring system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup."""
    init_db()
    
    # Check if database has data, if not, seed it
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM events")
        result = cursor.fetchone()
        
        if result["count"] == 0:
            print("Database is empty. Seeding with initial data...")
            seed_all_data(days=7)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Worker Productivity Dashboard API",
        "version": "1.0.0"
    }


@app.get("/api/workers", response_model=List[Worker])
async def list_workers():
    """Get list of all workers."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT worker_id, name FROM workers")
        workers = [Worker(**dict(row)) for row in cursor.fetchall()]
        return workers


@app.get("/api/workstations", response_model=List[Workstation])
async def list_workstations():
    """Get list of all workstations."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT station_id, name, type FROM workstations")
        workstations = [Workstation(**dict(row)) for row in cursor.fetchall()]
        return workstations


@app.post("/api/events", status_code=201)
async def ingest_event(event: Event):
    """
    Ingest a new AI-generated event from CCTV system.
    
    Handles:
    - Duplicate detection: Checks for events with same timestamp, worker, station, and type
    - Out-of-order timestamps: Stores all events regardless of order
    - Validation: Ensures worker and workstation exist
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Validate worker exists
        cursor.execute("SELECT worker_id FROM workers WHERE worker_id = ?", (event.worker_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Worker {event.worker_id} not found")
        
        # Validate workstation exists
        cursor.execute("SELECT station_id FROM workstations WHERE station_id = ?", (event.workstation_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Workstation {event.workstation_id} not found")
        
        # Check for duplicate event
        cursor.execute(
            """SELECT event_id FROM events 
               WHERE timestamp = ? AND worker_id = ? AND workstation_id = ? AND event_type = ?""",
            (event.timestamp, event.worker_id, event.workstation_id, event.event_type)
        )
        
        if cursor.fetchone():
            return {
                "status": "duplicate",
                "message": "Event already exists, skipping insertion"
            }
        
        # Insert event
        cursor.execute(
            """INSERT INTO events 
               (timestamp, worker_id, workstation_id, event_type, confidence, count) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (event.timestamp, event.worker_id, event.workstation_id, 
             event.event_type, event.confidence, event.count)
        )
        conn.commit()
        
        return {
            "status": "success",
            "message": "Event ingested successfully",
            "event_id": cursor.lastrowid
        }


@app.post("/api/events/batch", status_code=201)
async def ingest_events_batch(events: List[Event]):
    """
    Ingest multiple events in a batch.
    Useful for handling intermittent connectivity - edge devices can queue and send in batches.
    """
    success_count = 0
    duplicate_count = 0
    error_count = 0
    errors = []
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        for event in events:
            try:
                # Validate worker exists
                cursor.execute("SELECT worker_id FROM workers WHERE worker_id = ?", (event.worker_id,))
                if not cursor.fetchone():
                    error_count += 1
                    errors.append(f"Worker {event.worker_id} not found")
                    continue
                
                # Validate workstation exists
                cursor.execute("SELECT station_id FROM workstations WHERE station_id = ?", (event.workstation_id,))
                if not cursor.fetchone():
                    error_count += 1
                    errors.append(f"Workstation {event.workstation_id} not found")
                    continue
                
                # Check for duplicate
                cursor.execute(
                    """SELECT event_id FROM events 
                       WHERE timestamp = ? AND worker_id = ? AND workstation_id = ? AND event_type = ?""",
                    (event.timestamp, event.worker_id, event.workstation_id, event.event_type)
                )
                
                if cursor.fetchone():
                    duplicate_count += 1
                    continue
                
                # Insert event
                cursor.execute(
                    """INSERT INTO events 
                       (timestamp, worker_id, workstation_id, event_type, confidence, count) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (event.timestamp, event.worker_id, event.workstation_id, 
                     event.event_type, event.confidence, event.count)
                )
                success_count += 1
                
            except Exception as e:
                error_count += 1
                errors.append(str(e))
        
        conn.commit()
    
    return {
        "status": "completed",
        "total": len(events),
        "success": success_count,
        "duplicates": duplicate_count,
        "errors": error_count,
        "error_details": errors[:10]  # Return first 10 errors
    }


@app.get("/api/metrics/dashboard", response_model=DashboardResponse)
async def get_dashboard_metrics():
    """Get all metrics for the dashboard."""
    factory_metrics = get_factory_metrics()
    worker_metrics = get_worker_metrics()
    workstation_metrics = get_workstation_metrics()
    
    return DashboardResponse(
        factory_metrics=factory_metrics,
        worker_metrics=worker_metrics,
        workstation_metrics=workstation_metrics
    )


@app.get("/api/metrics/workers", response_model=List[WorkerMetrics])
async def get_workers_metrics(worker_id: Optional[str] = None):
    """Get metrics for all workers or a specific worker."""
    return get_worker_metrics(worker_id)


@app.get("/api/metrics/workstations", response_model=List[WorkstationMetrics])
async def get_workstations_metrics(station_id: Optional[str] = None):
    """Get metrics for all workstations or a specific workstation."""
    return get_workstation_metrics(station_id)


@app.get("/api/metrics/factory", response_model=FactoryMetrics)
async def get_factory_metrics_endpoint():
    """Get factory-wide metrics."""
    return get_factory_metrics()


@app.post("/api/admin/seed-data")
async def seed_database(days: int = 7):
    """
    Admin endpoint to refresh dummy data.
    This allows evaluators to reset or refresh the database without manual intervention.
    """
    try:
        seed_all_data(days=days)
        return {
            "status": "success",
            "message": f"Database seeded with {days} days of data"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/stats")
async def get_database_stats():
    """Get basic statistics about the database."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM workers")
        worker_count = cursor.fetchone()["count"]
        
        cursor.execute("SELECT COUNT(*) as count FROM workstations")
        workstation_count = cursor.fetchone()["count"]
        
        cursor.execute("SELECT COUNT(*) as count FROM events")
        event_count = cursor.fetchone()["count"]
        
        cursor.execute("SELECT MIN(timestamp) as first, MAX(timestamp) as last FROM events")
        time_range = cursor.fetchone()
        
        return {
            "workers": worker_count,
            "workstations": workstation_count,
            "events": event_count,
            "data_range": {
                "first_event": time_range["first"],
                "last_event": time_range["last"]
            }
        }


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
