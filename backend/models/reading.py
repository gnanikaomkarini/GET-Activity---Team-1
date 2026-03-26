from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    power_watts = Column(Float)
    energy_kwh = Column(Float)
    voltage = Column(Float)
    current = Column(Float)
    metadata = Column(JSON, default={})

    device = relationship("Device", back_populates="readings")
