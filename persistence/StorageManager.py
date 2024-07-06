

from models.base_model import BaseModel


class LocalStorage:
    
    storage = {}

    @staticmethod
    def create(entity):
        if isinstance(entity, BaseModel):
            user = entity.__dict__
            class_type = entity.__class__.__name__

            if class_type in LocalStorage.storage.keys():
                LocalStorage.storage[class_type].append(user)
            else:
                LocalStorage.storage[class_type] = [user]
            return user
        else:
            raise TypeError()
        
    @staticmethod
    def all(entity):
        return LocalStorage.storage[f"{entity.__class__.__name__}"]

    @staticmethod
    def get(entity_type, entity_id):
        for user in LocalStorage.storage[f"{entity_type.__class__.__name__}"]:
            if user["id"] == entity_id:
                return user

    @staticmethod
    def update(entity):
        class EntityNotFoundError(Exception):
            pass

        class_type = f"{entity.__class__.__name__}"
        for idx, user in enumerate(LocalStorage.storage[class_type]):
            if user["id"] == entity.id:
                LocalStorage.storage[class_type][idx] = entity.__dict__
                return entity.__dict__
        raise EntityNotFoundError("Bad Request")
    
    @staticmethod
    def delete(entity_type, entity_id):
        LocalStorage.storage[f"{entity_type.__class__.__name__}"] = [user for user in LocalStorage.storage[f"{entity_type.__class__.__name__}"] if user["id"] != entity_id] 
