from api.modals.ride import Ride
from flask_restful import Resource


class RidesList(Resource):
    """RidesList extends Resource class methods get """
    def get(self):
        """returns all the rides in the system"""
        rides = Ride.get_all_rides()
        if rides:
            return {"status": "success", "rides": rides}, 200
        else:
            return {"status": "fail", "message": "no records in the database"}, 404
