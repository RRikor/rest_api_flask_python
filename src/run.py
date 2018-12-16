# https://www.udemy.com/rest-api-flask-and-python/learn/v4/t/lecture/6038450?start=0
# File created to fix database importing issues in Heroku

from app import app
from db import db

# Initialize SQLAlchemy
db.init_app(app)

# Like it says, run this before the first request
# Create the database and create the tables unless they exist already
@app.before_first_request
def create_tables():
    db.create_all()