# тут работа с базой данных
# подключение добавление и извлечение данных
import psycopg2
from dotenv import load_dotenv
import os

class Database:
    
    #A class to handle database connection and query execution using psycopg2.
    def __init__(self):
        
        #Initializes the database configuration from environment variables.
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
 
        #Establishes a connection to the database if not already connected.
        #:return: The database connection or None if the connection fails.
    
        if not self.connection:
            try:
                self.connection = psycopg2.connect(**self.config)
            except psycopg2.Error as er:
                print(f"Database connection error: {er}")
                self.connection = None
        return self.connection

    def execute_query(self, query, params=None, connection=None):
   
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








    # def create_tables(self):
    #     queries = [
    #         """
    #         CREATE TABLE IF NOT EXISTS users (
    #             id SERIAL PRIMARY KEY,
    #             name VARCHAR(50) UNIQUE NOT NULL,
    #             daily_calories_limit INTEGER NOT NULL
    #         );
    #         """,
    #         """
    #         CREATE TABLE IF NOT EXISTS products (
    #             id SERIAL PRIMARY KEY,
    #             name VARCHAR(100) UNIQUE NOT NULL,
    #             calories REAL NOT NULL,
    #             proteins REAL NOT NULL,
    #             fats REAL NOT NULL,
    #             carbs REAL NOT NULL
    #         );
    #         """,
    #         """
    #         CREATE TABLE IF NOT EXISTS meals (
    #             id SERIAL PRIMARY KEY,
    #             user_id INTEGER NOT NULL,
    #             product_id INTEGER NOT NULL,
    #             meal_type VARCHAR(50) NOT NULL,
    #             quantity REAL NOT NULL,
    #             meal_date DATE NOT NULL DEFAULT CURRENT_DATE,
    #             CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    #             CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    #             UNIQUE (user_id, product_id, meal_type, meal_date)
    #         );
    #         """
    #     ]
    #     try:
    #         connection = self.connect_to_db()  # Assuming connect_to_db() exists in db_connect.py
    #         if not connection:
    #             print("Failed to connect to the database.")
    #             return
    #         with connection.cursor() as cursor:
    #             for query in queries:
    #                 cursor.execute(query)
    #             connection.commit()
    #         print("Tables created successfully or already exist.")
    #         cursor.close()
    #     except Exception as e:
    #         print(f"Error creating tables: {e}")
            
# db = Database()
# db.create_tables()
# Example usage
# test = Database()
# print(test.connect_to_db())





















