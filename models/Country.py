from BaseModel import BaseModel

class Country(BaseModel):

    def __init__(self, name="", population=0, city_id=[]):
        super().__init__()
        self.name = name
        self.population = population
        self.city_id = city_id