from models.base_model import BaseModel
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

class Review(BaseModel):
    if os.getenv('USE_DATABASE'):

        __tablename__ = 'reviews'

        id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
        feedback: Mapped[String] = mapped_column(String, nullable=False, default="")
        rating: Mapped[String] = mapped_column(String, nullable=False, default="")
        comment: Mapped[String] = mapped_column(String, nullable=True, default="")
        place_id: Mapped[Integer | None] = mapped_column(Integer, ForeignKey('places.id'), nullable=True)
        user_id: Mapped[Integer | None] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)

        user = relationship("User", back_populates="reviews", foreign_keys="[Review.user_id]")
    
    else:
        def __init__(self, obj_id=None, feedback="", rating="", comment="", place_id=None, user_id=None):
            super().__init__()
            if obj_id != None:
                self.id = obj_id
            self.feedback = feedback
            self.rating = rating
            self.comment = comment
            self.place_id = place_id
            self.user_id = user_id