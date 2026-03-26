from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(
        String, nullable=False
    )  # smart_meter, thermostat, plug, energy_monitor
    location = Column(String, default="Home")
    params = Column(JSON, default={})
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    readings = relationship("Reading", back_populates="device")
