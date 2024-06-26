from app import db

class SqlAlchemyManager:
    
    @staticmethod
    def create(obj):
        db.session.add(obj)
        db.session.commit()
    
    @staticmethod
    def read(model, id):
        query = model.query.filter_by(model.id == id)
        result = query.all()
        return result
    
    @staticmethod
    def update(obj):
        db.session.merge(obj)
        db.session.commit()
    
    @staticmethod
    def delete(model, id):
        obj = model.query.filter_by(id == id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
