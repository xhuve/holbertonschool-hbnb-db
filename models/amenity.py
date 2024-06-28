from models.base_model import BaseModel 
from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app import app, db

class Amenity(BaseModel):

    if app.config['USE_DATABASE']:
        __tablename__ = 'amenities'
        name: Mapped[String] = mapped_column(String(128), nullable=False)
        description: Mapped[String] = mapped_column(String(1024), nullable=True)
        place_id = mapped_column(String(60), nullable=False)

        place_amenities: Mapped[list[String]] = relationship("Place", back_populates='amenities')
    else:
        amenity_list = set()

        def __init__(self, name="", description="", place_id=""):
            super().__init__()
            self.name = name
            self.description = description
            self.place_id = place_id
            self.amenity_list.add(name)
