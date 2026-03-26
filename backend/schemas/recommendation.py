from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    description: Optional[str]
    estimated_savings_kwh: Optional[float]
    estimated_savings_currency: Optional[float]
    confidence_score: Optional[float]
    actions: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
