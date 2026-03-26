from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models.reading import Reading
from ..models.device import Device
from ..models.user import User
from ..schemas.reading import ReadingCreate, ReadingResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/readings", tags=["readings"])


@router.get("", response_model=List[ReadingResponse])
def get_readings(
    device_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(1000, le=10000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Reading).join(Device).filter(Device.user_id == current_user.id)

    if device_id:
        query = query.filter(Reading.device_id == device_id)
    if start_date:
        query = query.filter(Reading.timestamp >= start_date)
    if end_date:
        query = query.filter(Reading.timestamp <= end_date)

    readings = query.order_by(Reading.timestamp.desc()).limit(limit).all()
    return readings


@router.post("", response_model=ReadingResponse)
def create_reading(
    reading: ReadingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device = (
        db.query(Device)
        .filter(Device.id == reading.device_id, Device.user_id == current_user.id)
        .first()
    )
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    db_reading = Reading(
        device_id=reading.device_id,
        power_watts=reading.power_watts,
        energy_kwh=reading.energy_kwh,
        voltage=reading.voltage,
        current=reading.current,
        metadata=reading.metadata,
        timestamp=reading.timestamp or datetime.utcnow(),
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading


from fastapi import HTTPException
