from flask_restful import Resource, reqparse

from models.user import UserModel


class RegisterUser(Resource):

    # Initialize parser to parse the JSON data from request body
    parser = reqparse.RequestParser()

    # Acceptable arguments in the JSON payload of the request
    parser.add_argument('username', type=str, required=True, help='Username cannot be empty')
    parser.add_argument('password', type=str, required=True, help='Password cannot be empty')

    def post(self):

        # Parse the JSON payload from the request body
        data = RegisterUser.parser.parse_args()

        # Find the userdata mapped to the given username
        if UserModel.find_username(data['username']):
            return {"message": "user {} already exists".format(data['username'])}, 400

        # Create a new userdata object
        user = UserModel(data['username'], data['password'])

        # Save the userdata to the database
        user.save_to_db()

        return {"message": "User created successfully"}, 201
