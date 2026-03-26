from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import hashlib
import json

from database import (
    get_db,
    Household,
    Device,
    Reading,
    Analysis,
    SimulationRun,
)
from simulator import simulator

app = FastAPI(title="Energy Efficiency Advisor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Schemas
class HouseholdCreate(BaseModel):
    name: str = "My Home"
    size_sqft: int = 1500
    occupants: int = 4
    location: str = "Unknown"
    tariff_rate: float = 0.12


class HouseholdResponse(BaseModel):
    id: int
    name: str
    size_sqft: int
    occupants: int
    location: str
    tariff_rate: float

    class Config:
        from_attributes = True


class DeviceCreate(BaseModel):
    type: str
    name: str
    location: Optional[str] = "Home"
    params: dict = {}


class DeviceResponse(BaseModel):
    id: int
    household_id: int
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


class SimulationRunResponse(BaseModel):
    id: int
    device_id: int
    scenario: str
    duration_hours: int
    readings_count: int
    avg_power: float
    total_energy: float
    summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


def compute_hash(readings: list) -> str:
    return hashlib.md5(json.dumps(readings, sort_keys=True).encode()).hexdigest()


@app.get("/api/health")
def health():
    return {"status": "healthy"}


# Household endpoints
@app.get("/api/household", response_model=HouseholdResponse)
def get_household(db: Session = Depends(get_db)):
    household = db.query(Household).first()
    if not household:
        household = Household()
        db.add(household)
        db.commit()
        db.refresh(household)
    return household


@app.post("/api/household", response_model=HouseholdResponse)
def save_household(data: HouseholdCreate, db: Session = Depends(get_db)):
    household = db.query(Household).first()
    if not household:
        household = Household()
        db.add(household)

    household.name = data.name
    household.size_sqft = data.size_sqft
    household.occupants = data.occupants
    household.location = data.location
    household.tariff_rate = data.tariff_rate
    household.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(household)
    return household


# Device endpoints
@app.get("/api/devices", response_model=List[DeviceResponse])
def list_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()


@app.post("/api/devices", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    household = db.query(Household).first()
    if not household:
        household = Household()
        db.add(household)
        db.commit()
        db.refresh(household)

    db_device = Device(
        household_id=household.id,
        name=device.name,
        type=device.type,
        location=device.location,
        params=device.params,
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@app.delete("/api/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"message": "Device deleted"}


# Reading endpoints
@app.get("/api/readings", response_model=List[ReadingResponse])
def get_readings(
    device_id: Optional[int] = None, limit: int = 1000, db: Session = Depends(get_db)
):
    query = db.query(Reading)
    if device_id:
        query = query.filter(Reading.device_id == device_id)
    return query.order_by(Reading.timestamp.desc()).limit(limit).all()


@app.delete("/api/readings/{device_id}")
def delete_readings(device_id: int, db: Session = Depends(get_db)):
    db.query(Reading).filter(Reading.device_id == device_id).delete()
    db.commit()
    return {"message": "Readings deleted"}


# Simulation endpoints
@app.post("/api/simulate/generate")
def generate_readings(
    device_id: int,
    count: int = 96,
    household_id: int = 1,
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    household = db.query(Household).filter(Household.id == household_id).first()
    params = device.params.copy() if device.params else {}
    if household:
        params["size_sqft"] = household.size_sqft
        params["occupants"] = household.occupants
        params["tariff_rate"] = household.tariff_rate

    # Clear old readings
    db.query(Reading).filter(Reading.device_id == device_id).delete()

    household_obj = (
        {
            "size_sqft": household.size_sqft if household else 1500,
            "occupants": household.occupants if household else 4,
            "tariff_rate": household.tariff_rate if household else 0.12,
        }
        if household
        else None
    )

    data = simulator.generate_historical(
        device.type, params, max(1, count // 48 + 1), household_obj
    )[:count]

    for r in data:
        reading = Reading(
            device_id=device_id,
            power_watts=r["power_watts"],
            energy_kwh=r["energy_kwh"],
            voltage=r.get("voltage"),
            current=r.get("current"),
            meta={"source": "simulator", "household_id": household_id},
            timestamp=r["timestamp"],
        )
        db.add(reading)

    db.commit()
    return {"message": f"Generated {len(data)} readings", "count": len(data)}


@app.post("/api/simulate/scenario")
def run_scenario(
    device_id: int,
    scenario: str,
    duration_hours: int = 48,
    household_id: int = 1,
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    household = db.query(Household).filter(Household.id == household_id).first()
    params = device.params.copy() if device.params else {}
    if household:
        params["size_sqft"] = household.size_sqft
        params["occupants"] = household.occupants
        params["tariff_rate"] = household.tariff_rate

    # Clear old readings
    db.query(Reading).filter(Reading.device_id == device_id).delete()

    household_obj = (
        {
            "size_sqft": household.size_sqft if household else 1500,
            "occupants": household.occupants if household else 4,
            "tariff_rate": household.tariff_rate if household else 0.12,
        }
        if household
        else None
    )

    data = simulator.run_scenario(
        device.type, params, scenario, duration_hours, household_obj
    )

    for r in data:
        reading = Reading(
            device_id=device_id,
            power_watts=r["power_watts"],
            energy_kwh=r["energy_kwh"],
            voltage=r.get("voltage"),
            current=r.get("current"),
            meta={
                "source": "simulator",
                "scenario": scenario,
                "household_id": household_id,
            },
            timestamp=r["timestamp"],
        )
        db.add(reading)

    db.commit()

    # Calculate summary
    avg_power = sum(r["power_watts"] for r in data) / len(data)
    total_energy = sum(r["energy_kwh"] for r in data)

    cost = total_energy * (household.tariff_rate if household else 0.12)

    summary = f"Ran {scenario} scenario for {duration_hours} hours. "
    summary += f"Generated {len(data)} readings. "
    summary += f"Avg power: {avg_power:.0f}W. Total energy: {total_energy:.1f}kWh. "
    summary += f"Estimated cost: ${cost:.2f}"

    # Save simulation run
    sim_run = SimulationRun(
        device_id=device_id,
        scenario=scenario,
        duration_hours=duration_hours,
        readings_count=len(data),
        avg_power=avg_power,
        total_energy=total_energy,
        summary=summary,
    )
    db.add(sim_run)
    db.commit()

    return {
        "message": f"Ran scenario '{scenario}'",
        "count": len(data),
        "avg_power": avg_power,
        "total_energy": total_energy,
        "estimated_cost": cost,
        "sim_run_id": sim_run.id,
    }


@app.get("/api/simulation-runs", response_model=List[SimulationRunResponse])
def get_simulation_runs(
    device_id: Optional[int] = None, limit: int = 50, db: Session = Depends(get_db)
):
    query = db.query(SimulationRun)
    if device_id:
        query = query.filter(SimulationRun.device_id == device_id)
    return query.order_by(SimulationRun.created_at.desc()).limit(limit).all()


# Device readings with cache check
@app.get("/api/devices/{device_id}/readings")
def get_device_readings(
    device_id: int, limit: int = 200, db: Session = Depends(get_db)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    household = db.query(Household).filter(Household.id == device.household_id).first()

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
        "household": {
            "size_sqft": household.size_sqft if household else 1500,
            "occupants": household.occupants if household else 4,
            "tariff_rate": household.tariff_rate if household else 0.12,
            "location": household.location if household else "Unknown",
        }
        if household
        else None,
        "cached_analysis": existing.analysis_data if existing else None,
    }


@app.post("/api/analysis", response_model=AnalysisResponse)
def save_analysis(req: AnalysisRequest, db: Session = Depends(get_db)):
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


@app.get("/api/analysis")
def get_analysis(db: Session = Depends(get_db)):
    all_readings = db.query(Reading).order_by(Reading.timestamp.desc()).limit(200).all()
    household = db.query(Household).first()
    device_count = db.query(Device).count()
    readings_data = [
        {
            "power_watts": r.power_watts,
            "energy_kwh": r.energy_kwh,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in all_readings
    ]

    if not readings_data:
        return {
            "readings_count": 0,
            "devices_count": device_count,
            "analysis": None,
            "household": {
                "size_sqft": household.size_sqft if household else 1500,
                "occupants": household.occupants if household else 4,
            }
            if household
            else None,
        }

    readings_hash = compute_hash(readings_data)
    existing = (
        db.query(Analysis).filter(Analysis.readings_hash == readings_hash).first()
    )

    if existing:
        return {
            "readings_count": len(readings_data),
            "devices_count": device_count,
            "analysis": existing.analysis_data,
            "cached": True,
            "household": {
                "size_sqft": household.size_sqft if household else 1500,
                "occupants": household.occupants if household else 4,
                "tariff_rate": household.tariff_rate if household else 0.12,
            }
            if household
            else None,
        }

    return {
        "readings_count": len(readings_data),
        "devices_count": device_count,
        "analysis": None,
        "cached": False,
        "household": {
            "size_sqft": household.size_sqft if household else 1500,
            "occupants": household.occupants if household else 4,
            "tariff_rate": household.tariff_rate if household else 0.12,
        }
        if household
        else None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
