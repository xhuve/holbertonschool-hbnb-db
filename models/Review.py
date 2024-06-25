from models.base_model import BaseModel
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.user import User

class Review(BaseModel):
    __tablename__ = 'reviews'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feedback: Mapped[String] = mapped_column(String, nullable=False, default="")
    rating: Mapped[String] = mapped_column(String, nullable=False, default="")
    comment: Mapped[String] = mapped_column(String, nullable=True, default="")
    place_id: Mapped[Integer | None] = mapped_column(Integer, ForeignKey('places.id'), nullable=True)
    user_id: Mapped[Integer | None] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="reviews")

