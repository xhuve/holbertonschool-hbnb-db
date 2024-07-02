 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base_model import BaseModel
from .user import User
from .place import Place
from .amenity import Amenity
from .city import City
from .review import Review
from .country import Country
