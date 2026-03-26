from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.reading import Reading
from models.device import Device
from schemas.reading import ReadingResponse

router = APIRouter(prefix="/api/readings", tags=["readings"])


@router.get("", response_model=List[ReadingResponse])
def get_readings(
    device_id: Optional[int] = Query(None),
    limit: int = Query(1000, le=10000),
    db: Session = Depends(get_db),
):
    query = db.query(Reading)

    if device_id:
        query = query.filter(Reading.device_id == device_id)

    readings = query.order_by(Reading.timestamp.desc()).limit(limit).all()
    return readings


@router.delete("/{device_id}")
def delete_device_readings(device_id: int, db: Session = Depends(get_db)):
    db.query(Reading).filter(Reading.device_id == device_id).delete()
    db.commit()
    return {"message": "Readings deleted"}
