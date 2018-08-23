import datetime
import json
from api.modals.user import User
from api.modals.ride import Ride
import re

valid_user = User(name="stephen", email="sample1@mail.com", password="123", confirm="123")

user_with_missing_values = User(email="sample1@mail.com")
user_with_malformed_email = User(name="stephen2", email="", password="123", confirm="123")
second_valid_user = User(name="stephen", email="sample2@mail.com", password="333", confirm="333")

user_with_wrong_password = User(name="", email="sample1@mail.com", password="344", confirm="")
different_passwords_user = User(name="stephen", email="sample1@mail.com", password="hhd", confirm="hhd2")

valid_ride = Ride(origin="masaka", destination="mbale", departure_time="2018-06-10 13:00",
                  slots=3, description="This is just a sample request")

missing_values_ride = Ride()


def register_user(self, user):
    """method register_user sends a request to register a user
       parameters name,email,password,confirm_password
       returns json response with users token"""

    return self.app.post('/api/v1/auth/signup', data=json.dumps(dict(email=user.email, name=user.name,
                                                                     password=user.password, confirm=user.confirm)),
                         content_type='application/json')


def login_user(self, user):
    """method login_user sends a request to login user
       parameters email,password
       returns json response with users token"""

    return self.app.post('/api/v1/auth/login', data=json.dumps(dict(email=user.email, password=user.password)),
                         content_type='application/json')


def request_ride_join(self, ride_id, auth_token):
    """method request_ride_join sends a request for a given user to join a ride
       parameters ride_id,auth_token
       returns json response"""
    return self.app.post('/api/v1/rides/'+str(ride_id)+'/requests', headers=dict(Authorization='Bearer '+auth_token),
                         content_type='application/json')


def post_ride_offer(self, user_token, ride):
    """method post_ride_offer sends a request for registering a ride
       parameters users_token,from,to,date,time,slots,description
       returns json response"""

    return self.app.post('/api/v1/users/rides', headers=dict(Authorization='Bearer '+user_token),
                         data=json.dumps(dict(origin=ride.origin, destination=ride.destination,
                                              departure_time=ride.departure_time,
                                              slots=ride.slots, description=ride.description)),
                         content_type='application/json')


def get_particular_ride(self, ride_id, auth_token):
    """method get_particular_ride sends a request to return details of a given ride
        parameters self,ride_id
        returns json response"""
    return self.app.get('/api/v1/rides/'+str(ride_id),
                        headers=dict(Authorization='Bearer '+auth_token),
                        content_type='application/json')


def get_all_rides(self, auth_token):
    """method get_all_rides sends a request to return all ride offers in the system
        returns json response"""
    return self.app.get('/api/v1/rides', headers=dict(Authorization='Bearer '+auth_token),
                        content_type='application/json')


def update_request(self, ride_id, request_id, auth_token, status):
    """method sends a put request to update a ride request to either accepted or rejected"""
    return self.app.put('/api/v1/users/rides/'+str(ride_id)+'/requests/'+str(request_id),
                        headers=dict(Authorization='Bearer '+auth_token),
                        data=json.dumps(dict(status=status)),
                        content_type='application/json')


def get_ride_requests(self, ride_id, auth_token):
    """method sends a get request to return all the requests on a given ride"""
    return self.app.get('/api/v1/users/rides/'+str(ride_id)+'/requests', headers=dict(Authorization='Bearer '+auth_token),
                        content_type='application/json')


def get_my_trips(self, auth_token):
    """method get_my_trips sends a request to get all rides the user has taken or given"""
    
    return self.app.get('/api/v1/mytrips', headers=dict(Authorization='Bearer '+auth_token),
                        content_type='application/json')


def check_missing_field(fields, values):
    message = []
    for i in range(0, len(fields)):
        if not values[i]:
            ans = fields[i]+" can't be blank"
            message.append(ans)
    if message:
        return ' , '.join(message)
    else:
        return False


def validate_status(status):
    if status.lower() == "accepted" or status.lower() == "rejected":
        return True
    else:
        return False


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email, flags=0):
        return False
    else:
        return True


def validate_date(date_txt):
    try:
        datetime.datetime.strptime(date_txt, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False


def convert_to_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
