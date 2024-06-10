from models.base_model import BaseModel

class Country(BaseModel):

    def __init__(self, name="", population=0, code=None):
        super().__init__()
        self.name = name
        self.population = population
        self.code = code