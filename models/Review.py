from models.base_model import BaseModel

class review(BaseModel):

    def __init__(self, obj_id=None, feedback="", rating="", comment="", place_id=None, user_id=None):
        super().__init__()
        if obj_id != None:
            self.id = obj_id
        self.feedback = feedback
        self.rating = rating
        self.comment = comment
        self.place_id = place_id
        self.user_id = user_id
