from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


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


class AnalysisRequest(BaseModel):
    device_id: int
    readings_hash: str
    analysis_data: Dict[str, Any]
    readings_count: int


class AnalysisResponse(BaseModel):
    id: int
    device_id: int
    readings_hash: str
    readings_count: int
    created_at: datetime
    cached: bool

    class Config:
        from_attributes = True


class GetAnalysisRequest(BaseModel):
    device_id: int
    readings_data: List[Dict[str, Any]]
