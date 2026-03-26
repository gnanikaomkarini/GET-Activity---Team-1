from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(
        String, nullable=False
    )  # smart_meter, thermostat, plug, energy_monitor
    name = Column(String, nullable=False)
    location = Column(String)
    params = Column(JSON, default={})  # device-specific parameters
    status = Column(String, default="active")  # active, paused
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="devices")
    readings = relationship("Reading", back_populates="device")
