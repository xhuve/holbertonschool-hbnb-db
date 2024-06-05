from BaseModel import BaseModel

class City(BaseModel):
        
    def __init__(self, name="", population=0, user_id=""):
        super().__init__()
        self.name = name
        self.population = population
        self.user_id = user_id

