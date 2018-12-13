import sqlite3
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
        return ItemModel.query.filter_by(name=name).first()

        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            # method 1
            # return cls(row[0], row[1])
            # method 2: argument unpacking: passing all arguments
            return cls(*row)

    def insert(self):
        # Connect to the database to insert the item
        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self):
        
        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()
        query = "UPDATE items set price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
