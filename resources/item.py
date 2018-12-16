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
    parser.add_argument('store_id',
        type=int,                             # the price has to be a float
        required=True,                          # price is a required attribute
        help="Every item needs a store_id."
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
        item = ItemModel(name, data['price'], data['store_id'])
        # or: item = ItemModel(name, **data) 

        # Insert item into DB
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500 
 
        # Return item
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "Item has been deleted"}

    def put(self, name):
        # Passes only the valid arguments into variable data
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name) 

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # Methode 1: for loop
        # for item in ItemModel.query.all():
        #     items = {
        #         'item': item.name,
        #         'price': item.price
        #     }
        # return {'items': items}, 200

        # Methode 2: list comprehension
        # return {'items': [item.json() for item in ItemModel.query.all()]}

        # Methode 3: lambda 
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}