import json


def register_user(self, users_name, user_email, password1, password2):
    """method register_user sends a request to register a user
       parameters name,email,password,confirm_password
       returns json response with users token"""

    return self.app.post('/api/v1/auth/register', data=json.dumps(dict(email=user_email, name=users_name,
                                                                       password=password1, confirm=password2)),
                         content_type='application/json')


def login_user(self, user_email, password1):
    """method login_user sends a request to login user
       parameters email,password
       returns json response with users token"""

    return self.app.post('/api/v1/auth/login', data=json.dumps(dict(email=user_email, password=password1)),
                         content_type='application/json')


def request_ride_join(self, ride_id, auth_token):
    """method request_ride_join sends a request for a given user to join a ride
       parameters ride_id,auth_token
       returns json response"""
    return self.app.post('/api/v1/rides/'+str(ride_id)+'/requests', headers=dict(Authorization='jwt '+auth_token),
                         content_type='application/json')


def post_ride_offer(self, user_token, ride_from, ride_to, dept_date, ride_time, slots, description):
    """method post_ride_offer sends a request for registering a ride
       parameters users_token,from,to,date,time,slots,description
       returns json response"""

    return self.app.post('/api/v1/rides', headers=dict(Authorization='jwt '+user_token),
                         data=json.dumps(dict(origin=ride_from, destination=ride_to, dept_date=dept_date,
                                              dept_time=ride_time, slots=slots, description=description)),
                         content_type='application/json')


def get_particular_ride(self, ride_id):
    """method get_particular_ride sends a request to return details of a given ride
        parameters self,ride_id
        returns json response"""
    return self.app.get('/api/v1/rides/'+str(ride_id))


def get_all_rides(self):
    """method get_all_rides sends a request to return all ride offers in the system
        returns json response"""
    return self.app.get('/api/v1/rides')


def get_my_trips(self, auth_token):
    """method get_my_trips sends a request to get all rides the user has taken or given"""
    
    return self.app.get('/api/v1/mytrips', headers=dict(Authorization='jwt '+auth_token),
                        content_type='application/json')
