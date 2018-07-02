import pytest
import unittest
from api import rideapi
import json
from api.modals.user import User
from api.settings import config
from api.tests import helpers

class TestRide(unittest.TestCase):
    def setUp(self):
        self.app = rideapi.app.test_client()

    def test_configuration(self):
        self.assertTrue(config.SECRET_KEY is 'ride_api_key')

    def test_register_user(self):
        # register user
        register_response = helpers.register_user(self,"stephen","sample1@mail.com","123","123")
        data = json.loads(register_response.data.decode())
        
        # test response data
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["auth_token"])
        self.assertEqual(register_response.status_code, 201)

    def test_register_mismatch_password(self):
        # register user
        register_response = helpers.register_user(self,"stephen","sampleab@mail.com","123","34e")
        data = json.loads(register_response.data.decode())
        
        # test responce data
        self.assertTrue(data["status"] == "fail")
        self.assertEqual(register_response.status_code, 400)

    def test_login_for_registered_user(self):
        """method tests for logging in of a registered user"""
       
        # register 1 users 
        user_response = helpers.register_user(self,"stephen","sample7@mail.com","123","123")
        user_data = json.loads(user_response.data.decode())

        #test register
        self.assertTrue(user_data["status"] == "success")
        self.assertTrue(user_data["auth_token"])
        self.assertEqual(user_response.status_code, 201)

        #attempt to login user
        login_response = helpers.login_user(self,"sample7@mail.com","123")
        login_data = json.loads(login_response.data.decode())

        # test login to a user that has been created on register at the start of the method
        self.assertTrue(login_data["status"] == "success")
        self.assertTrue(login_data["auth_token"])
        self.assertEqual(login_response.status_code, 200)

    def test_login_invalid_credentials(self):
         # register 1 users 
        user_response = helpers.register_user(self,"stephen","samplesss@mail.com","123","123")
        user_data = json.loads(user_response.data.decode())

        #test register
        self.assertTrue(user_data["status"] == "success")
        self.assertTrue(user_data["auth_token"])
        self.assertEqual(user_response.status_code, 201)

        #attempt to login user but with wrong password
        login_response = helpers.login_user(self,"samplesss@mail.com","fsd")
        login_data = json.loads(login_response.data.decode())

        # test login to a user that has been created on register at the start of the method
        self.assertTrue(login_data["status"] == "fail")
        self.assertEqual(login_response.status_code, 401)
    
    def test_post_ride_offer(self):
        # register user
        register_response = helpers.register_user(self,"stephen","sample2@mail.com","123","123")
        data = json.loads(register_response.data.decode())
        
        # test register response data 
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["auth_token"])
        self.assertEqual(register_response.status_code, 201)

        # use user's token to register an offer
        post_ride_response=helpers.post_ride_offer(self,data["auth_token"],"masaka","mbale","14/06/2018","13:00",3,"This is just a sample request");
        post_ride_data=json.loads(post_ride_response.data.decode())
        
        # test response data
        self.assertTrue(post_ride_data["status"] == "success")
        self.assertEqual(post_ride_response.status_code, 201)

    def test_get_all_rides(self):
        # register user 
        register_response = helpers.register_user(self,"stephen","sample3@mail.com","123","123")
        data = json.loads(register_response.data.decode())
        
        # register atleast 2 rides using users token
        helpers.post_ride_offer(self,data["auth_token"],"masaka","mbale","14/06/2018","13:00",3,"This is just a sample request");
        helpers.post_ride_offer(self,data["auth_token"],"masaka","mbale","14/06/2018","13:00",3,"This is just a sample request");
        
        # fetch the rides
        get_rides_response = helpers.get_all_rides(self)
        self.assertEqual(get_rides_response.status_code, 200)
    
    def test_single_ride(self):
        
        # register user 
        register_response = helpers.register_user(self,"stephen","sample4@mail.com","123","123")
        data = json.loads(register_response.data.decode())

        # create the ride
        ride_response=helpers.post_ride_offer(self,data["auth_token"],"masaka","mbale","14/06/2018","13:00",3,"This is just a sample request");
        ride_data=json.loads(ride_response.data.decode())

        # fetch the created ride
        get_ride_response = helpers.get_particular_ride(self,ride_data['ride']['id'])
        get_ride_data = json.loads(get_ride_response.data.decode())

        self.assertEqual(get_ride_data["status"],"success")
        self.assertEqual(get_ride_response.status_code, 200)
    
    def test_send_ride_request(self): 
        
        # register atleast 2 users 
        user1_response = helpers.register_user(self,"stephen","sample5@mail.com","123","123")
        user1_data = json.loads(user1_response.data.decode())

        user2_response = helpers.register_user(self,"stephen","sample6@mail.com","123","123")
        user2_data = json.loads(user2_response.data.decode())

        # create ride using user1's token
        ride_response=helpers.post_ride_offer(self,user1_data["auth_token"],"masaka","mbale","14/06/2018","13:00",3,"This is just a sample request");
        ride_data=json.loads(ride_response.data.decode())
        
        #then send request to join ride using this person2's token
        request_ride = helpers.request_ride_join(self,ride_data["ride"]["id"],user2_data["auth_token"]);

        request_ride_data = json.loads(request_ride.data.decode())
        self.assertTrue(request_ride_data["status"] == "success")
        self.assertEqual(request_ride.status_code,201)
    
    def test_get_ride_with_invalid_ride_id(self):
        
        request_ride = helpers.get_particular_ride(self,11);
        request_ride_data = json.loads(request_ride.data.decode())
        self.assertTrue(request_ride_data["status"] == "fail")
        self.assertEqual(request_ride.status_code, 404)

    def test_request_ride_wrong_authentication_code(self):
        user_response = helpers.register_user(self,"stephen","sample123@mail.com","123","123")
        user_data = json.loads(user_response.data.decode())

        # create ride using user1's token
        ride_response=helpers.post_ride_offer(self,user_data["auth_token"],"masaka","mbale","14/06/2018","13:00",3,"This is just a sample request");
        ride_data=json.loads(ride_response.data.decode())
        
        #then send request to join ride using this person's token
        request_ride = helpers.request_ride_join(self,ride_data["ride"]["id"],'jwt fakeauth');

        request_ride_data = json.loads(request_ride.data.decode())
        self.assertTrue(request_ride_data["status"] == "fail")
        self.assertEqual(request_ride.status_code,401)

    def test_get_my_trips(self):
        """test user getting all his registered trips"""
        
        # register atleast 2 users 
        user1_response = helpers.register_user(self,"stephen","sample9@mail.com","123","123")
        user1_data = json.loads(user1_response.data.decode())
        
        user2_response = helpers.register_user(self,"stephen","sample10@mail.com","123","123")
        user2_data = json.loads(user2_response.data.decode())

        # create ride using user1's token
        ride_response1=helpers.post_ride_offer(self,user1_data["auth_token"],"masaka","mbale","14/06/2018","13:00",3,"This is just a sample request");
        ride_response2=helpers.post_ride_offer(self,user1_data["auth_token"],"kabale","tororo","14/06/2018","13:00",3,"This is just a sample request");
        
        # create ride using user2 token
        ride_response3=helpers.post_ride_offer(self,user2_data["auth_token"],"makerere","bugolobi","14/06/2018","13:00",3,"This is just a sample request");
        
        ride3_data=json.loads(ride_response3.data.decode())
        
        #then send request to join ride using this person1's token
        request_ride = helpers.request_ride_join(self,ride3_data["ride"]["id"],user1_data["auth_token"]);
        
        # request all trips for the user and check 
        mytrips_response=helpers.get_my_trips(self,user1_data["auth_token"])
        mytrips_data=json.loads(mytrips_response.data.decode())
        self.assertTrue(mytrips_response.status_code,200)
        self.assertEqual(mytrips_data["status"], "success")
        self.assertIsInstance(mytrips_data["my_rides"],list)
        
    def test_get_rides_wrong_token(self):
        # request all trips for the user and check 
        mytrips_response=helpers.get_my_trips(self,"jwt faketoken")
        mytrips_data=json.loads(mytrips_response.data.decode())

        self.assertTrue(mytrips_response.status_code,401)
        self.assertEqual(mytrips_data["status"], "fail")

if __name__ == "__main__":
    unittest.main()