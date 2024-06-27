from models.base_model import BaseModel

class Place(BaseModel):

    def __init__(self, obj_id=None, name="", description="", address="", longitude=0.0, latitude=0.0, price_per_night=0.0, number_of_rooms=0, bathrooms=0, max_guests=0, amenity_id=(), city_id="", host_id=""):
        super().__init__()
        if obj_id != None:
            self.id = obj_id
        self.name = name
        self.description = description
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.price_per_night = price_per_night
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.max_guests = max_guests
        self.amenity_id = amenity_id
        self.city_id = city_id
        self.host_id = host_id
