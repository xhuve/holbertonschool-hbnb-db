from persistence.IPersistenceManager import IPersistenceManager
from models.base_model import BaseModel
from models.users import Users


class DataManager(IPersistenceManager):

    storage = {}

    def save(self, entity):
        try:
            if isinstance(entity, BaseModel):
                user = entity.__dict__
                if entity.__class__.__name__ in DataManager.storage.keys():
                    DataManager.storage[entity.__class__.__name__].append(user)
                else:
                    DataManager.storage[entity.__class__.__name__] = [user]
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
        try:
            curr_entity = f"{entity.__class__.__name__}.{entity.id}"
            if curr_entity in DataManager.storage:
                DataManager.storage.curr_entity = entity
        except Exception as e:
            print(e)


    def delete(self, entity_id, entity_type):
        try:
            DataManager.storage[f"{entity_type}"] = [user for user in DataManager.storage[f"{entity_type}"] if user["id"] != entity_id]
        except Exception as e:
            print(e)

