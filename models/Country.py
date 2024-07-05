import os
from models.base_model import BaseModel
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from dotenv import load_dotenv

load_dotenv()

class Country(BaseModel):
    if os.getenv('USE_DATABASE'):
        __tablename__ = 'countries'

        name: Mapped[String] = mapped_column(String)
        population: Mapped[Integer] = mapped_column(Integer)
        code: Mapped[Integer] = mapped_column(String, unique=True)

        cities = relationship('City', back_populates="country", uselist=True)
    else:
        all_country_codes = set()

        def __init__(self, name="", population=0, code=None):
            super().__init__()
            self.name = name
            self.population = population
            self.code = code
            self.all_country_codes.add(code)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'population': self.population,
            'code': self.code
        }