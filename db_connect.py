# тут работа с базой данных
# подключение добавление и извлечение данных
import psycopg2
from dotenv import load_dotenv
import os

class Database:
    """
    A class to handle database connection and query execution using psycopg2.
    """

    def __init__(self):
        """
        Initializes the database configuration from environment variables.
        """
        load_dotenv()
        self.config = {
            'dbname': os.getenv("DATABASE"),
            'user': os.getenv("USER"),
            'password': os.getenv("PASSWORD"),
            'host': os.getenv("HOST"),
            'port': os.getenv("PORT"),
        }
        self.connection = None

    def connect_to_db(self):
        """
        Establishes a connection to the database if not already connected.
        :return: The database connection or None if the connection fails.
        """
        if not self.connection:
            try:
                self.connection = psycopg2.connect(**self.config)
            except psycopg2.Error as er:
                print(f"Database connection error: {er}")
                self.connection = None
        return self.connection

    def execute_query(self, query, params=None, connection=None):
        """
        Executes an SQL query.

        :param query: The SQL query string.
        :param params: Optional parameters for the query (tuple).
        :return: Query result for SELECT statements, or None for others.
        """
        manage_connection = False 
        if not connection:
            connection = self.connect_to_db()
            if not connection:
                print("Connection to the database failed.")
                return None
            manage_connection = True  # Флаг для закрытия соединения
        else:
            manage_connection = False

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall()
                else:
                    connection.commit()
                    result = None
            return result
        except psycopg2.Error as er:
            print(f"Error: {er}")
            if manage_connection:
                connection.rollback()
            return None
        finally:
            if manage_connection:
                connection.close()

# Example usage
# test = Database()
# print(test.connect_to_db())





















