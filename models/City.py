from models.base_model import BaseModel
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

class City(BaseModel, Base):
    if os.getenv('USE_DATABASE'):
        __tablename__ = 'cities'

        name: Mapped[String] = mapped_column(String)
        population: Mapped[Integer] = mapped_column(Integer)
        country_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("countries.id"))

        country = relationship("Country", back_populates="cities")
        user = relationship("User", back_populates="city")
        places = relationship("Place", back_populates="city")

    else:
        def __init__(self, name="", population=0, country_code=None):
            super().__init__()
            self.name = name
            self.population = population
            self.country_code = country_code
