from api.modals.user import User
from api.modals.ride import Ride
from flask import request
from flask_restful import Resource
# from flask_jwt import jwt_required


class RideRequest(Resource):
    """class RequestRide extends Resource class methods post"""
    # @jwt_required()
    def post(self, ride_id):
        """post method creates a ride request basing on the logged in user"""
        header_token = request.headers.get('Authorization')
        if header_token:
            user_token = header_token.split(" ")[1]
            user_id = User.decode_authentication_token(user_token)

            if isinstance(user_id, int):
                # check if ride exits
                if Ride.get_ride(ride_id):
                    Ride.create_ride_request(ride_id, user_id)
                    return {"status": "success", "message": "Request sent"}, 201

        return {"status": "fail", "message": "Request Rejected, Login to request a ride"}, 401

    def get(self, ride_id):
        header_token = request.headers.get('Authorization')
        if header_token:
            user_token = header_token.split(" ")[1]
            user_id = User.decode_authentication_token(user_token)

            if isinstance(user_id, int):
                # check if ride exits
                requests = Ride.ride_requests(ride_id)
                return {"status": "success", "requests": requests}, 200

        return {"status": "fail", "message": "Request Rejected, Login to request a ride"}, 401

