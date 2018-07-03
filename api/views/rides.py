from api.modals.ride import Ride
from flask_restful import Resource


class RidesList(Resource):
    """RidesList extends Resource class methods get """
    def get(self):
        """returns all the rides in the system"""
        rides = []
        rows = Ride.get_all_rides()
        for row in rows:
            temp_ride = Ride(row["ride_id"], row["user_id"], row["origin"], row["destination"],
                             row["departure_time"].strftime("%Y-%m-%d %H:%M:%S"), row["slots"], row["description"])

            rides.append(temp_ride.__dict__)
        return {"rides": rides}, 200
