from abc import	ABC, abstractmethod


class IPersistenceManager(ABC):
    @abstractmethod
    def save(self, entity):
        pass


    @abstractmethod
    def get(self, entity_id, entity_type):
        pass


    @abstractmethod
    def update(self, entity):
        pass


    @abstractmethod
    def delete(self, entity_id, entity_type):
        pass
