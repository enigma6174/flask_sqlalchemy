from flask_restful import Resource
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):

    # Fetch store object from database identified by store name
    @jwt_required()
    def get(self, name):

        store = StoreModel.get_store(name)

        if store:
            return store.json()
        else:
            return {'message': 'Store {} not found'.format(name)}, 404

    # Create a new store in the database
    @jwt_required()
    def post(self, name):

        # Check if store with given name already exists in database
        if StoreModel.get_store(name):
            return {'message': 'Store {} already exists'.format(name)}, 400

        # Create a store object
        store = StoreModel(name)

        # Add new store object to database
        try:
            store.save_to_db()
        except Exception as e:
            return {'exception': e}, 500

        return store.json(), 201

    # Delete the store object identified by store name from the database
    @jwt_required()
    def delete(self, name):

        store = StoreModel.get_store(name)

        if store:
            store.delete_from_db()

        return {'message': 'store deleted'}


class StoreList(Resource):

    # Return a list of all available stores
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
