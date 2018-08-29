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

        length_violations = helpers.check_length_restrictions(["name", "email"], [data["name"], data["email"]])

        error_found = False

        if missing_fields:
            error_found = True
            message = missing_fields

        if length_violations:
            error_found = True
            message = length_violations

        if data["name"]:
            if not data["name"].isalpha():
                error_found = True
                message = "Invalid name"

        if not helpers.validate_email(data["email"]):
            error_found = True
            message = "Invalid email"

        if data["password"] != data["confirm"]:
            error_found = True
            message = "Password mismatch"

        if error_found:
            return {"status": "fail", "message": message}, 400

        user_data = User.get_user_by_email(data["email"])

        if not user_data:
            user = User(name=data["name"], email=data["email"], password=data["password"], confirm=data["confirm"])
            user.create_user()

            get_user = User.get_user_by_email(data["email"])

            if get_user:
                expires = datetime.timedelta(days=1)
                
                auth_token = create_access_token(identity=get_user['user_id'], expires_delta=expires)
                return {"auth_token": auth_token, "status": "success",
                        "message": "account created", "users_name": data["name"]}, 201

        return {"status": "fail", "message": "email already taken"}, 409
