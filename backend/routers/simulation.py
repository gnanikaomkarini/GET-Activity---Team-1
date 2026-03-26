from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.device import Device
from ..models.reading import Reading
from ..simulator import simulator
from .. import ai

router = APIRouter(prefix="/api", tags=["simulation"])


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


@router.get("/analysis")
def get_analysis(db: Session = Depends(get_db)):
    """
    Single endpoint that returns complete analysis:
    - Summary stats
    - Forecast
    - Anomalies
    - Recommendations
    - Energy score
    """
    readings = db.query(Reading).order_by(Reading.timestamp.desc()).limit(200).all()

    readings_data = [
        {
            "power_watts": r.power_watts,
            "energy_kwh": r.energy_kwh,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in readings
    ]

    devices = db.query(Device).all()
    device_name = devices[0].name if devices else "your home"

    analysis = ai.analyze_energy(readings_data, device_name)

    return {
        "readings_count": len(readings),
        "devices_count": len(devices),
        "analysis": analysis,
    }


@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    """Get AI recommendations (kept for compatibility)"""
    readings = db.query(Reading).order_by(Reading.timestamp.desc()).limit(200).all()

    readings_data = [
        {
            "power_watts": r.power_watts,
            "energy_kwh": r.energy_kwh,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in readings
    ]

    analysis = ai.analyze_energy(readings_data)
    return {"recommendations": analysis.get("recommendations", [])}
