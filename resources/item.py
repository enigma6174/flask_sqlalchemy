from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    # Initialize parser to parse the contents of the JSON body
    parser = reqparse.RequestParser()

    # Acceptable arguments in the JSON payload of the request
    parser.add_argument('price', type=float, required=True, help='Price cannot be empty')
    parser.add_argument('store_id', type=int, required=True, help='store_id cannot be empty')

    # Method to fetch the item record from the table
    # Returns a JSON representation of the item record object
    @jwt_required()
    def get(self, name):

        try:
            item = ItemModel.get_item(name)
        except Exception as e:
            return {'exception': e}, 500

        if item:
            return item.json(), 200

        return {'message': 'item {} not in database'.format(name)}, 404

    # POST call for the resource - add new item to database
    # Authentication required to modify database
    @jwt_required()
    def post(self, name):

        # Fetch the item for the given name from the database
        if ItemModel.get_item(name):
            return {'message': 'item {} already exists in database'.format(name)}, 400

        # Parse the JSON payload from the request body
        data = Item.parser.parse_args()

        # Create a new Item object from the request data
        item = ItemModel(name, data['price'], data['store_id'])

        # Add new item to database
        try:
            item.save_to_db()
        except Exception as e:
            return {'exception': e}, 500

        return item.json(), 201

    # DELETE call for the resource - delete existing item from database
    # Authentication required to modify database
    @jwt_required()
    def delete(self, name):

        # Fetch the item for the given name from the database
        item = ItemModel.get_item(name)

        if item is None:
            return {'message': '{} does not exist in the database'.format(name)}

        # Delete the item from the database if it exists
        item.delete_from_db()

        return {'message': '{} deleted'.format(name)}

    # PUT call for the resource - update existing item in the database or create new item if not exist
    # Authentication required to modify database
    @jwt_required()
    def put(self, name):

        # Parse the JSON payload from the request body
        data = Item.parser.parse_args()

        # Fetch the item for the specified name from the database
        item = ItemModel.get_item(name)

        # If the item with given name does not exist, create a new item from request body
        # If the item already exists in the database, update the price of the item
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        # Save the item to the database
        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):

    # Returns a list of all the items present in the database
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
