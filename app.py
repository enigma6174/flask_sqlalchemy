from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import RegisterUser
from resources.item import Item, ItemList
from resources.store import Store, StoreList


# Flask object
app = Flask(__name__)

# Configurations for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT secret key
app.secret_key = 'secret2021'

# Api object
api = Api(app)


# Instruction to SQLAlchemy to create tables and database before any queries are executed
@app.before_first_request
def create_tables():
    db.create_all()


# JWT object for authentication
# Creates a new endpoint /auth where we make a request with username and password in JSON body
# The JSON body is verified with authenticate(username, password) and a JWT token is generated
# JWT calls identity(payload) with the token and from it extracts the userid to get the correct username
# Correct username from the extracted userid of the JWT token means the token was valid and authentication success
jwt = JWT(app, authenticate, identity)


api.add_resource(RegisterUser, '/register')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
