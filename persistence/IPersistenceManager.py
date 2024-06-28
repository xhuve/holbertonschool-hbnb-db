from abc import ABC, abstractmethod

class IPersistenceManager(ABC):

    @abstractmethod
    @staticmethod
    def all(entity):
        pass

    @abstractmethod
    @staticmethod
    def save(self, entity):
        pass

    @abstractmethod
    @staticmethod
    def get(self, entity_id, entity_type):
        pass

    @abstractmethod
    @staticmethod
    def update(self, entity):
        pass

    @abstractmethod
    @staticmethod
    def delete(self, entity_id, entity_type):
        pass