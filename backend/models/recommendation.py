from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # behavioral, timing, settings
    title = Column(String, nullable=False)
    description = Column(String)
    estimated_savings_kwh = Column(Float)
    estimated_savings_currency = Column(Float)
    confidence_score = Column(Float)
    actions = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    user = relationship("User", back_populates="recommendations")
