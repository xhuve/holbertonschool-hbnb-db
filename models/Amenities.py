from models.base_model import BaseModel 

class Amenities(BaseModel):

    def __init__(self, name="", description="", place_id=""):
        super().__init__()
        self.name = name
        self.description = description
        self.place_id = place_id

