from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        # Check if store is in the database. If so,
        # return the store.
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store does not exist.'}, 404

    def post(self, name):
        # Check if the name of the store is already taken
        if StoreModel.find_by_name(name):
            return {'message:' "Store name '{}' is already taken".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
            return store.json()
        except:
            return {'message': 'An error occured while creating the store'}, 500
        

    def delete(self, name):
        # Check if the store exists in the DB
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'The store has been deleted.'}
        else:
            return {'message': 'The store does not exist.'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

    