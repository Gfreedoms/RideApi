from api.modals.user import User
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class MyTrips(Resource):
    """MyTrips class inherits from Resource"""

    @jwt_required
    def get(self):
        """method get returns all the rides taken or offered by the logged in user"""

        user_id = get_jwt_identity()

        user = User(user_id)
        user_rides = user.my_offers()

        user_requests = user.my_requests()

        return {"status": "success",
                "my_rides": user_rides, "my_requests": user_requests}, 200
