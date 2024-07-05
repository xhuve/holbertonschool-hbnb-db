import os
from models.base_model import BaseModel 
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from flask_bcrypt import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class User(BaseModel, Base):

    if os.getenv('USE_DATABASE'):
        
        __tablename__ = 'users'

        email: Mapped[String] = mapped_column(String(255), nullable=False, unique=True)
        password: Mapped[String] = mapped_column(String(255), nullable=False)
        first_name: Mapped[String | None] = mapped_column(String(128), nullable=False)
        last_name: Mapped[String | None] = mapped_column(String(128), nullable=True)
        city_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('cities.id'), nullable=True)
        is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False)  # Changed to Boolean

        city = relationship("City", back_populates="user", foreign_keys="[User.city_id]")
        reviews = relationship("Review", back_populates="user", uselist=True)
        places= relationship("Place", back_populates="user")

    else:

        email_list = set()

        def __init__(self, email='', password='', first_name='', last_name='', review_id=[], place_id=[], is_admin=False):
            super().__init__()
            self.email = email
            User.email_list.add(email)
            self.password = password
            self.first_name = first_name
            self.last_name = last_name
            self.review_id = review_id
            self.place_id = place_id
            self.is_admin= is_admin


    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
