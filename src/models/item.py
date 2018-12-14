from db import db

# Extending db.Model to tell SQLAlchemy that this class
# will save things to a db..
class ItemModel(db.Model):

    # SQLAlchemy definitions for the table 'items'
    # Properties not defined here will not be saved into the db
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))    # Floating point number with 2 decimals

    # Added for store.py
    # Creating a foreign key inside table items that matches the id 
    # inside table stores, for easy finding matching items-store combinations
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # This will create a SQL join between ItemModel and StoreModel
    store = db.relationship('StoreModel')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    # This should still be a classmethod because it returns 
    # an object of type ItemModel
    @classmethod
    def find_by_name(cls, name):
        # works like: "SELECT * FROM items where name = ? LIMIT 1"
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()