import datetime
import uuid

class BaseModel():

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = str(datetime.datetime.now())
        self.updated_at = str(datetime.datetime.now())
