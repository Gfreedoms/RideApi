import unittest
import json
from api.database.database_handler import DataBaseConnection
from api.settings import config
from api.tests import helpers
from api import app


class TestRide(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            connection = DataBaseConnection()
            connection.drop_test_tables()
            connection.create_tables()

    def test_configuration(self):
        self.assertTrue(config.SECRET_KEY is 'ride_api_key')

    def test_register_user(self):
        register_response = helpers.register_user(self, helpers.valid_user)
        data = json.loads(register_response.data.decode())

        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["auth_token"])
        self.assertEqual(register_response.status_code, 201)

    def test_register_mismatch_password(self):

        register_response = helpers.register_user(self, helpers.different_passwords_user)
        data = json.loads(register_response.data.decode())

        self.assertTrue(data["status"] == "fail")
        self.assertEqual(register_response.status_code, 400)

    def test_login_for_registered_user(self):
        """method tests for logging in of a registered user"""

        helpers.register_user(self, helpers.valid_user)

        login_response = helpers.login_user(self, helpers.valid_user)

        login_data = json.loads(login_response.data.decode())

        self.assertTrue(login_data["status"] == "success")
        self.assertTrue(login_data["auth_token"])
        self.assertEqual(login_response.status_code, 200)

    def test_login_invalid_credentials(self):

        user_response = helpers.register_user(self, helpers.valid_user)
        json.loads(user_response.data.decode())

        login_response = helpers.login_user(self, helpers.user_with_wrong_password)
        login_data = json.loads(login_response.data.decode())

        self.assertTrue(login_data["status"] == "fail")
        self.assertEqual(login_response.status_code, 401)

    def test_post_ride_offer(self):

        register_response = helpers.register_user(self, helpers.valid_user)
        register_data = json.loads(register_response.data.decode())

        post_ride_response = helpers.post_ride_offer(self, register_data["auth_token"], helpers.valid_ride)

        post_ride_data = json.loads(post_ride_response.data.decode())

        self.assertTrue(post_ride_data["status"] == "success")
        self.assertEqual(post_ride_response.status_code, 201)

    def test_get_all_rides(self):

        register_response = helpers.register_user(self, helpers.valid_user)
        data = json.loads(register_response.data.decode())

        helpers.post_ride_offer(self, data["auth_token"], helpers.valid_ride)

        get_rides_response = helpers.get_all_rides(self, data["auth_token"])
        self.assertEqual(get_rides_response.status_code, 200)

    def test_get_single_ride(self):

        register_response = helpers.register_user(self, helpers.valid_user)
        data = json.loads(register_response.data.decode())

        ride_response = helpers.post_ride_offer(self, data["auth_token"], helpers.valid_ride)
        ride_data = json.loads(ride_response.data.decode())

        self.assertTrue(ride_data["ride"]["ride_id"])
        get_ride_response = helpers.get_particular_ride(self, ride_data["ride"]["ride_id"], data["auth_token"])
        get_ride_data = json.loads(get_ride_response.data.decode())

        self.assertEqual(get_ride_data["status"], "success")
        self.assertEqual(get_ride_response.status_code, 200)

    def test_send_ride_request(self):

        first_user_response = helpers.register_user(self, helpers.valid_user)
        first_user_data = json.loads(first_user_response.data.decode())

        second_user_response = helpers.register_user(self, helpers.second_valid_user)
        second_user_data = json.loads(second_user_response.data.decode())

        ride_response = helpers.post_ride_offer(self, first_user_data["auth_token"], helpers.valid_ride)
        ride_data = json.loads(ride_response.data.decode())

        self.assertTrue(ride_data["ride"]["ride_id"])
        request_ride = helpers.request_ride_join(self, ride_data["ride"]["ride_id"],
                                                 second_user_data["auth_token"])

        request_ride_data = json.loads(request_ride.data.decode())
        self.assertTrue(request_ride_data["status"] == "success")
        self.assertEqual(request_ride.status_code, 201)

    def test_get_ride_with_invalid_ride_id(self):

        user_response = helpers.register_user(self, helpers.valid_user)
        user_data = json.loads(user_response.data.decode())

        # no ride will ever have id zero
        request_ride = helpers.get_particular_ride(self, 0, user_data["auth_token"])
        request_ride_data = json.loads(request_ride.data.decode())
        self.assertTrue(request_ride_data["status"] == "fail")
        self.assertEqual(request_ride.status_code, 404)

    def test_get_my_trips(self):
        """test user getting all his registered trips"""

        first_user_response = helpers.register_user(self, helpers.valid_user)
        first_user_data = json.loads(first_user_response.data.decode())

        second_user_response = helpers.register_user(self, helpers.second_valid_user)
        user2_data = json.loads(second_user_response.data.decode())

        # post ride for first user
        helpers.post_ride_offer(self, first_user_data["auth_token"], helpers.valid_ride)

        # post ride for second user
        second_user_ride_response = helpers.post_ride_offer(self, user2_data["auth_token"], helpers.valid_ride)

        second_user_ride_data = json.loads(second_user_ride_response.data.decode())

        helpers.request_ride_join(self, second_user_ride_data["ride"]["ride_id"], first_user_data["auth_token"])

        user_trips_response = helpers.get_my_trips(self, first_user_data["auth_token"])
        users_trips_data = json.loads(user_trips_response.data.decode())
        self.assertTrue(user_trips_response.status_code, 200)
        self.assertEqual(users_trips_data["status"], "success")
        self.assertIsInstance(users_trips_data["my_rides"], list)

    def tearDown(self):
        with app.app_context():
            connection = DataBaseConnection()
            connection.drop_test_tables()
            connection.create_tables()


if __name__ == "__main__":
    unittest.main()
