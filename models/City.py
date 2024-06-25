from models.base_model import BaseModel
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.country import Country
from models.user import User


class City(BaseModel):
    __tablename__ = 'cities'

    name: Mapped[String] = mapped_column(String)
    population: Mapped[Integer] = mapped_column(Integer)
    country_code: Mapped[String] = mapped_column(String, ForeignKey("country.code"))

    country: Mapped[Country] = relationship("Country", back_populates="cities")
    user: Mapped[User] = relationship("Place", back_populates="city")
