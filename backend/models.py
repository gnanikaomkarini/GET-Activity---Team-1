from .database import Base, engine, get_db
from .device import Device
from .reading import Reading

Base.metadata.create_all(bind=engine)
