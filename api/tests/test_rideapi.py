import unittest

import json

from api.database.database import DataBaseConnection
from api.settings import config
from api.tests import helpers
from api import app


class TestRide(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['DATABASE'] = "myway"
        connection = DataBaseConnection(app.config["DATABASE"])
        connection.drop_test_tables()
        connection.create_tables()
        self.app = app.test_client()

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
        
        # test response data
        self.assertTrue(data["status"] == "fail")
        self.assertEqual(register_response.status_code, 400)

    def test_login_for_registered_user(self):
        """method tests for logging in of a registered user"""
       
        # register 1 users 
        user_response = helpers.register_user(self, "stephen",
                                              "sample7@mail.com", "123", "123")
        user_data = json.loads(user_response.data.decode())

        # test register
        self.assertTrue(user_data["status"] == "success")
        self.assertTrue(user_data["auth_token"])
        self.assertEqual(user_response.status_code, 201)

        # attempt to login user
        login_response = helpers.login_user(self, "sample7@mail.com", "123")
        login_data = json.loads(login_response.data.decode())

        # test login to a user that has been created on register at the start of the method
        self.assertTrue(login_data["status"] == "success")
        self.assertTrue(login_data["auth_token"])
        self.assertEqual(login_response.status_code, 200)

    def test_login_invalid_credentials(self):

        # register 1 users
        user_response = helpers.register_user(self,"stephen","samplesss@mail.com","123","123")
        user_data = json.loads(user_response.data.decode())

        # test register
        self.assertTrue(user_data["status"] == "success")
        self.assertTrue(user_data["auth_token"])
        self.assertEqual(user_response.status_code, 201)

        # attempt to login user but with wrong password
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
        post_ride_response=helpers.post_ride_offer(self,data["auth_token"],"masaka","mbale","2018-06-10 13:00",3,"This is just a sample request");
        post_ride_data=json.loads(post_ride_response.data.decode())
        
        # test response data
        self.assertTrue(post_ride_data["status"] == "success")
        self.assertEqual(post_ride_response.status_code, 201)

    def test_get_all_rides(self):
        # register user 
        register_response = helpers.register_user(self,"stephen","sample3@mail.com","123","123")
        data = json.loads(register_response.data.decode())
        
        # register atleast 2 rides using users token
        helpers.post_ride_offer(self,data["auth_token"],"masaka","mbale","2018-06-10 13:00",3,"This is just a sample request");
        helpers.post_ride_offer(self,data["auth_token"],"masaka","mbale","2018-06-10 13:00",3,"This is just a sample request");
        
        # fetch the rides
        get_rides_response = helpers.get_all_rides(self)
        self.assertEqual(get_rides_response.status_code, 200)

    # to be called after tests have run
    def tearDown(self):
        connection = DataBaseConnection(app.config["DATABASE"])
        connection.drop_test_tables()
        connection.create_tables()


if __name__ == "__main__":
    unittest.main()
