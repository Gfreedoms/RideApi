from api.modals.ride import Ride
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity


class SingleRide(Resource):
    """class SingleRide extends Resource class methods get
     which returns a given ride, post for creating a ride offer"""
    @jwt_required
    def get(self, ride_id):
        """returns a ride matching a given id"""

        row = Ride.get_ride(ride_id)
        if row:
            ride = Ride(row["ride_id"], row["user_id"], row["origin"], row["destination"],
                        row["departure_time"].strftime("%Y-%m-%d %H:%M:%S"), row["slots"], row["description"])

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

        user_id = get_jwt_identity()
        temp_ride = Ride(None, user_id, data["origin"], data["destination"], data["departure_time"], data["slots"], data["description"])

        ride_id = Ride.create_ride(temp_ride)
        temp_ride.ride_id = ride_id
        return {"status": "success", "ride": temp_ride.__dict__}, 201
