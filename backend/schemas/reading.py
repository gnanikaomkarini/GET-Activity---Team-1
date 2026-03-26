from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class ReadingBase(BaseModel):
    device_id: int
    power_watts: float
    energy_kwh: float
    voltage: Optional[float] = None
    current: Optional[float] = None
    metadata: Dict[str, Any] = {}


class ReadingCreate(ReadingBase):
    timestamp: Optional[datetime] = None


class ReadingResponse(ReadingBase):
    id: int
    timestamp: datetime
    device_id: int

    class Config:
        from_attributes = True


class ReadingsQuery(BaseModel):
    device_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 1000
