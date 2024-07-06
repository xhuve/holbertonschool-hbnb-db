from models.base_model import BaseModel

class SqlAlchemyManager:
    def __init__(self, db_instance):
        self.db = db_instance

    def create(self, obj):
        if isinstance(obj, BaseModel):
            self.db.session.add(obj)
            self.db.session.commit()
        else:
            raise TypeError()
        
    def all(self, model):
        query = model.query.all()
        return query

    def read(self, model, id):
        query = model.query.filter_by(id=id).all()
        return query

    def update(self, obj):
        self.db.session.merge(obj)
        self.db.session.commit()

    def delete(self, model, id):
        obj = model.query.filter_by(id=id).first()
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()
