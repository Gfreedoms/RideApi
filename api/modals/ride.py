from pprint import pprint
from api.database.database import DataBaseConnection


class Request:
    def __init__(self, ride, request_id, owner_id, owner_name, requestor_name):
        self.request_id = request_id
        self.ride_id = ride.ride_id
        self.requestor_id = ride.user_id
        self.origin = ride.origin
        self.destination = ride.destination
        self.departure_time = ride.departure_time
        self.slots = ride.slots
        self.description = ride.description
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.requestor_name = requestor_name


class Ride:

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
                      VALUES (%s,%s,%s,%s,%s,%s) RETURNING ride_id;
                      """
        try:
            # create connection and set cursor
            connection = DataBaseConnection()
            cursor = connection.cursor
            cursor.execute(query_string, (ride.user_id, ride.origin, ride.destination,
                                          ride.departure_time, ride.slots, ride.description))

            return cursor.fetchone()[0]

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def get_all_rides():
        query_string = """
                     SELECT * FROM rides
                     """
        try:
            connection = DataBaseConnection()
            cursor = connection.dict_cursor
            cursor.execute(query_string)
            # connection.connection.close()
            row = cursor.fetchone()

            db_rides = []

            while row:
                temp_ride = Ride(row["ride_id"], row["user_id"], row["origin"], row["destination"],
                                 row["departure_time"].strftime("%Y-%m-%d %H:%M:%S"), row["slots"], row["description"])

                row = cursor.fetchone()
                db_rides.append(temp_ride.__dict__)

            pprint(db_rides)
            return db_rides

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def get_ride(ride_id):
        query_string = "SELECT * FROM rides WHERE ride_id = %s "

        try:
            connection = DataBaseConnection()
            cursor = connection.dict_cursor
            cursor.execute(query_string, [ride_id])
            # connection.connection.close()
            return cursor.fetchone()

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def create_ride_request(ride_id, user_id):
        query_string = "INSERT INTO ride_requests (ride_id,user_id,status) VALUES (%s,%s,%s)"

        try:
            connection = DataBaseConnection()
            connection.cursor.execute(query_string, (ride_id, user_id, "pending"))
            # connection.connection.close()
            return True

        except Exception as exp:
            pprint(exp)
            return None

    @staticmethod
    def ride_requests(ride_id):
        query = """SELECT rq.request_id,rq.status,rq.user_id as requestor_id,u.name as owner,r.*,u2.name as requestor  FROM ride_requests rq
                LEFT JOIN rides r ON (r.ride_id=rq.ride_id)
                LEFT JOIN users u on (u.user_id=r.user_id)
                LEFT JOIN users u2 on (u2.user_id=rq.user_id)
                WHERE rq.ride_id=%s
                """
        try:
            connection = DataBaseConnection()
            dict_cursor = connection.dict_cursor
            dict_cursor.execute(query, [ride_id])
            row = dict_cursor.fetchone()
            requests = []
            while row:
                ride = Ride(row["ride_id"], row["user_id"], row["origin"], row["destination"],
                            row["departure_time"].strftime("%Y-%m-%d %H:%M:%S"), row["slots"], row["description"])
                temp_request = Request(ride, row["request_id"], row["requestor_id"], row["owner"], row["requestor"])
                requests.append(temp_request.__dict__)
                row = dict_cursor.fetchone()
                requests.append(row)
            # connection.connection.close()
            return requests

        except Exception as exp:
            pprint(exp)

    def my_requests(self):
        my_requests = """
            SELECT rq.*,u.name,r.* as owner,u2.name as requestor  FROM ride_requests rq
            LEFT JOIN rides r ON (r.ride_id=rq.ride_id)
            LEFT JOIN users u on (u.user_id=r.user_id)
            LEFT JOIN users u2 on (u2.user_id=rq.user_id)
            WHERE rq.user_id=%s
            """
        try:
            connection = DataBaseConnection()
            dict_cursor = connection.dict_cursor
            dict_cursor.execute(my_requests, self.user_id)
            requests = dict_cursor.fetchmany()
            # connection.connection.close()
            return requests
        except Exception as exp:
            pprint(exp)

    @staticmethod
    def my_offers(user_id):
        my_offers = """
        SELECT * FROM rides WHERE user_id = %s 
        """

        try:
            connection = DataBaseConnection()
            dict_cursor = connection.dict_cursor
            dict_cursor.execute(my_offers, [user_id])
            offers = dict_cursor.fetchmany()
            # connection.connection.close()
            return offers
        except Exception as exp:
            pprint(exp)
