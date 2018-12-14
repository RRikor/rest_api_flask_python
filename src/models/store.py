# https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/6020514?start=0
# Showing exensibility features of this setup, using ItemModel as an example
from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # This will create a SQL join between ItemModel and StoreModel
    # This is a many to one relationship. Many items for 1 store.

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, price):
        self.name = name 
 
    def json(self):
        return {'name': self.name, [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
