from models.base_model import BaseModel 
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from flask_bcrypt import Bcrypt
from app import app

bcrypt = Bcrypt(app)
class User(BaseModel):

    if app.config['USE_DATABASE']:
        from models.place import Place
        from models.review import Review
        
        __tablename__ = 'users'

        id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
        email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
        password: Mapped[str] = mapped_column(String(255), nullable=False)
        first_name: Mapped[str | None] = mapped_column(String(128), nullable=False)
        last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
        review_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('reviews.id'), nullable=True)
        place_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('places.id'), nullable=True)
        password_hash: Mapped[String] = mapped_column(String(128))
        is_admin = mapped_column(Boolean, default=False)


        reviews: Mapped[list[Review]] = relationship("Review", back_populates="user")
        places: Mapped[Place] = relationship("Place", back_populates="user")

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


    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
