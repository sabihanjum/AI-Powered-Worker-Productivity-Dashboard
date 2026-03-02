"""Compute productivity metrics from event data."""
from datetime import datetime, timedelta
from typing import Dict, List
from .database import get_db
from .models import WorkerMetrics, WorkstationMetrics, FactoryMetrics


def calculate_time_duration_hours(events: List[Dict]) -> Dict[str, float]:
    """
    Calculate time durations for different event types.
    
    Assumption: Each event represents the start of that state.
    The duration is calculated as the time until the next event.
    If there's no next event, we assume a default duration of 10 minutes.
    """
    durations = {"working": 0.0, "idle": 0.0, "absent": 0.0}
    
    if not events:
        return durations
    
    # Sort events by timestamp
    sorted_events = sorted(events, key=lambda x: x["timestamp"])
    
    for i, event in enumerate(sorted_events):
        event_type = event["event_type"]
        
        # Skip product_count events for duration calculation
        if event_type == "product_count":
            continue
        
        # Calculate duration until next event
        if i < len(sorted_events) - 1:
            current_time = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            next_time = datetime.fromisoformat(sorted_events[i + 1]["timestamp"].replace("Z", "+00:00"))
            duration_hours = (next_time - current_time).total_seconds() / 3600
            
            # Cap duration at 2 hours to handle anomalies (e.g., overnight gaps)
            duration_hours = min(duration_hours, 2.0)
        else:
            # Last event: assume 10 minutes duration
            duration_hours = 10 / 60
        
        if event_type in durations:
            durations[event_type] += duration_hours
    
    return durations


def get_worker_metrics(worker_id: str = None) -> List[WorkerMetrics]:
    """
    Calculate metrics for workers.
    
    If worker_id is provided, return metrics for that worker only.
    Otherwise, return metrics for all workers.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get all workers or specific worker
        if worker_id:
            cursor.execute("SELECT * FROM workers WHERE worker_id = ?", (worker_id,))
        else:
            cursor.execute("SELECT * FROM workers")
        
        workers = cursor.fetchall()
        metrics_list = []
        
        for worker in workers:
            wid = worker["worker_id"]
            name = worker["name"]
            
            # Get all events for this worker
            cursor.execute(
                "SELECT * FROM events WHERE worker_id = ? ORDER BY timestamp",
                (wid,)
            )
            events = [dict(row) for row in cursor.fetchall()]
            
            # Calculate time durations
            time_durations = calculate_time_duration_hours(events)
            
            total_active_time = time_durations["working"]
            total_idle_time = time_durations["idle"]
            
            # Calculate utilization percentage
            total_time = total_active_time + total_idle_time
            utilization = (total_active_time / total_time * 100) if total_time > 0 else 0
            
            # Count total units produced
            cursor.execute(
                """SELECT SUM(count) as total FROM events 
                   WHERE worker_id = ? AND event_type = 'product_count'""",
                (wid,)
            )
            result = cursor.fetchone()
            total_units = result["total"] if result["total"] else 0
            
            # Calculate units per hour
            units_per_hour = (total_units / total_active_time) if total_active_time > 0 else 0
            
            metrics_list.append(WorkerMetrics(
                worker_id=wid,
                name=name,
                total_active_time=round(total_active_time, 2),
                total_idle_time=round(total_idle_time, 2),
                utilization_percentage=round(utilization, 2),
                total_units_produced=total_units,
                units_per_hour=round(units_per_hour, 2)
            ))
        
        return metrics_list


def get_workstation_metrics(station_id: str = None) -> List[WorkstationMetrics]:
    """
    Calculate metrics for workstations.
    
    If station_id is provided, return metrics for that station only.
    Otherwise, return metrics for all workstations.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get all workstations or specific workstation
        if station_id:
            cursor.execute("SELECT * FROM workstations WHERE station_id = ?", (station_id,))
        else:
            cursor.execute("SELECT * FROM workstations")
        
        workstations = cursor.fetchall()
        metrics_list = []
        
        for station in workstations:
            sid = station["station_id"]
            name = station["name"]
            
            # Get all events for this workstation
            cursor.execute(
                "SELECT * FROM events WHERE workstation_id = ? ORDER BY timestamp",
                (sid,)
            )
            events = [dict(row) for row in cursor.fetchall()]
            
            # Calculate time durations
            time_durations = calculate_time_duration_hours(events)
            
            # Occupancy time is when someone is working at this station
            occupancy_time = time_durations["working"]
            
            # Total observation time (working + idle)
            total_time = time_durations["working"] + time_durations["idle"]
            
            # Utilization percentage
            utilization = (occupancy_time / total_time * 100) if total_time > 0 else 0
            
            # Count total units produced at this workstation
            cursor.execute(
                """SELECT SUM(count) as total FROM events 
                   WHERE workstation_id = ? AND event_type = 'product_count'""",
                (sid,)
            )
            result = cursor.fetchone()
            total_units = result["total"] if result["total"] else 0
            
            # Calculate throughput rate (units per hour)
            throughput = (total_units / occupancy_time) if occupancy_time > 0 else 0
            
            metrics_list.append(WorkstationMetrics(
                station_id=sid,
                name=name,
                occupancy_time=round(occupancy_time, 2),
                utilization_percentage=round(utilization, 2),
                total_units_produced=total_units,
                throughput_rate=round(throughput, 2)
            ))
        
        return metrics_list


def get_factory_metrics() -> FactoryMetrics:
    """Calculate factory-wide metrics."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get all events
        cursor.execute("SELECT * FROM events ORDER BY timestamp")
        events = [dict(row) for row in cursor.fetchall()]
        
        # Calculate total productive time across all workers
        cursor.execute("SELECT DISTINCT worker_id FROM events")
        workers = cursor.fetchall()
        
        total_productive_time = 0.0
        for worker in workers:
            wid = worker["worker_id"]
            cursor.execute(
                "SELECT * FROM events WHERE worker_id = ? ORDER BY timestamp",
                (wid,)
            )
            worker_events = [dict(row) for row in cursor.fetchall()]
            time_durations = calculate_time_duration_hours(worker_events)
            total_productive_time += time_durations["working"]
        
        # Total production count
        cursor.execute(
            "SELECT SUM(count) as total FROM events WHERE event_type = 'product_count'"
        )
        result = cursor.fetchone()
        total_production = result["total"] if result["total"] else 0
        
        # Average production rate
        avg_production_rate = (total_production / total_productive_time) if total_productive_time > 0 else 0
        
        # Average utilization across workers
        worker_metrics = get_worker_metrics()
        avg_utilization = (
            sum(w.utilization_percentage for w in worker_metrics) / len(worker_metrics)
            if worker_metrics else 0
        )
        
        return FactoryMetrics(
            total_productive_time=round(total_productive_time, 2),
            total_production_count=total_production,
            average_production_rate=round(avg_production_rate, 2),
            average_utilization=round(avg_utilization, 2)
        )
