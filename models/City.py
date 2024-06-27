from models.base_model import BaseModel
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.country import Country
from models.user import User
from app import app

class City(BaseModel):

    if app.config['USE_DATABASE']:
        __tablename__ = 'cities'

        name: Mapped[String] = mapped_column(String)
        population: Mapped[Integer] = mapped_column(Integer)
        country_code: Mapped[String] = mapped_column(String, ForeignKey("country.code"))

        country: Mapped[Country] = relationship("Country", back_populates="cities")
        user: Mapped[User] = relationship("Place", back_populates="city")

    else:
        def __init__(self, name="", population=0, country_code=None):
            super().__init__()
            self.name = name
            self.population = population
            self.country_code = country_code
