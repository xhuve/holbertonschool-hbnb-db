import datetime
import uuid
import os
from sqlalchemy import String, DateTime, Column
from . import db
from dotenv import load_dotenv

load_dotenv()

if os.getenv('USE_DATABASE'):
    class BaseModel(db.Model):
        __abstract__ = True
        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        created_at = Column(DateTime, default=datetime.datetime.now())
        updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
else:
    class BaseModel:
        def __init__(self):
            self.id = str(uuid.uuid4())
            self.created_at = str(datetime.datetime.now())
            self.updated_at = str(datetime.datetime.now())