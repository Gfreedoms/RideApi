from api.modals.ride import Ride
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.tests import helpers


class SingleRide(Resource):
    """class SingleRide extends Resource class methods get
     which returns a given ride, post for creating a ride offer"""
    @jwt_required
    def get(self, ride_id):
        """returns a ride matching a given id"""
        ride = Ride(ride_id, None, None, None, None, None, None)
        row = ride.get_ride()

        if row:
            ride.user_id = row["user_id"]
            ride.origin = row["origin"]
            ride.destination = row["destination"]
            ride.departure_time = row["departure_time"].strftime("%Y-%m-%d %H:%M:%S")
            ride.slots = row["slots"]
            ride.description = row["description"]

            return {"status": "success", "ride": ride.__dict__}, 200
        else:
            return {"status": "fail", "message": "ride not found"}, 404

        return {"status": "fail", "message": "unauthorised access"}, 401

    @jwt_required
    def post(self):
        """creates a new ride offer"""
        parser = reqparse.RequestParser()
        parser.add_argument('origin', type=str, required=True, help="origin field is required")
        parser.add_argument('destination', type=str, required=True, help="destination field is required")
        parser.add_argument('departure_time', type=str, required=True, help="departure_time field is required")
        parser.add_argument('slots', type=str, required=True, help="slots field is required")
        parser.add_argument('description', type=str, required=True, help="description field is required")
        data = parser.parse_args()

        missing_fields = helpers.check_missing_field(
            ["origin", "destination", "departure_time", "slots", "description"],
            [data["origin"], data["destination"], data["departure_time"], data["slots"], data["description"]]
        )

        if missing_fields:
            return {"message:": missing_fields}, 400

        user_id = get_jwt_identity()
        temp_ride = Ride(None, user_id, data["origin"], data["destination"], data["departure_time"], data["slots"], data["description"])

        ride_id = temp_ride.create_ride()

        temp_ride.ride_id = ride_id
        return {"status": "success", "ride": temp_ride.__dict__}, 201
