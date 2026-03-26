from .user import User
from .device import Device
from .reading import Reading
from .recommendation import Recommendation

from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)
