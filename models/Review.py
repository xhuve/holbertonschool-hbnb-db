from BaseModel import BaseModel

class Review(BaseModel):

    def __init__(self, feedback="", rating="", comment=""):
        super().__init__()
        self.feedback = feedback
        self.rating = rating
        self.comment = comment
