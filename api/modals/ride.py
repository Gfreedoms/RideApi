from pprint import pprint
from api.database.database import DataBaseConnection


class Ride:
    connection = DataBaseConnection()

    def __init__(self, ride_id, user_id, origin, destination, departure_time, slots, description):
        self.ride_id = ride_id
        self.user_id = user_id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.slots = slots
        self.description = description

    @staticmethod
    def create_ride(ride):
        query_string = """
                      INSERT INTO rides (user_id, origin, destination, departure_time, slots, description) 
                      VALUES (%s,%s,%s,%s,%s,%s)
                      """
        try:
            # create connection and set cursor

            Ride.connection.cursor.execute(query_string, (ride.user_id, ride.origin, ride.destination,
                                           ride.departure_time, ride.slots, ride.description))
        except Exception as exp:
            pprint(exp)

    @staticmethod
    def get_all_rides():
        query_string = """
                     SELECT * FROM rides
                     """
        try:
            cursor = Ride.connection.dict_cursor
            cursor.execute(query_string)
            return cursor.fetchmany()

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def get_ride(ride_id):
        query_string = "SELECT * FROM rides WHERE ride_id = %s "

        try:

            cursor = Ride.connection.dict_cursor
            cursor.execute(query_string, [ride_id])
            return cursor.fetchone()

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def create_ride_request(ride_id, user_id):
        query_string = "INSERT INTO ride_requests (ride_id,user_id,status) VALUES (%s,%s,%s)"

        try:

            Ride.connection.cursor.execute(query_string, (ride_id, user_id, "pending"))
            return True

        except Exception as exp:
            pprint(exp)
            return None

    def my_requests(self):
        my_requests = """
            """

        try:

            dict_cursor = Ride.connection.dict_cursor
            dict_cursor.execute(my_requests, self.user_id)
            requests = dict_cursor.fetchmany()
            return requests
        except Exception as exp:
            pprint(exp)

    def my_offers(self):
        my_offers = """
        """

        try:

            dict_cursor = Ride.connection.dict_cursor
            dict_cursor.execute(my_offers, [self.user_id])
            offers = dict_cursor.fetchmany()
            return offers
        except Exception as exp:
            pprint(exp)
