import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# The API works with Resources and every Resource needs to be a class
# Every class also needs to inherit from Resouce
class Item(Resource):

    # Request Parsing: RequestParser filters the JSON payload. It can also filter
    # through HTML forms and do many more things. We only defined 
    # price so any other arguments in the JSON payload will be erased.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,                             # the price has to be a float
        required=True,                          # price is a required attribute
        help="This field cannot be left blank!"
    )

    #Authorization required
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        # Check if item already exists
        if ItemModel.find_by_name(name):
            return {'message': "Item '{}' already exists".format(name)}, 400

        # Parse the incoming request
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        # Insert item into DB
        try:
            item.insert()
        except:
            return {'message': 'An error occured inserting the item'}, 500

        # Return item
        return item.json(), 201

    def delete(self, name):

        # Connect to the database to delete the item 
        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {"message": "The item {} is deleted".format(name)}

    def put(self, name):
        # Passes only the valid arguments into variable data
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name) 
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occured inserting the item'}, 500
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occured updating the item'}, 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items" 
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({
                "name": row[0],
                "price": row[1]
            })
        connection.close()
        return {'items': items}
