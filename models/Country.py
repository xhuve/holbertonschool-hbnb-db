from models.base_model import BaseModel

class Country(BaseModel):

    all_country_codes = set()

    def __init__(self, name="", population=0, code=None):
        super().__init__()
        self.name = name
        self.population = population
        self.code = code
        self.all_country_codes.add(code)