from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

# Creates an instance of Flask called app. And telling it where it is
# located with __name__.
app = Flask(__name__)

# Tell SQLAlchemy where the database is located: At the root folder of
# the project.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Turning off the Flask SQLAlchemy Modification Tracker. It uses too
# much resources to track changes to the database. SQLAlchemy itself has 
# a better tracker.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize SQLAlchemy
db.init_app(app)

# Secret key to understand what was encrypted with JWT
# The secret key should not be visible if you publish this code
# In a production environment this should be something complicated
app.secret_key = "RRikor"

# The API allows to very easily add resources to it. And say things like:
# for this resource you can GET and POST, for this other resource you can 
# GET and DELETE and so on. 
api = Api(app)

# Like it says, run this before the first request
# Create the database and create the tables unless they exist already
@app.before_first_request
def create_tables():
    db.create_all()

# The JWT object uses app, authenticate and identity functions together to 
# allow for authentication. JWT creates a new endpoint: '/auth'
# When we call /auth we send a username+ password. Jwt receives this and 
# sends this to the authenticate function.
# When we send a token, JWT sends it to the identy function. It uses the token
# to get the user ID. If it can do that, that means that the user is 
# authenticated and all is good. 
# To make JWT work you need: @jwt_required
jwt = JWT(app, authenticate, identity)

# In memory database for examplary purposes
# items = []

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# When running a file it receives the name "__main__". Only 
# the file you run receives this name. 
#if __name__ == "__main__":

# https://stackoverflow.com/questions/30764073/sqlalchemy-extension-isnt-registered-when-running-app-with-gunicorn
# Not working to initialze with __name__ == "__main__"
# db import and db.init_app(app) moved to the top of the file.

# debug=True will turn Flask error messaging on
app.run(port=5000, debug=True)

