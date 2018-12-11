# https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960168?start=30
# User object file

import sqlite3
from flask_restful import Resource, reqparse

class User:
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

class UserRegister(Resource):

    # Using RequestParser() to parse the request
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str
        , required=True
        , help="This field cannot be blank"
        )
    parser.add_argument('password',
        type=str
        , required=True
        , help="This field cannot be blank"
        )

    def post(self):
        # Parsing the request into data
        data = UserRegister.parser.parse_args()

        # Check if user already exists
        if User.find_by_username(data['username']):
            return {"message": "User already exists"}, 400 
        else:
            # Connecting to the database
            connection = sqlite3.connect("src/data.db")
            cursor = connection.cursor()
            # Insert user into the database
            # ID will be auto incremented, so we have to insert NULL
            query = "INSERT INTO users VALUES (Null,?,?)"
            # Tuple with username and password into queyr execute
            cursor.execute(query, (data['username'], data['password']))
            connection.commit()
            connection.close()
            return {"message": "User created succesfully"}, 201

