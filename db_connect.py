# тут работа с базой данных
# подключение добавление и извлечение данных

import psycopg2
from dotenv import load_dotenv
import os
# доступ к переменным окружения os

#создаем класс для удобства пользования подключением и запросами 

class Database:
    def __init__(self): # начальный инициализатор класса
        load_dotenv()   #агружаем переменные из скрытого файла
        self.config = {
            'dbname' : os.getenv("DATABASE"),
            'user' : os.getenv("USER"),
            'password' : os.getenv("PASSWORD"),
            'host' : os.getenv("HOST"),
            'port' : os.getenv("PORT"),
        }
        self.connection = None    #нужно для хранения текущего соединения с БД 

    def connect_to_db(self):    # чекаем если уже установленное соединениеб если нет то соединяем 
         if not self.connection:  #чтобы пытался установить соединение пок аоно None
             try:
                self.connection = psycopg2.connect(**self.config)   #** - это способ распаковать словарь 
             except psycopg2.Error as er:
                 print(f"Database connection error: {er}")
                 self.connection = None
             return self.connection     #необходимо вернуть чтобы им далее можно было воспользоваться
         
    def execute_query(self, query, params = None):   # метод для выполнения SQL запросов 
        connection = self.connect_to_db()
        if not connection:
            print("Connection to the database is failed")
            return None
        try:                           #with закроет соединение после запроса , создаем курсор для SQL
            with connection.cursor() as cursor:       #with  автоматически закрывает соединение даже если возникают ошибкт
                cursor.execute(query, params) 
                if query.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall() 
                else:                              #query - запрос , params - параметры (кортежи для подстановки в запрос)
                    connection.commit()
                    result = None
            return result
        except psycopg2.Error as er:                                 #перехватывает любые ошибки
            print(f"Error: {er}")
            return None

        # finally:                            #закрываем соединение даже если были ошибки 
        #     if self.connection:
        #         self.connection.commit()         # соединение в конце снова становится None


# test = Database()
# print(test.connect_to_db())

























