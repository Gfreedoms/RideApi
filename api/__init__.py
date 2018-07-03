from api.views.rides import RidesList
from api.views.single_ride import SingleRide
from api.views.request_ride import RequestRide
from api.views.register_user import RegisterUser
from api.views.login import LoginUser
from api.views.my_trips import MyTrips
from api.database.database import DataBaseConnection
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)
app.config['TESTING'] = False
app.config['DEBUG'] = True
if app.config['TESTING']:
    app.config["DATABASE"] = "myway_test"
else:
    app.config["DATABASE"] = "myway"


app.config.from_object(__name__)
# app.config.from_object('configmodule.DevelopmentConfig')
print(app.config["DATABASE"])

api.add_resource(RidesList, '/api/v1/rides')  # get all rides
api.add_resource(SingleRide, '/api/v1/rides/<int:ride_id>', '/api/v1/rides')
api.add_resource(RegisterUser, '/api/v1/auth/register')  # register a user
api.add_resource(LoginUser, '/api/v1/auth/login')  # register a user
api.add_resource(RequestRide, '/api/v1/rides/<int:ride_id>/requests')
api.add_resource(MyTrips, '/api/v1/mytrips')
