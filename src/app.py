from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Creates an instance of Flask called app. And telling it where it is
# located with __name__.
app = Flask(__name__)

# Secret key to understand what was encrypted with JWT
# The secret key should not be visible if you publish this code
# In a production environment this should be something complicated
app.secret_key = "RRikor"

# The API allows to very easily add resources to it. And say things like:
# for this resource you can GET and POST, for this other resource you can 
# GET and DELETE and so on. 
api = Api(app)

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
items = []

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
        item = next(filter(lambda x: x['name'] == name, items), None)
        # Return value if item not found will be 404 (not found)
        # Return code is a ternary if statement
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # If we found an item, and that item is not None: return message
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "Item '{}' already exists".format(name)}, 400

        # If the request does not have the proper JSON payload or does
        # not have an error. The request.get_json() will give an error.
        # get_json(force=True): Will ignore the header and scan the body for JSON
        # get_json(silent=True):
        # data = request.get_json(force=True)
        # replaced the request.get_json() with the RequestParser()
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return items[-1], 201

    def delete(self, name):
        # Overwrite items list with all elements except the one to be deleted
        # global items means python will use the global items variable 
        # for these instructions
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": "'{}' deleted".format(name)}

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

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# debug=True will turn Flask error messaging on
app.run(port=5000, debug=True)

