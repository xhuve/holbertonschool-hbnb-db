from models.amenity import Amenity
from models.base_model import BaseModel
from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dotenv import load_dotenv
import os

load_dotenv()

class Place(BaseModel):    
    if os.getenv('USE_DATABASE'):
    
        __tablename__ = 'places'

        name: Mapped[String] = mapped_column(String(128), nullable=False)
        description: Mapped[String | None] = mapped_column(String(1024), nullable=True)
        address: Mapped[String] = mapped_column(String(256), nullable=False)
        longitude: Mapped[Float] = mapped_column(Float, nullable=False)
        latitude: Mapped[Float] = mapped_column(Float, nullable=False)
        price_per_night: Mapped[Float] = mapped_column(Float, nullable=False)
        number_of_rooms: Mapped[Integer] = mapped_column(Integer, nullable=False)
        bathrooms: Mapped[Integer] = mapped_column(Integer, nullable=False)
        max_guests: Mapped[Integer] = mapped_column(Integer, nullable=False)
        amenity_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("amenities.id"), nullable=True, unique=True)
        city_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("cities.id"), nullable=True)
        host_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

        amenities = relationship("Amenity", back_populates="place_amenities", uselist=True, foreign_keys="[Place.amenity_id]")
        city = relationship("City", back_populates="places", foreign_keys="[Place.city_id]")
        user = relationship("User", back_populates="places", foreign_keys="[Place.host_id]")
    else: 
        def __init__(self, obj_id=None, name="", description="", address="", longitude=0.0, latitude=0.0, price_per_night=0.0, number_of_rooms=0, bathrooms=0, max_guests=0, amenity_id=(), city_id="", host_id=""):
            super().__init__()
            if obj_id != None:
                self.id = obj_id
            self.name = name
            self.description = description
            self.address = address
            self.longitude = longitude
            self.latitude = latitude
            self.price_per_night = price_per_night
            self.number_of_rooms = number_of_rooms
            self.bathrooms = bathrooms
            self.max_guests = max_guests
            self.amenity_id = amenity_id
            self.city_id = city_id
            self.host_id = host_id
