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
        connection = DataBaseConnection()
        connection.drop_test_tables()
        connection.create_tables()
        self.app = app.test_client()

    def test_configuration(self):
        self.assertTrue(config.SECRET_KEY is 'ride_api_key')

    def test_register_user(self):
        register_response = helpers.register_user(self, "stephen", "sample1@mail.com",
                                                  "123", "123")
        data = json.loads(register_response.data.decode())

        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["auth_token"])
        self.assertEqual(register_response.status_code, 201)

    def test_register_mismatch_password(self):

        register_response = helpers.register_user(self, "stephen", "sampleab@mail.com",
                                                  "123", "34e")
        data = json.loads(register_response.data.decode())

        self.assertTrue(data["status"] == "fail")
        self.assertEqual(register_response.status_code, 400)

    def test_login_for_registered_user(self):
        """method tests for logging in of a registered user"""

        helpers.register_user(self, "stephen", "sample7@mail.com", "123", "123")

        login_response = helpers.login_user(self, "sample7@mail.com", "123")
        login_data = json.loads(login_response.data.decode())

        self.assertTrue(login_data["status"] == "success")
        self.assertTrue(login_data["auth_token"])
        self.assertEqual(login_response.status_code, 200)

    def test_login_invalid_credentials(self):

        user_response = helpers.register_user(self, "stephen", "samplesss@mail.com",
                                              "123", "123")
        json.loads(user_response.data.decode())

        # attempt to login user but with wrong password
        login_response = helpers.login_user(self, "samplesss@mail.com", "fsd")
        login_data = json.loads(login_response.data.decode())

        self.assertTrue(login_data["status"] == "fail")
        self.assertEqual(login_response.status_code, 401)
    
    def test_post_ride_offer(self):

        register_response = helpers.register_user(self, "stephen", "sample2@mail.com",
                                                  "123", "123")
        register_data = json.loads(register_response.data.decode())

        post_ride_response = helpers.post_ride_offer(self, register_data["auth_token"], "masaka", "mbale",
                                                     "2018-06-10 13:00", 3, "This is just a sample request");
        post_ride_data = json.loads(post_ride_response.data.decode())

        self.assertTrue(post_ride_data["status"] == "success")
        self.assertEqual(post_ride_response.status_code, 201)

    def test_get_all_rides(self):

        register_response = helpers.register_user(self, "stephen", "sample3@mail.com",
                                                  "123", "123")
        data = json.loads(register_response.data.decode())
        
        # register at least 2 rides using users token
        helpers.post_ride_offer(self, data["auth_token"], "masaka", "mbale",
                                "2018-06-10 13:00", 3, "This is just a sample request")
        helpers.post_ride_offer(self, data["auth_token"], "masaka", "mbale",
                                "2018-06-10 13:00", 3, "This is just a sample request")
        
        # fetch the rides
        get_rides_response = helpers.get_all_rides(self, data["auth_token"])
        self.assertEqual(get_rides_response.status_code, 200)

    def test_get_single_ride(self):

        register_response = helpers.register_user(self, "stephen", "sample4@mail.com",
                                                  "123", "123")
        data = json.loads(register_response.data.decode())

        ride_response = helpers.post_ride_offer(self, data["auth_token"], "masaka", "mbale",
                                                "2018-06-10 13:00", 3, "This is a")
        ride_data = json.loads(ride_response.data.decode())

        get_ride_response = helpers.get_particular_ride(self, ride_data["ride"]["ride_id"], data["auth_token"])
        get_ride_data = json.loads(get_ride_response.data.decode())

        self.assertEqual(get_ride_data["status"], "success")
        self.assertEqual(get_ride_response.status_code, 200)

    def test_send_ride_request(self):

        user1_response = helpers.register_user(self, "stephen", "sample5@mail.com",
                                               "123", "123")
        user1_data = json.loads(user1_response.data.decode())

        user2_response = helpers.register_user(self, "stephen", "sample6@mail.com",
                                               "123", "123")
        user2_data = json.loads(user2_response.data.decode())

        ride_response = helpers.post_ride_offer(self, user1_data["auth_token"], "masaka", "mbale",
                                                "2018-05-4 13:00", 3, "This is jus")
        ride_data = json.loads(ride_response.data.decode())

        request_ride = helpers.request_ride_join(self, ride_data["ride"]["ride_id"],
                                                 user2_data["auth_token"])

        request_ride_data = json.loads(request_ride.data.decode())
        self.assertTrue(request_ride_data["status"] == "success")
        self.assertEqual(request_ride.status_code, 201)

    def test_get_ride_with_invalid_ride_id(self):

        user_response = helpers.register_user(self, "stephen", "sample5@mail.com",
                                              "123", "123")
        user_data = json.loads(user_response.data.decode())

        # no ride will ever have id zero
        request_ride = helpers.get_particular_ride(self, 0, user_data["auth_token"])
        request_ride_data = json.loads(request_ride.data.decode())
        self.assertTrue(request_ride_data["status"] == "fail")
        self.assertEqual(request_ride.status_code, 404)

    def test_get_my_trips(self):
        """test user getting all his registered trips"""

        user1_response = helpers.register_user(self, "stephen", "sample9@mail.com",
                                               "123", "123")
        user1_data = json.loads(user1_response.data.decode())

        user2_response = helpers.register_user(self, "stephen", "sample10@mail.com",
                                               "123", "123")
        user2_data = json.loads(user2_response.data.decode())

        helpers.post_ride_offer(self, user1_data["auth_token"],
                                                 "masaka", "mbale", "14/06/2018 13:00",
                                                 3, "This is just a sample request")

        helpers.post_ride_offer(self, user1_data["auth_token"], "kabale",
                                                 "tororo", "14/06/2018 13:00",
                                                 3, "This is just a sample request")

        ride_response3 = helpers.post_ride_offer(self, user2_data["auth_token"],
                                                 "makerere", "bugolobi", "14/06/2018 13:00",
                                                 3, "This is just a sample request")

        ride3_data = json.loads(ride_response3.data.decode())

        helpers.request_ride_join(self, ride3_data["ride"]["ride_id"], user1_data["auth_token"])

        user_trips_response = helpers.get_my_trips(self, user1_data["auth_token"])
        users_trips_data = json.loads(user_trips_response.data.decode())
        self.assertTrue(user_trips_response.status_code, 200)
        self.assertEqual(users_trips_data["status"], "success")
        self.assertIsInstance(users_trips_data["my_rides"], list)

    # def test_get_rides_wrong_token(self):
    #
    #     user_trips_response = helpers.get_my_trips(self, "jwt faketoken")
    #     users_trips_data = json.loads(user_trips_response.data.decode())
    #
    #     self.assertTrue(user_trips_response.status_code, 401)
    #     self.assertEqual(users_trips_data["status"], "fail")

    def tearDown(self):
        connection = DataBaseConnection()
        connection.drop_test_tables()
        connection.create_tables()


if __name__ == "__main__":
    unittest.main()
