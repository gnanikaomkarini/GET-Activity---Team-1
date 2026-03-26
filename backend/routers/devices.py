from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.device import Device
from ..schemas.device import DeviceCreate, DeviceResponse

router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get("", response_model=List[DeviceResponse])
def list_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return devices


@router.post("", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
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


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"message": "Device deleted"}
