import datetime
import uuid

class BaseModel():

    def __init__(self):
        self.id = uuid.uuid4()
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    