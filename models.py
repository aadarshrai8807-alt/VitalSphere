# models.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Ward(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    centroid_lat: float
    centroid_lon: float
    # relationship
    metrics: Optional["WardMetric"] = Relationship(back_populates="ward")

class WardMetric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="ward.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    aqi: float
    green_cover_percent: float
    temperature_c: float
    hospital_visits: int
    reports_count: int

    ward: Optional[Ward] = Relationship(back_populates="metrics")

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ward_id: int = Field(foreign_key="ward.id")
    category: str                # e.g., "air", "waste", "water"
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False
    reporter: Optional[str] = None

class SensorRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str                 # "nasa" or "local-sensor"
    lat: float
    lon: float
    metric: str                 # e.g., "aqi", "temp", "ndvi"
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)