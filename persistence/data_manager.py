from persistence.IPersistenceManager import IPersistenceManager
from models.base_model import BaseModel
from models.users import Users
from models.city import City
from models.country import Country
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

user1 = Users(
    email="john.doe@example.com",
    password="password123",
    first_name="John",
    last_name="Doe",
    review_id=["review1", "review2"],
    place_id=["place1"]
)
user1.id = 1

# User 2
user2 = Users(
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
    Country(name="India", population=1380004385, code="IND")
]

for idx, value in enumerate(seeder):
    value.id = idx
    DataManager.save(DataManager, value)

