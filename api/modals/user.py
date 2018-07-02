import datetime
import jwt

from api.settings import config


class User:
    """User class defines the methods needed by user and the attributes.
        on creation pass in id,name,email,password"""
    def __init__(self, _id, name, email, password,confirm):
        self.id = _id
        self.name = name
        self.email = email
        self.password = password
        self.confirm = confirm

    @staticmethod
    def encode_authentication_token(user_id):
        """generates authentication token for a particular user"""
        try:
            payload = {"exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=360),
                       "iat": datetime.datetime.utcnow(),
                       "sub": user_id}
            return jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')  # algorithm for signing
        except Exception as exp:
            return exp

    @staticmethod
    def decode_authentication_token(auth_token):
        """Decodes the auth_token into the user id and returns the user id"""

        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY)
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return "Token Expired. Please Login Again"
        
        except jwt.InvalidTokenError:
            return "Invalid token. Please Login Again"
    
    @staticmethod
    def create_user(cursor, name, email, password):
        query_string = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
        cursor.execute(query_string, (name, email, password))
    
    @staticmethod   
    def get_user_by_email(dict_cursor, email):

        query_string = "SELECT * FROM users WHERE email = %s "
        dict_cursor.execute(query_string, [email])
        row = dict_cursor.fetchone()
        return row
    
    @staticmethod
    def get_all_users(dict_cursor):
        query_string = "SELECT * FROM users"
        dict_cursor.execute(query_string)
        return dict_cursor.fetchall()
