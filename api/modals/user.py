from api.database.database import DataBaseConnection


class User:
    """User class defines the methods needed by user and the attributes.
        on creation pass in id,name,email,password"""

    connection = DataBaseConnection()

    def __init__(self, _id, name, email, password, confirm):
        self.id = _id
        self.name = name
        self.email = email
        self.password = password
        self.confirm = confirm

    @staticmethod
    def create_user(name, email, password):
        cursor = User.connection.cursor
        query_string = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
        cursor.execute(query_string, (name, email, password))
    
    @staticmethod   
    def get_user_by_email(email):
        cursor = User.connection.dict_cursor
        query_string = "SELECT * FROM users WHERE email = %s "
        cursor.execute(query_string, [email])
        row = cursor.fetchone()
        return row
    
    @staticmethod
    def get_all_users():
        cursor = User.connection.dict_cursor
        query_string = "SELECT * FROM users"
        cursor.execute(query_string)
        return cursor.fetchall()
