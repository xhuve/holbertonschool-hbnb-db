from persistence.IPersistenceManager import IPersistenceManager
from models.base_model import BaseModel
from models.users import Users
from models.city import City
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
    City(name="Chicago", population=2716000, country_code="USA"),
    City(name="Tokyo", population=13929286, country_code="JPN"),
    City(name="Paris", population=2141000, country_code="FRA")
]

for idx, value in enumerate(seeder):
    value.id = idx
    DataManager.save(DataManager, value)
