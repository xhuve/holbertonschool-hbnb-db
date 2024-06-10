from models.base_model import BaseModel

class City(BaseModel):
        
    def __init__(self, name="", population=0, country_code=None):
        super().__init__()
        self.name = name
        self.population = population
        self.country_code = country_code

