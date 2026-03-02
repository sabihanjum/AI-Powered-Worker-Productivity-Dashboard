"""Pydantic models for API request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Worker(BaseModel):
    worker_id: str
    name: str


class Workstation(BaseModel):
    station_id: str
    name: str
    type: Optional[str] = None


class Event(BaseModel):
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    worker_id: str
    workstation_id: str
    event_type: Literal["working", "idle", "absent", "product_count"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    count: int = Field(default=0, ge=0)


class WorkerMetrics(BaseModel):
    worker_id: str
    name: str
    total_active_time: float  # in hours
    total_idle_time: float  # in hours
    utilization_percentage: float
    total_units_produced: int
    units_per_hour: float


class WorkstationMetrics(BaseModel):
    station_id: str
    name: str
    occupancy_time: float  # in hours
    utilization_percentage: float
    total_units_produced: int
    throughput_rate: float  # units per hour


class FactoryMetrics(BaseModel):
    total_productive_time: float  # in hours
    total_production_count: int
    average_production_rate: float  # units per hour
    average_utilization: float  # percentage


class DashboardResponse(BaseModel):
    factory_metrics: FactoryMetrics
    worker_metrics: list[WorkerMetrics]
    workstation_metrics: list[WorkstationMetrics]
