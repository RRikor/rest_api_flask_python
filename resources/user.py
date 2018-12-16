# https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/5960168?start=30
# User object file

import sqlite3
from models.user import UserModel
from flask_restful import Resource, reqparse

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
        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400 
        else:
            # Method 1:
            user = UserModel(data['username'], data['password'])
            # Method 2: For each of the keys in data, pass all arguments. Possible
            # because of using the parser. So arguments will always be the same.
            user = UserModel(**data)


            user.save_to_db()

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

