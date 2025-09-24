# main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, get_session
import crud
from models import Ward, WardMetric, Report, SensorRecord
from typing import List
import uvicorn
from datetime import datetime

app = FastAPI(title="VitalSphere Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# init DB
init_db()

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Overview (cards in top row)
@app.get("/overview")
def overview():
    data = crud.overall_overview()
    return {
        "average_aqi": data["avg_aqi"],
        "green_cover_percent": data["avg_green"],
        "hospital_visits_today": data["hospital_visits"],
        "active_reports": data["active_reports"]
    }

# List wards (for dropdowns and ward list)
@app.get("/wards", response_model=List[Ward])
def list_wards():
    return crud.list_wards()

# Ward detail + latest metrics
@app.get("/wards/{ward_id}")
def ward_detail(ward_id: int):
    w = crud.get_ward(ward_id)
    if not w:
        raise HTTPException(status_code=404, detail="Ward not found")
    m = crud.latest_metric_for_ward(ward_id)
    reports = []
    with get_session() as sess:
        from sqlmodel import select
        q = select(Report).where(Report.ward_id==ward_id).order_by(Report.created_at.desc()).limit(10)
        reports = sess.exec(q).all()
    return {"ward": w, "metric": m, "recent_reports": reports}

# GeoJSON for map layer
@app.get("/map.geojson")
def map_geojson(metric: str = "aqi"):
    return crud.map_geojson(metric=metric)

# Leaderboard
@app.get("/leaderboard")
def get_leaderboard(top_n: int = 10):
    return {"leaderboard": crud.leaderboard(top_n)}

# Reports endpoints
@app.post("/reports")
def create_report(ward_id:int, category:str, description:str=None, reporter:str=None):
    # basic validation
    w = crud.get_ward(ward_id)
    if not w:
        raise HTTPException(status_code=404, detail="Ward not found")
    r = crud.add_report(ward_id, category, description, reporter)
    return r

@app.get("/reports")
def list_reports(limit:int=100):
    with get_session() as sess:
        from sqlmodel import select
        rows = sess.exec(select(Report).order_by(Report.created_at.desc()).limit(limit)).all()
        return rows

# Add sensor data (ingest API)
@app.post("/sensor")
def add_sensor_record(source:str, lat:float, lon:float, metric:str, value:float):
    rec = SensorRecord(source=source, lat=lat, lon=lon, metric=metric, value=value)
    with get_session() as sess:
        sess.add(rec); sess.commit(); sess.refresh(rec)
    return rec

# Simulate: quick endpoint to recompute leaderboard or run a scenario (simplified)
@app.post("/simulator/run")
def run_simulation(action: str = "recompute"):
    # For demo, just return leaderboard snapshot or simple advice
    if action == "recompute":
        lb = crud.leaderboard(10)
        return {"status": "ok", "leaderboard_snapshot": lb}
    return {"status":"unknown_action"}

if _name_ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=8000)