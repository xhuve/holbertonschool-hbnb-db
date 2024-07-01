from abc import ABC, abstractmethod

class IPersistenceManager(ABC):

    @abstractmethod
    def all(entity):
        pass

    @abstractmethod
    def save(entity):
        pass

    @abstractmethod
    def get(entity_id, entity_type):
        pass

    @abstractmethod
    def update(entity):
        pass

    @abstractmethod
    def delete(entity_id, entity_type):
        pass
