from models.base_model import BaseModel
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.city import City


class Country(BaseModel):
    __tablename__ = 'countries'

    name: Mapped[String] = mapped_column(String)
    population: Mapped[Integer] = mapped_column(Integer)
    code: Mapped[Integer] = mapped_column(String)

    cities: Mapped[list[City]] = relationship('City', back_populates="country")