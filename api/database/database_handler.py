import psycopg2
import psycopg2.extras as extra
from flask import current_app


class DataBaseConnection:
    def __init__(self, database=None):
            try:
                if database:
                    self.connection = psycopg2.connect(database=database, user="mczhkqyutgspud",
                                                       password="bc4506c9ca483df2d1756d8fecebdc9" +
                                                                "095df6593414ac3e85b7962f019252600",
                                                       host="ec2-23-23-248-192.compute-1.amazonaws.com",
                                                       port="5432")
                else:
                    if current_app.config["TESTING"]:
                        self.connection = psycopg2.connect(database=current_app.config["TEST_DATABASE"], user="ucbqtxsiwvfoyw",
                                                           password="12085cfa573cb6e106d198baae33" +
                                                                    "02839719753a1f7c2c519dc743e92e7661eb",
                                                           host="ec2-23-23-248-192.compute-1.amazonaws.com",
                                                           port="5432")
                    else:

                        self.connection = psycopg2.connect(database=current_app.config["DATABASE"], user="mczhkqyutgspud",
                                                           password="bc4506c9ca483df2d1756d8fecebdc9" +
                                                                    "095df6593414ac3e85b7962f019252600",
                                                           host="ec2-23-23-248-192.compute-1.amazonaws.com",
                                                           port="5432")

                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
                self.dict_cursor = self.connection.cursor(cursor_factory=extra.DictCursor)

                self.create_tables()
            except Exception as exp:
                print(exp)

    def create_tables(self):
        # status pending,approved, rejected
        queries = (
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS rides (
                ride_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                origin VARCHAR(255) NOT NULL,
                destination VARCHAR(255) NOT NULL,
                departure_time timestamp,
                slots integer,
                description text,
                FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS ride_requests (
                request_id SERIAL PRIMARY KEY,
                ride_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (ride_id)
                    REFERENCES rides (ride_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                status VARCHAR(10) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS friend_requests (
                request_id SERIAL PRIMARY KEY,
                from_user INTEGER NOT NULL,
                to_user INTEGER NOT NULL,
                FOREIGN KEY (from_user)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (to_user)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                status VARCHAR(10) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                message text,
                FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE 
            )
            """
        )

        for query in queries:
            self.cursor.execute(query)

    def drop_test_tables(self):
        queries = ("""
                DROP TABLE IF EXISTS users cascade 
                """,
                """
                DROP TABLE IF EXISTS rides cascade
                """,
                """
                DROP TABLE IF EXISTS ride_requests cascade
                """,
                """
                DROP TABLE IF EXISTS friend_requests cascade
                """,
                """
                DROP TABLE IF EXISTS notifications cascade
                """
                   )
        for query in queries:
            self.cursor.execute(query)


if __name__ == "__main__":
    db_connection = DataBaseConnection("dbl39rci502hrl")
    db_connection.create_tables()
