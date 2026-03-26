import hashlib
import json
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.device import Device, Reading, Analysis
from ..simulator import simulator
from ..schemas.analysis import AnalysisRequest, AnalysisResponse, GetAnalysisRequest

router = APIRouter(prefix="/api", tags=["simulation"])


def compute_readings_hash(readings: list) -> str:
    data = json.dumps(readings, sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()


@router.post("/simulate/generate")
def generate_readings(
    device_id: int, count: int = Query(96, ge=1, le=1000), db: Session = Depends(get_db)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    readings_data = simulator.generate_historical(
        device.type, device.params, days=max(1, count // 48 + 1)
    )[:count]

    for data in readings_data:
        reading = Reading(
            device_id=device_id,
            power_watts=data["power_watts"],
            energy_kwh=data["energy_kwh"],
            voltage=data.get("voltage"),
            current=data.get("current"),
            metadata={"source": "simulator"},
            timestamp=data["timestamp"],
        )
        db.add(reading)

    db.commit()

    return {
        "message": f"Generated {len(readings_data)} readings",
        "count": len(readings_data),
    }


@router.post("/simulate/scenario")
def run_scenario(
    device_id: int,
    scenario: str,
    duration_hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    readings_data = simulator.run_scenario(
        device.type, device.params, scenario, duration_hours
    )

    for data in readings_data:
        reading = Reading(
            device_id=device_id,
            power_watts=data["power_watts"],
            energy_kwh=data["energy_kwh"],
            voltage=data.get("voltage"),
            current=data.get("current"),
            metadata={"source": "simulator", "scenario": scenario},
            timestamp=data["timestamp"],
        )
        db.add(reading)

    db.commit()

    return {"message": f"Ran scenario '{scenario}'", "count": len(readings_data)}


@router.get("/devices/{device_id}/analysis", response_model=AnalysisResponse)
def get_cached_analysis(device_id: int, db: Session = Depends(get_db)):
    """Get the latest cached analysis for a device."""
    analysis = (
        db.query(Analysis)
        .filter(Analysis.device_id == device_id)
        .order_by(Analysis.created_at.desc())
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404, detail="No cached analysis found. Generate analysis first."
        )

    return analysis


@router.get("/devices/{device_id}/readings")
def get_device_readings(
    device_id: int, limit: int = Query(200, le=1000), db: Session = Depends(get_db)
):
    """Get readings for a device, used by frontend for AI analysis."""
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

    readings_hash = compute_readings_hash(readings_data)

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


@router.post("/analysis", response_model=AnalysisResponse)
def save_analysis(analysis_req: AnalysisRequest, db: Session = Depends(get_db)):
    """Save analysis from frontend (called after AI generates response)."""
    device = db.query(Device).filter(Device.id == analysis_req.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    existing = (
        db.query(Analysis)
        .filter(
            Analysis.device_id == analysis_req.device_id,
            Analysis.readings_hash == analysis_req.readings_hash,
        )
        .first()
    )

    if existing:
        existing.analysis_data = analysis_req.analysis_data
        existing.created_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing

    analysis = Analysis(
        device_id=analysis_req.device_id,
        readings_hash=analysis_req.readings_hash,
        analysis_data=analysis_req.analysis_data,
        readings_count=analysis_req.readings_count,
        cached=True,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


from datetime import datetime
