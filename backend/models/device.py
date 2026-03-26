from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    JSON,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    location = Column(String, default="Home")
    params = Column(JSON, default={})
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    readings = relationship("Reading", back_populates="device")
    analyses = relationship("Analysis", back_populates="device")


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


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    readings_hash = Column(String, nullable=False)
    analysis_data = Column(JSON, nullable=False)
    readings_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    cached = Column(Boolean, default=True)

    device = relationship("Device", back_populates="analyses")
