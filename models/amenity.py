import os
from .base_model import BaseModel 
from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from dotenv import load_dotenv

load_dotenv()

class Amenity(BaseModel):
    if os.getenv('USE_DATABASE'):
        __tablename__ = 'amenities'
        name: Mapped[String] = mapped_column(String(128), nullable=False)
        description: Mapped[String] = mapped_column(String(1024), nullable=True)
        place_id = mapped_column(String(60), nullable=False)

        place_amenities = relationship("Place", back_populates='amenities')
    else:
        amenity_list = set()

        def __init__(self, name="", description="", place_id=""):
            super().__init__()
            self.name = name
            self.description = description
            self.place_id = place_id
            self.amenity_list.add(name)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'description': self.description,
            'place_id': self.place_id
        }
