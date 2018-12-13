import sqlite3
from db import db

# Extending db.Model to tell SQLAlchemy that this class
# will save things to a db..
class UserModel(db.Model):

    # SQLAlchemy definitions for the table 'users'
    # Properties not defined here will not be saved into the db
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        # id is a python keyword and we don't want to use that as a variable id. 
        # thus we use _id. But self.id works fine. 
        self.id = _id
        self.username = username
        self.password = password

    # Because of calling the class User, we can use the @classmethod tag. This is 
    # not necessary, but slightly nicer.
    @classmethod
    def find_by_username(cls, username):

        connection = sqlite3.connect("src/data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # The value to execute always has to be a tuple. The only way to make 
        # a tuple with a single element is with a comma, to tell python that this 
        # is not a useless pair of brackets.
        result = cursor.execute(query, (username,))
        # If there are no rows, result.fetchone() will return None
        row = result.fetchone()
        if row:
            # Create a user object with data from the row
            # method 1: use the location in row
            # user = cls(row[0], row[1], row[2])
            # method 2: pass it as a set of positional arguments
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    # Copy paste from find_by_username, adapted to kd
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("src/data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
