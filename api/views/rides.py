from api.modals.ride import Ride
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class RidesList(Resource):
    """RidesList extends Resource class methods get """
    @jwt_required
    def get(self):
        """returns all the rides in the system"""
        rides = Ride.get_all_rides()
        if rides:
            return {"status": "success", "rides": rides}, 200
        else:
            return {"status": "fail", "message": "no records in the database"}, 404
