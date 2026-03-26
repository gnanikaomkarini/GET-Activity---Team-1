from .database import Base, engine, get_db
from .device import Device, Reading, Analysis

Base.metadata.create_all(bind=engine)
