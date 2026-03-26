from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


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
