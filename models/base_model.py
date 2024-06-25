import datetime
import uuid
from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from app import db

class BaseModel(db.Models):

    __abstract__ = True

    id: Mapped[String] = mapped_column(default=str(uuid.uuid4()), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(default=datetime.datetime.now())
    updated_at: Mapped[DateTime] = mapped_column(default=datetime.datetime.now())
    