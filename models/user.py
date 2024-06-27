from models.base_model import BaseModel 

class User(BaseModel):

    email_list = set()

    def __init__(self, email='', password='', first_name='', last_name='', review_id=[], place_id=[]):
        super().__init__()
        self.email = email
        User.email_list.add(email)
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.review_id = review_id
        self.place_id = place_id
