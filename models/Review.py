from models.base_model import BaseModel

class Review(BaseModel):

    def __init__(self, feedback="", rating="", comment="", place_id=None, user_id=None):
        super().__init__()
        self.feedback = feedback
        self.rating = rating
        self.comment = comment
        self.place_id = place_id
        self.user_id = user_id
