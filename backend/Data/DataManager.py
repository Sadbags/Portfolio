from Data.IPersistenceManager import IPersistenceManager
from database import db

class DataManager(IPersistenceManager):
    def save(self, entity):
        db.session.add(entity)
        db.session.commit()

    def get(self, entity_id, entity_type):
        return entity_type.query.get(entity_id)

    def update(self, entity):
        db.session.commit()

    def delete(self, entity_id, entity_type):
        entity = entity_type.query.get(entity_id)
        if entity:
            db.session.delete(entity)
            db.session.commit()
        else:
            raise ValueError(f"{entity_type.__name__} with ID {entity_id} not found")

        # aqui estoy tratando otras cosas volver a este punto IOE