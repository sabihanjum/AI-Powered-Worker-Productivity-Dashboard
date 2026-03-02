"""Generate and seed dummy data for testing and development."""
import random
from datetime import datetime, timedelta
from .database import get_db


def clear_all_data():
    """Clear all existing data from the database."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events")
        cursor.execute("DELETE FROM workers")
        cursor.execute("DELETE FROM workstations")
        conn.commit()


def seed_workers():
    """Seed worker data."""
    workers = [
        ("W1", "John Smith"),
        ("W2", "Sarah Johnson"),
        ("W3", "Michael Chen"),
        ("W4", "Emily Rodriguez"),
        ("W5", "David Kumar"),
        ("W6", "Jessica Williams"),
    ]
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT OR REPLACE INTO workers (worker_id, name) VALUES (?, ?)",
            workers
        )
        conn.commit()
    
    return workers


def seed_workstations():
    """Seed workstation data."""
    workstations = [
        ("S1", "Assembly Station Alpha", "assembly"),
        ("S2", "Assembly Station Beta", "assembly"),
        ("S3", "Quality Control Station", "quality_control"),
        ("S4", "Packaging Station A", "packaging"),
        ("S5", "Packaging Station B", "packaging"),
        ("S6", "Final Inspection Station", "inspection"),
    ]
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT OR REPLACE INTO workstations (station_id, name, type) VALUES (?, ?, ?)",
            workstations
        )
        conn.commit()
    
    return workstations


def seed_events(days=7):
    """
    Generate realistic event data for the past N days.
    
    Assumptions:
    - 8-hour shifts (9 AM to 5 PM)
    - Events are logged every 5-15 minutes
    - Workers are assigned to workstations somewhat consistently
    - Productivity varies throughout the day
    """
    workers = [f"W{i}" for i in range(1, 7)]
    workstations = [f"S{i}" for i in range(1, 7)]
    
    # Assign workers to preferred workstations (with some variation)
    worker_station_mapping = {
        "W1": "S1", "W2": "S2", "W3": "S3",
        "W4": "S4", "W5": "S5", "W6": "S6"
    }
    
    events = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    current_date = start_date
    
    while current_date < end_date:
        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue
        
        # Generate events for each worker during their shift
        for worker_id in workers:
            preferred_station = worker_station_mapping[worker_id]
            
            # Shift starts at 9 AM
            shift_start = current_date.replace(hour=9, minute=0, second=0, microsecond=0)
            shift_end = shift_start + timedelta(hours=8)
            
            current_time = shift_start
            
            while current_time < shift_end:
                # Randomly choose station (80% preferred, 20% other)
                if random.random() < 0.8:
                    station_id = preferred_station
                else:
                    station_id = random.choice([s for s in workstations if s != preferred_station])
                
                # Determine event type based on time of day and randomness
                hour = current_time.hour
                rand_val = random.random()
                
                # More productive in mid-morning and mid-afternoon
                if hour in [10, 11, 14, 15]:
                    if rand_val < 0.65:
                        event_type = "working"
                    elif rand_val < 0.75:
                        event_type = "idle"
                    else:
                        event_type = "product_count"
                # Less productive early morning and late afternoon
                elif hour in [9, 16]:
                    if rand_val < 0.50:
                        event_type = "working"
                    elif rand_val < 0.70:
                        event_type = "idle"
                    else:
                        event_type = "product_count"
                # Lunch time (12-1 PM) - mostly idle
                elif hour == 12:
                    if rand_val < 0.20:
                        event_type = "working"
                    elif rand_val < 0.90:
                        event_type = "idle"
                    else:
                        event_type = "product_count"
                else:
                    if rand_val < 0.60:
                        event_type = "working"
                    elif rand_val < 0.75:
                        event_type = "idle"
                    else:
                        event_type = "product_count"
                
                # Confidence score (AI models aren't perfect)
                confidence = random.uniform(0.75, 0.99)
                
                # Count for product_count events
                count = 0
                if event_type == "product_count":
                    # Realistic production: 1-5 units per event
                    count = random.randint(1, 5)
                
                events.append((
                    current_time.isoformat(),
                    worker_id,
                    station_id,
                    event_type,
                    confidence,
                    count
                ))
                
                # Next event in 5-15 minutes
                current_time += timedelta(minutes=random.randint(5, 15))
        
        current_date += timedelta(days=1)
    
    # Insert events in batches
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT INTO events 
               (timestamp, worker_id, workstation_id, event_type, confidence, count) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            events
        )
        conn.commit()
    
    return len(events)


def seed_all_data(days=7):
    """Seed all data (workers, workstations, and events)."""
    print("Clearing existing data...")
    clear_all_data()
    
    print("Seeding workers...")
    workers = seed_workers()
    print(f"Created {len(workers)} workers")
    
    print("Seeding workstations...")
    workstations = seed_workstations()
    print(f"Created {len(workstations)} workstations")
    
    print(f"Generating events for the past {days} days...")
    event_count = seed_events(days)
    print(f"Created {event_count} events")
    
    print("Data seeding completed successfully!")


if __name__ == "__main__":
    from .database import init_db
    
    # Initialize database
    init_db()
    
    # Seed with 7 days of data
    seed_all_data(days=7)
