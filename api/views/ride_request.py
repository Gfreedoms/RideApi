from api.modals.ride import Ride
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.tests import helpers


class RideRequest(Resource):
    """class RequestRide extends Resource class methods post"""

    @jwt_required
    def post(self, ride_id):
        """post method creates a ride request basing on the logged in user"""
        user_id = get_jwt_identity()
        ride = Ride(ride_id=ride_id)
        if ride.get_ride():

            if Ride.user_owns_ride(ride_id, user_id):
                return {"status": "fail", "message": "you can't request your own ride"}, 400

            else:
                request_id = Ride.create_ride_request(ride_id, user_id)
                return {"status": "success", "request_id": request_id, "message": "Request sent"}, 201

        return {"status": "fail", "message": "Ride not found"}, 404

    @jwt_required
    def get(self, ride_id):
        ride = Ride(ride_id=ride_id)
        if ride.get_ride():
            ride_requests = Ride.ride_requests(ride_id)
            if ride_requests:
                return {"status": "success", "requests": ride_requests}, 200

        return {"status": "fail", "message": "Ride not found"}, 404

    @jwt_required
    def put(self, ride_id, request_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True, help="status is required")
        data = parser.parse_args()

        missing_fields = helpers.check_missing_field(["status"], [data["status"]])

        if missing_fields:
            return {"message": missing_fields}, 400

        if not helpers.validate_status(data["status"]):
            return {"message": "wrong status, accepted values are 'accepted' or 'rejected' "}

        user_id = get_jwt_identity()

        if Ride.user_owns_ride(ride_id, user_id):
            ride_request = Ride.get_request(request_id)
            if ride_request:
                Ride.update_ride_request(ride_id, request_id, data["status"])
                return {"status": "success", "message": "request updated"}, 200
            else:
                return {"status": "fail", "message": "request does not exist"}, 404
        else:
            return {"status": "fail", "message": "you can't approve this request"}, 400
