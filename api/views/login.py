from api.modals.user import User
from flask_restful import Resource, reqparse
import datetime
from flask_jwt_extended import create_access_token
from api.tests import helpers


class LoginUser(Resource):
    """LoginUses extends Resource methods post which logins i given user"""
    def post(self):
        """logins in a given user"""

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email field is required")
        parser.add_argument('password', type=str, required=True, help="Password field is required")
        data = parser.parse_args()

        missing_fields = helpers.check_missing_field(
            ["email", "password"],
            [data["email"], data["password"]]
        )

        if missing_fields:
            return {"message:": missing_fields}, 400

        if not helpers.validate_email(data["email"]):
            return {"message:": "Invalid email"}, 400

        user_data = User.get_user_by_email(data["email"])

        if user_data:
            if user_data["password"] == data["password"]:

                expires = datetime.timedelta(days=1)
                auth_token = create_access_token(identity=user_data['user_id'], expires_delta=expires)
                return {"status": "success", "message": "successful login",
                        "auth_token": auth_token}, 200

        return {"status": "fail", "message": "Unauthorised Access. Invalid email or password"}, 401
