from api.modals.user import User
from api.db import DataBaseConnection
from flask_restful import Resource, reqparse


class LoginUser(Resource):
    """LoginUses extends Resource methods post which logins i given user"""
    def post(self):
        """logins in a given user"""
        # parse arguments to ensure that required fields are sent
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email field is required")
        parser.add_argument('password', type=str, required=True, help="Password field is required")

        data = parser.parse_args()
        
        # create connection and set cursor
        connection = DataBaseConnection()
        dict_cursor = connection.dict_cursor

        user_data = User.get_user_by_email(dict_cursor, data["email"])

        if user_data:
            # find if the user passwords match
            if user_data["password"] == data["password"]:
                # generate token
                auth_token = User.encode_authentication_token(user_data['user_id'])
                return {"status": "success", "message": "successful login",
                        "auth_token": auth_token.decode()}, 200
                        
        # If no return till this point then the user was not found
        return {"status": "fail", "message": "Invalid user name or password"}, 401
