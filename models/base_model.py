import datetime
import uuid
from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from app import app, db

class BaseModel(db.Models):

    if app.config['USE_DATABASE']:
        __abstract__ = True

        id: Mapped[String] = mapped_column(default=str(uuid.uuid4()), primary_key=True)
        created_at: Mapped[DateTime] = mapped_column(default=datetime.datetime.now())
        updated_at: Mapped[DateTime] = mapped_column(default=datetime.datetime.now())
    else:
        id = str(uuid.uuid4())
        created_at = str(datetime.datetime.now())

        updated_at = str(datetime.datetime.now())