from models.place import Place
from models.base_model import BaseModel 
from models.base_model import BaseModel
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.review import Review
from app import app

class User(BaseModel):

    if app.config['USE_DATABASE']:
        __tablename__ = 'users'

        id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
        email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
        password: Mapped[str] = mapped_column(String(255), nullable=False)
        first_name: Mapped[str | None] = mapped_column(String(128), nullable=False)
        last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
        review_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('reviews.id'), nullable=True)
        place_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('places.id'), nullable=True)

        reviews: Mapped[list[Review]] = relationship("Review", back_populates="user")
        places: Mapped[Place] = relationship("Place", back_populates="user")
    else:
        email_list = set()

        def __init__(self, email='', password='', first_name='', last_name='', review_id=[], place_id=[]):
            super().__init__()
            self.email = email
            User.email_list.add(email)
            self.password = password
            self.first_name = first_name
            self.last_name = last_name
            self.review_id = review_id
            self.place_id = place_id
