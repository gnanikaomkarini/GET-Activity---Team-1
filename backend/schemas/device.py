from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class DeviceCreate(BaseModel):
    type: str
    name: str
    location: Optional[str] = "Home"
    params: Dict[str, Any] = {}


class DeviceResponse(BaseModel):
    id: int
    name: str
    type: str
    location: str
    params: Dict[str, Any]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
