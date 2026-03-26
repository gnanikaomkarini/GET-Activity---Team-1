from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    JSON,
    Boolean,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./energy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="My Home")
    size_sqft = Column(Integer, default=1500)
    occupants = Column(Integer, default=4)
    location = Column(String, default="Unknown")
    tariff_rate = Column(Float, default=0.12)  # $/kWh
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    devices = relationship("Device", back_populates="household")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"), default=1)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    location = Column(String, default="Home")
    params = Column(JSON, default={})
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    household = relationship("Household", back_populates="devices")
    readings = relationship("Reading", back_populates="device")
    analyses = relationship("Analysis", back_populates="device")
    simulation_runs = relationship("SimulationRun", back_populates="device")


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    power_watts = Column(Float)
    energy_kwh = Column(Float)
    voltage = Column(Float)
    current = Column(Float)
    meta = Column(JSON, default={})

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


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    scenario = Column(String, nullable=False)
    duration_hours = Column(Integer, default=24)
    readings_count = Column(Integer, default=0)
    avg_power = Column(Float, default=0)
    total_energy = Column(Float, default=0)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="simulation_runs")


Base.metadata.create_all(bind=engine)
