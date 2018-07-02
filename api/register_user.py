from api.modals.user import User
from api.db import DataBaseConnection
from flask_restful import Resource, reqparse


class RegisterUser(Resource):
    """RegisterUser extends Resource class methods post for creating a new user"""
    def post(self):
        """RideResource2 extends Resource class methods post for creating a ride join request"""
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="name is required")
        parser.add_argument('email', type=str, required=True, help="email is required")
        parser.add_argument('password', type=str, required=True, help="password field is required")
        parser.add_argument('confirm', type=str, required=True, help="password confirmation is required")
        data = parser.parse_args()

        # create connection and set cursor
        connection = DataBaseConnection()
        cursor = connection.cursor
        dict_cursor = connection.dict_cursor

        if data["password"] != data["confirm"]:
            return {"status": "fail", "message": "Password mismatch"}, 400
        
        # check if user with this email exists
        user_data = User.get_user_by_email(dict_cursor, data["email"])
        
        if not user_data:
            User.create_user(cursor, data["name"], data["email"], data["password"])
            get_user = User.get_user_by_email(dict_cursor, data["email"])

            if get_user:
                # get auth token 
                auth_token = User.encode_authentication_token(get_user['user_id']) 
                return {"auth_token": auth_token.decode(), "status": "success",
                        "message": "account created"}, 201

        return {"status": "fail", "message": "email already taken"}, 400
