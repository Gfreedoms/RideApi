import sys
import os
sys.path.append(os.path.pardir)
from api.rides import RidesList
from api.single_ride import SingleRide
from api.request_ride import RequestRide
from api.register_user import RegisterUser
from api.login import LoginUser
from api.my_trips import MyTrips

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(RidesList, '/api/v1/rides')  # get all rides
api.add_resource(SingleRide, '/api/v1/rides/<int:ride_id>', '/api/v1/rides')
api.add_resource(RegisterUser, '/api/v1/auth/register')  # register a user
api.add_resource(LoginUser, '/api/v1/auth/login')  # register a user
api.add_resource(RequestRide, '/api/v1/rides/<int:ride_id>/requests')
api.add_resource(MyTrips, '/api/v1/mytrips')

if __name__ == "__main__":
    app.run(debug=True)
