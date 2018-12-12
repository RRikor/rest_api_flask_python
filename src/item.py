import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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
        # Filter function returns a filter object
        # All items are unique so this filter will only return 1 item 
        # Next returns the first item found by the filter function (when
        # calling next again it gives the 2nd item, 3rd and so on)
        # 
        # next can cause an error and break the program if there are no more items left
        # None parameter prevents this. When nothing found it will return None
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # Return value if item not found will be 404 (not found)
        # Return code is a ternary if statement
        # return {'item': item}, 200 if item else 404

        item = self.find_by_name(name)
        if item:
            return item
        else:
            return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {
                'item': {
                    'name': row[0],
                    'price': row[1]
                }
            }

    def post(self, name):
        # Check if item already exists
        if self.find_by_name(name):
            return {'message': "Item '{}' already exists".format(name)}, 400

        # Parse the incoming request
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }

        # Connect to the database to insert the item
        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

        # Return item
        return item, 201

    @classmethod
    def insert(cls, item):
        # Connect to the database to insert the item
        connection = sqlite3.connect('src/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()


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
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}