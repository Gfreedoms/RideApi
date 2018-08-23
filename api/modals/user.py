from api.database.database_handler import DataBaseConnection
from api.modals.ride import Ride


class User:
    """User class defines the methods needed by user and the attributes.
        on creation pass in id,name,email,password"""

    def __init__(self, **kwargs):

        allowed_keys = set(['id', 'name', 'email', 'password', 'confirm'])
        self.__dict__.update((key, None) for key in allowed_keys)
        self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)

    def create_user(self):
        connection = DataBaseConnection()
        cursor = connection.cursor
        query_string = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
        cursor.execute(query_string, (self.name, self.email, self.password))

    @staticmethod   
    def get_user_by_email(email):
        connection = DataBaseConnection()
        cursor = connection.dict_cursor
        query_string = "SELECT * FROM users WHERE email = %s "
        cursor.execute(query_string, [email])
        row = cursor.fetchone()
        return row
    
    @staticmethod
    def get_all_users():
        connection = DataBaseConnection()
        cursor = connection.dict_cursor
        query_string = "SELECT * FROM users"
        cursor.execute(query_string)
        return cursor.fetchall()

    def my_offers(self):
        my_offers = """
            SELECT * FROM rides WHERE user_id = %s 
            """

        try:
            connection = DataBaseConnection()
            cursor = connection.dict_cursor
            cursor.execute(my_offers, (self.id,))
            row = cursor.fetchone()
            offers = []
            while row:
                temp_ride = Ride.create_ride_instance(row)
                row = cursor.fetchone()
                offers.append(temp_ride.__dict__)
            return offers
        except Exception as exp:
            print(exp)

    def my_requests(self):

        my_requests = """SELECT rq.request_id,rq.status,rq.user_id as requestor_id,rq.status,u.name as owner,u.user_id as owner_id,
                        r.*,u2.name as requestor  FROM ride_requests rq
                        LEFT JOIN rides r ON (r.ride_id=rq.ride_id)
                        LEFT JOIN users u on (u.user_id=r.user_id)
                        LEFT JOIN users u2 on (u2.user_id=rq.user_id)
                        WHERE rq.user_id=%s
                        """
        try:
            connection = DataBaseConnection()
            dict_cursor = connection.dict_cursor
            dict_cursor.execute(my_requests, (self.id,))
            row = dict_cursor.fetchone()
            requests = []
            while row:
                ride = Ride.create_ride_instance(row)

                temp_request = Ride.create_request_instance(ride, row)

                requests.append(temp_request.__dict__)
                row = dict_cursor.fetchone()

            return requests
        except Exception as exp:
            print(exp)
