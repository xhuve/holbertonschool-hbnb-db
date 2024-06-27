from persistence.IPersistenceManager import IPersistenceManager
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.country import Country
from models.amenity import Amenity
from models.place import Place
from models.review import Review
class DataManager(IPersistenceManager):

    storage = {}

    def save(self, entity):
        try:
            if isinstance(entity, BaseModel):
                user = entity.__dict__
                class_type = entity.__class__.__name__

                if class_type in DataManager.storage.keys():
                    DataManager.storage[class_type].append(user)
                else:
                    DataManager.storage[class_type] = [user]
                return user
            else:
                raise TypeError()
        except TypeError:
            print("The argument should be an object")

    def get(self, entity_id, entity_type):
        try:
            for user in DataManager.storage[f"{entity_type}"]:
                if user["id"] == entity_id:
                    return user
        except Exception as e:
            print(e)

    def update(self, entity):
        class EntityNotFoundError(Exception):
            pass

        try:
            class_type = f"{entity.__class__.__name__}"
            print(entity.id)
            for idx, user in enumerate(DataManager.storage[class_type]):
                if user["id"] == entity.id:
                    DataManager.storage[class_type][idx] = entity.__dict__
                    return entity.__dict__
            raise EntityNotFoundError("Bad Request")
        except EntityNotFoundError as e:
            raise e
        except Exception as e:
            print(e)

    def delete(self, entity_id, entity_type):
        try:
            DataManager.storage[f"{entity_type}"] = [user for user in DataManager.storage[f"{entity_type}"] if user["id"] != entity_id]
        except Exception as e:
            print(e)

user1 = User(
    email="john.doe@example.com",
    password="password123",
    first_name="John",
    last_name="Doe",
    review_id=["review1", "review2"],
    place_id=["place1"]
)
user1.id = 1

# User 2
user2 = User(
    email="jane.smith@example.com",
    password="password456",
    first_name="Jane",
    last_name="Smith",
    review_id=["review3"],
    place_id=["place2", "place3"]
)
user2.id = 2

DataManager.save(DataManager, user1)
DataManager.save(DataManager, user2)

seeder = [
    City(name="New York", population=8419000, country_code="USA"),
    City(name="Los Angeles", population=3980000, country_code="USA"),
    City(name="Chicago", population=2716000, country_code="USA"),
    City(name="Tokyo", population=13929286, country_code="JPN"),
    City(name="Paris", population=2141000, country_code="FRA"),
    City(name="London", population=8982000, country_code="GBR"),
    City(name="Berlin", population=3748000, country_code="DEU"),
    City(name="Sydney", population=5312000, country_code="AUS"),
    City(name="Toronto", population=2731000, country_code="CAN"),
    City(name="São Paulo", population=12300000, country_code="BRA"),
    Country(name="United States", population=331002651, code="USA"),
    Country(name="Canada", population=37742154, code="CAN"),
    Country(name="United Kingdom", population=67886011, code="GBR"),
    Country(name="Germany", population=83783942, code="DEU"),
    Country(name="France", population=65273511, code="FRA"),
    Country(name="Japan", population=126476461, code="JPN"),
    Country(name="Australia", population=25499884, code="AUS"),
    Country(name="Brazil", population=212559417, code="BRA"),
    Country(name="China", population=1439323776, code="CHN"),
    Country(name="India", population=1380004385, code="IND"),
    Amenity(name="Free Wi-Fi", description="High-speed wireless internet access available throughout the premises.", place_id="123"),
    Amenity(name="Swimming Pool", description="Outdoor pool open from 8 AM to 8 PM.", place_id="123"),
    Amenity(name="Gym", description="24-hour access to a well-equipped fitness center.", place_id="124"),
    Amenity(name="Parking", description="Complimentary on-site parking available.", place_id="125"),
    Amenity(name="Air Conditioning", description="In-room air conditioning system.", place_id="126"),
    Amenity(name="Breakfast Included", description="Complimentary breakfast served daily from 6 AM to 10 AM.", place_id="127"),
    Amenity(name="Pet-Friendly", description="Pets are allowed with prior arrangement.", place_id="128"),
    Amenity(name="Spa", description="Full-service spa offering various treatments and massages.", place_id="129"),
    Amenity(name="Room Service", description="24-hour room service available.", place_id="130"),
    Amenity(name="Laundry Service", description="On-site laundry and dry cleaning services.", place_id="123"),
    Place(
        obj_id=0,
        name="Luxury Penthouse in New York",
        description="A breathtaking penthouse with panoramic views of Manhattan. Featuring modern amenities and luxurious decor.",
        address="456 Park Ave, New York, NY 10022",
        longitude=-73.9725,
        latitude=40.7648,
        price_per_night=1500.00,
        number_of_rooms=4,
        bathrooms=3,
        max_guests=8,
        amenity_id=(1, 2, 5, 6, 9),
        city_id=1,
        host_id=1
    ),
    Place(
        obj_id=1,
        name="Beachfront Villa in Los Angeles",
        description="A stunning villa located right on the Malibu beachfront. Perfect for a family retreat or a romantic getaway.",
        address="789 Ocean Ave, Malibu, CA 90265",
        longitude=-118.8100,
        latitude=34.0256,
        price_per_night=1200.00,
        number_of_rooms=5,
        bathrooms=4,
        max_guests=10,
        amenity_id=(1, 2, 4, 5, 7),
        city_id=2,
        host_id=2
    ),
    Place(
        obj_id=2,
        name="Chic Apartment in Tokyo",
        description="A modern apartment in the heart of Tokyo. Ideal for business travelers and tourists.",
        address="123 Shibuya Crossing, Tokyo, Japan",
        longitude=139.7006,
        latitude=35.6895,
        price_per_night=300.00,
        number_of_rooms=2,
        bathrooms=1,
        max_guests=4,
        amenity_id=(1, 5, 8, 10),
        city_id=4,
        host_id=1
    ),
    Place(
        obj_id=3,
        name="Historic Home in Paris",
        description="A charming historic home in the heart of Paris. Experience the elegance of French architecture with modern comforts.",
        address="12 Rue de Rivoli, Paris, France",
        longitude=2.3500,
        latitude=48.8566,
        price_per_night=700.00,
        number_of_rooms=3,
        bathrooms=2,
        max_guests=6,
        amenity_id=(1, 4, 5, 6, 8),  
        city_id=5,
        host_id=2
    ),
    Review(
        obj_id=1,
        feedback="Excellent stay!",
        rating="5",
        comment="The host was very accommodating, and the property was spotless. Highly recommend!",
        place_id=2,
        user_id=2
    ),
    Review(
        obj_id=2,
        feedback="Good experience",
        rating="4",
        comment="Great location and amenities, but a bit noisy during the night.",
        place_id=3,
        user_id=1
    ),
    Review(
        obj_id=3,
        feedback="Could be better",
        rating="3",
        comment="The place was okay, but it didn't meet my expectations in terms of cleanliness.",
        place_id=3,
        user_id=1
    )
]

for idx, value in enumerate(seeder):
    if isinstance(value.id, str):
        value.id = idx
    DataManager.save(DataManager, value)

