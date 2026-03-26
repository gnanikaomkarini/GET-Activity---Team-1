import os
import sys
import hashlib
import json
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    JSON,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, PARENT_DIR)

DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'energy_advisor.db')}"
)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    location = Column(String, default="Home")
    params = Column(JSON, default={})
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    readings = relationship("Reading", back_populates="device")
    analyses = relationship("Analysis", back_populates="device")


class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    power_watts = Column(Float)
    energy_kwh = Column(Float)
    voltage = Column(Float)
    current = Column(Float)
    meta = Column(JSON, default={})
    device = relationship("Device", back_populates="readings")


class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    readings_hash = Column(String, nullable=False)
    analysis_data = Column(JSON, nullable=False)
    readings_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    cached = Column(Boolean, default=True)
    device = relationship("Device", back_populates="analyses")


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Energy Efficiency Advisor", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DeviceCreate(BaseModel):
    type: str
    name: str
    location: Optional[str] = "Home"
    params: dict = {}


class DeviceResponse(BaseModel):
    id: int
    name: str
    type: str
    location: str
    params: dict
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReadingResponse(BaseModel):
    id: int
    device_id: int
    timestamp: datetime
    power_watts: float
    energy_kwh: float
    voltage: Optional[float] = None
    current: Optional[float] = None

    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    device_id: int
    readings_hash: str
    analysis_data: dict
    readings_count: int


class AnalysisResponse(BaseModel):
    id: int
    device_id: int
    readings_hash: str
    readings_count: int
    created_at: datetime
    cached: bool

    class Config:
        from_attributes = True


import random


class Simulator:
    def __init__(self):
        self.scenarios = {
            "normal": lambda p, t: 1.0,
            "high_consumption": lambda p, t: 1.8,
            "heating": lambda p, t: 1.5,
            "cooling": lambda p, t: 1.7,
            "vacation": lambda p, t: 0.3,
            "weekend": lambda p, t: 1.1,
            "anomaly_spike": lambda p, t: 3.0,
            "anomaly_drop": lambda p, t: 0.2,
        }

    def generate_reading(self, device_type: str, params: dict, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()
        hour = timestamp.hour
        base_power = {
            "smart_meter": 500,
            "thermostat": 1000,
            "plug": 200,
            "energy_monitor": 600,
        }.get(device_type, 500)

        if 7 <= hour <= 9:
            mult = 2.5
        elif 17 <= hour <= 21:
            mult = 3.0
        elif 22 <= hour <= 6:
            mult = 0.4
        else:
            mult = 1.2

        power = base_power * mult * random.uniform(0.9, 1.1)
        return {
            "power_watts": round(power, 2),
            "energy_kwh": round(power / 1000 / 60, 4),
            "voltage": round(random.uniform(118, 122), 1),
            "current": round(power / 120, 2),
        }

    def generate_historical(self, device_type: str, params: dict, days: int = 7):
        readings = []
        now = datetime.utcnow()
        for day in range(days):
            for hour in range(24):
                for minute in [0, 30]:
                    ts = now - timedelta(days=day, hours=23 - hour, minutes=minute)
                    reading = self.generate_reading(device_type, params, ts)
                    reading["timestamp"] = ts
                    readings.append(reading)
        return readings

    def run_scenario(
        self, device_type: str, params: dict, scenario: str, hours: int = 24
    ):
        readings = []
        now = datetime.utcnow()
        scenario_func = self.scenarios.get(scenario, self.scenarios["normal"])
        for i in range(hours * 2):
            ts = now - timedelta(minutes=(hours * 60 - i * 30))
            reading = self.generate_reading(device_type, params, ts)
            reading["power_watts"] *= scenario_func(params, ts)
            reading["energy_kwh"] *= scenario_func(params, ts)
            reading["timestamp"] = ts
            readings.append(reading)
        return readings


simulator = Simulator()
from datetime import timedelta


def compute_hash(readings: list) -> str:
    return hashlib.md5(json.dumps(readings, sort_keys=True).encode()).hexdigest()


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/devices", response_model=List[DeviceResponse])
def list_devices(db=Depends(get_db)):
    return db.query(Device).all()


@app.post("/api/devices", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db=Depends(get_db)):
    db_device = Device(
        name=device.name,
        type=device.type,
        location=device.location,
        params=device.params,
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@app.get("/api/devices/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db=Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@app.delete("/api/devices/{device_id}")
def delete_device(device_id: int, db=Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"message": "Device deleted"}


@app.get("/api/readings", response_model=List[ReadingResponse])
def get_readings(
    device_id: Optional[int] = None, limit: int = 1000, db=Depends(get_db)
):
    query = db.query(Reading)
    if device_id:
        query = query.filter(Reading.device_id == device_id)
    return query.order_by(Reading.timestamp.desc()).limit(limit).all()


@app.delete("/api/readings/{device_id}")
def delete_readings(device_id: int, db=Depends(get_db)):
    db.query(Reading).filter(Reading.device_id == device_id).delete()
    db.commit()
    return {"message": "Readings deleted"}


@app.post("/api/simulate/generate")
def generate_readings(device_id: int, count: int = 96, db=Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    data = simulator.generate_historical(
        device.type, device.params, max(1, count // 48 + 1)
    )[:count]
    for r in data:
        reading = Reading(
            device_id=device_id,
            power_watts=r["power_watts"],
            energy_kwh=r["energy_kwh"],
            voltage=r.get("voltage"),
            current=r.get("current"),
            meta={"source": "simulator"},
            timestamp=r["timestamp"],
        )
        db.add(reading)
    db.commit()
    return {"message": f"Generated {len(data)} readings", "count": len(data)}


@app.post("/api/simulate/scenario")
def run_scenario(
    device_id: int, scenario: str, duration_hours: int = 24, db=Depends(get_db)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    data = simulator.run_scenario(device.type, device.params, scenario, duration_hours)
    for r in data:
        reading = Reading(
            device_id=device_id,
            power_watts=r["power_watts"],
            energy_kwh=r["energy_kwh"],
            voltage=r.get("voltage"),
            current=r.get("current"),
            meta={"source": "simulator", "scenario": scenario},
            timestamp=r["timestamp"],
        )
        db.add(reading)
    db.commit()
    return {"message": f"Ran scenario '{scenario}'", "count": len(data)}


@app.get("/api/devices/{device_id}/readings")
def get_device_readings(device_id: int, limit: int = 200, db=Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    readings = (
        db.query(Reading)
        .filter(Reading.device_id == device_id)
        .order_by(Reading.timestamp.desc())
        .limit(limit)
        .all()
    )
    readings_data = [
        {
            "power_watts": r.power_watts,
            "energy_kwh": r.energy_kwh,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in readings
    ]
    readings_hash = compute_hash(readings_data)
    existing = (
        db.query(Analysis)
        .filter(
            Analysis.device_id == device_id, Analysis.readings_hash == readings_hash
        )
        .first()
    )
    return {
        "readings": readings_data,
        "readings_hash": readings_hash,
        "readings_count": len(readings_data),
        "device_name": device.name,
        "cached_analysis": existing.analysis_data if existing else None,
    }


@app.post("/api/analysis", response_model=AnalysisResponse)
def save_analysis(req: AnalysisRequest, db=Depends(get_db)):
    device = db.query(Device).filter(Device.id == req.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    existing = (
        db.query(Analysis)
        .filter(
            Analysis.device_id == req.device_id,
            Analysis.readings_hash == req.readings_hash,
        )
        .first()
    )
    if existing:
        existing.analysis_data = req.analysis_data
        existing.created_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing
    analysis = Analysis(
        device_id=req.device_id,
        readings_hash=req.readings_hash,
        analysis_data=req.analysis_data,
        readings_count=req.readings_count,
        cached=True,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


if os.path.exists(os.path.join(PARENT_DIR, "frontend")):
    app.mount(
        "/",
        StaticFiles(directory=os.path.join(PARENT_DIR, "frontend"), html=True),
        name="frontend",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
