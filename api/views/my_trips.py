from api.modals.ride import Ride
from api.modals.user import User

from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required


class MyTrips(Resource):
    """MyTrips class inherits from Resource"""
    # @jwt_required
    def get(self):
        """method get returns all the rides taken or offered by the logged in user"""
        header_token = request.headers.get('Authorization')
        if header_token:
            user_token = header_token.split(" ")[1]
            user_id = User.decode_authentication_token(user_token)

            if isinstance(user_id, int):
                # then get all rides posted by this person using the got id
                user_rides = Ride.my_offers(user_id)

                # get all the ride requests by this person
                user_requests = Ride.my_requests(user_id)

                return {"status": "success", "message": "successful return",
                        "my_rides": user_rides, "my_requests": user_requests}

        return {"status": "fail", "message": "unregistered user"}, 404
