from models.base_model import BaseModel
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.city import City
from app import app


class Country(BaseModel):
    if app.config['USE_DATABASE']:
        __tablename__ = 'countries'

        name: Mapped[String] = mapped_column(String)
        population: Mapped[Integer] = mapped_column(Integer)
        code: Mapped[Integer] = mapped_column(String, unique=True)

        cities: Mapped[list[City]] = relationship('City', back_populates="country")
    else:
        all_country_codes = set()

        def __init__(self, name="", population=0, code=None):
            super().__init__()
            self.name = name
            self.population = population
            self.code = code
            self.all_country_codes.add(code)
