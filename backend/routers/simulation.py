from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ..database import get_db
from ..models.device import Device
from ..models.reading import Reading
from ..models.user import User
from ..schemas.recommendation import ChatRequest, ChatResponse
from ..auth import get_current_user
from ..simulator import simulator
from .. import ai

router = APIRouter(prefix="/api", tags=["simulation"])


@router.post("/simulate/generate")
def generate_readings(
    device_id: int,
    count: int = 48,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device = (
        db.query(Device)
        .filter(Device.id == device_id, Device.user_id == current_user.id)
        .first()
    )
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    readings_data = simulator.generate_historical(
        device.type, device.params, days=count // 48 + 1
    )[:count]

    readings = []
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
        readings.append(reading)

    db.commit()

    return {"message": f"Generated {len(readings)} readings", "count": len(readings)}


@router.post("/simulate/scenario")
def run_scenario(
    device_id: int,
    scenario: str,
    duration_hours: int = 24,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device = (
        db.query(Device)
        .filter(Device.id == device_id, Device.user_id == current_user.id)
        .first()
    )
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


@router.get("/recommendations")
def get_recommendations(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    readings = (
        db.query(Reading)
        .join(Device)
        .filter(Device.user_id == current_user.id)
        .order_by(Reading.timestamp.desc())
        .limit(100)
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

    user_data = {"home_size": 1500, "occupancy": 2, "location": "unknown"}

    recommendations = ai.generate_recommendations(user_data, readings_data)
    return {"recommendations": recommendations}


@router.get("/forecast")
def get_forecast(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    readings = (
        db.query(Reading)
        .join(Device)
        .filter(Device.user_id == current_user.id)
        .order_by(Reading.timestamp.desc())
        .limit(100)
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

    forecast = ai.generate_forecast(readings_data, {})
    return forecast


@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    readings = (
        db.query(Reading)
        .join(Device)
        .filter(Device.user_id == current_user.id)
        .order_by(Reading.timestamp.desc())
        .limit(48)
        .all()
    )

    avg_consumption = (
        sum(r.power_watts for r in readings) / len(readings) if readings else 0
    )
    total_kwh = sum(r.energy_kwh for r in readings)
    bill_estimate = total_kwh * 0.12  # $0.12/kWh average

    context = {
        "devices": [{"name": d.name, "type": d.type} for d in current_user.devices],
        "avg_consumption": avg_consumption,
        "bill_estimate": bill_estimate,
    }

    response = ai.chat(chat_request.message, context)
    return ChatResponse(response=response)


from fastapi import HTTPException
