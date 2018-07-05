from api.modals.user import User
from flask_restful import Resource, reqparse
import datetime
from flask_jwt_extended import create_access_token
from api.tests import helpers


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

        missing_fields = helpers.check_missing_field(
            ["name", "email", "password", "confirm password"],
            [data["name"], data["email"], data["password"], data["confirm"]]
        )

        if missing_fields:
            return {"message:": missing_fields}, 400

        if not data["name"].isalnum():
            return {"message:": "Invalid name"}, 400

        if not helpers.validate_email(data["email"]):
            return {"message:": "Invalid email"}, 400

        if data["password"] != data["confirm"]:
            return {"status": "fail", "message": "Password mismatch"}, 400

        user_data = User.get_user_by_email(data["email"])
        
        if not user_data:
            user = User(None, data["name"], data["email"], data["password"], data["confirm"])
            user.create_user()

            get_user = User.get_user_by_email(data["email"])

            if get_user:
                expires = datetime.timedelta(days=1)

                auth_token = create_access_token(identity=get_user['user_id'], expires_delta=expires)
                return {"auth_token": auth_token, "status": "success",
                        "message": "account created"}, 201

        return {"status": "fail", "message": "email already taken"}, 409

