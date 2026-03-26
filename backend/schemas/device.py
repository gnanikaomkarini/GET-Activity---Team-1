from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class DeviceBase(BaseModel):
    type: str  # smart_meter, thermostat, plug, energy_monitor
    name: str
    location: Optional[str] = None
    params: Dict[str, Any] = {}


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class DeviceResponse(DeviceBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
