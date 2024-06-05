from PersistenceManager import IPersistenceManager

class DataManager(IPersistenceManager):

    storage = {}

    def save(self, entity):
        DataManager.storage.update(entity)

    def get(self, entity_id, entity_type):
        # Logic to retrieve an entity based on ID and type
        pass

    def update(self, entity):
        # Logic to update an entity in storage
        pass

    def delete(self, entity_id, entity_type):
        # Logic to delete an entity from storage
        pass