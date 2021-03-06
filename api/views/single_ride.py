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
        ride = Ride(ride_id=ride_id)
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

        length_violations = helpers.check_length_restrictions(["origin", "destination",
                                                               "departure_time", "description"],
                                                              [data["origin"], data["destination"],
                                                               data["departure_time"], data["description"]])

        error_found = False

        if length_violations:
            error_found = True
            message = length_violations

        if missing_fields:
            error_found = True
            message = missing_fields

        if not helpers.validate_date(data["departure_time"]):
            error_found = True
            message = "Incorrect data format, should be YYYY-MM-DD HH:MM"

        if not helpers.convert_to_int(data["slots"]):
            error_found = True
            message = "slots must be int"

        if error_found:
            return {"status": "fail", "message:": message}, 400

        user_id = get_jwt_identity()
        temp_ride = Ride(user_id=user_id, origin=data["origin"], destination=data["destination"],
                         departure_time=data["departure_time"], slots=data["slots"], description=data["description"])

        ride_id = temp_ride.create_ride()

        temp_ride.ride_id = ride_id
        return {"status": "success", "ride": temp_ride.__dict__}, 201
