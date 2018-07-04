from api.views.rides import RidesList
from api.views.single_ride import SingleRide
from api.views.ride_request import RideRequest
from api.views.register_user import RegisterUser
from api.views.login import LoginUser
from api.views.my_trips import MyTrips
from api.database.database import DataBaseConnection
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api.settings import config

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
jwt = JWTManager(app)

app.config['TESTING'] = False
app.config['DEBUG'] = True

app.config.from_object(__name__)


api.add_resource(RidesList, '/api/v1/rides')  # get all rides
api.add_resource(SingleRide, '/api/v1/rides/<int:ride_id>', '/api/v1/users/rides')
api.add_resource(RegisterUser, '/api/v1/auth/signup')  # register a user
api.add_resource(LoginUser, '/api/v1/auth/login')  # login a user
api.add_resource(RideRequest, '/api/v1/rides/<int:ride_id>/requests',
                 '/api/v1/users/rides/<int:ride_id>/requests',
                 '/api/v1/users/rides/<int:ride_id>/requests/<int:request_id>')

api.add_resource(MyTrips, '/api/v1/mytrips')
