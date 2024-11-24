# тут будет пользовательское меню
# установка лимита
# ввод информации о сьеденном
# вывод информации
from api_connect import fetch_product_data
from db_connect import Database




class User:
    def __init__(self, name, db_instance = Database()):
        self.name = name
        self.db = db_instance
        self.daily_limit = None

    def set_daily_limit(self, limit):
        self.daily_limit = limit
        query = '''
        INSERT INTO users(name, daily_calories_limit)
        VALUES(%s, %s)
        ON CONFLICT (name) DO UPDATE
        SET daily_calories_limit = EXCLUDED.daily_calories_limit ;
        '''
        self.db.execute_query(query, (self.name, self.daily_limit))
        print(f"Daily calorie limit for {self.name} is set to {self.daily_limit} calories.")


    def add_meal(self, product_name, quantity, meal_type):
        #ищем по имени продукта в таблице в БД
        product_id_query = '''          
        SELECT id FROM products WHERE name = %s;
        '''
        connection = self.db.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(product_id_query, (product_name,))
                product_id = cursor.fetchone()
    
        if not product_id:
            print(f"Product '{product_name}' not found in the database. Fetching from API...")
            if not product_data:
                print(f"Information for product '{product_name}' not found in API.")
                return
        
        if not connection:
            print("Failed to connect to DB")
            return
        product_data = fetch_product_data(product_name)
        if not product_data:
            print(f"Information of this product not found")
            return
        
        #добавляем автоматически юзера если его еще нет и ставим лимит кал по умолчанию
        user_query_insert= '''
        INSERT INTO users (name, daily_calories_limit)
        VALUES (%s, 2000)  -- Лимит по умолчанию
        ON CONFLICT (name) DO NOTHING;
        '''
        self.db.execute_query(user_query_insert, (self.name,))
        user_query_select = '''
        SELECT id FROM users WHERE name = %s;
        '''
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(user_query_select, (self.name, self.name))
                user_id = cursor.fetchone()[0]
        
        product_query ='''
            INSERT INTO products (name, calories, proteins, fats, carbs)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id;
            '''
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(product_query, (
                product_name,
                product_data["calories"],
                product_data["proteins"],
                product_data["fats"],
                product_data["carbs"]
                ))

                result = cursor.fetchone()
                product_id = result[0] if result else None


        meal_query = '''
            INSERT INTO meals (user_id, product_id, meal_type, quantity, meal_date)
            VALUES (
                (SELECT id FROM users WHERE name = %s),
                (SELECT id FROM products WHERE name = %s),
                %s, %s, CURRENT_DATE
            )
            ON CONFLICT (user_id, product_id, meal_type, meal_date)
            DO UPDATE SET quantity = meals.quantity + EXCLUDED.quantity;'''
        
        self.db.execute_query(meal_query, (user_id, product_id, meal_type, quantity))
        print(f"Added {quantity}g of {product_name} for {meal_type}.")



    def view_daily_meals(self):
        query = """
            SELECT products.name, meals.quantity, products.calories
            FROM meals
            JOIN users ON meals.user_id = users.id
            JOIN products ON meals.product_id = products.id
            WHERE users.name = %s AND meal_date = CURRENT_DATE;
        """
        with self.db.connect_to_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (self.name,))
                meals = cursor.fetchall()
                print(f"Daily meals for {self.name}:")
        for meal in meals:
            product_name, quantity, calories = meal
            print(f"{product_name}: {quantity}g, {calories * quantity / 100:.2f} calories")



    def check_limit(self):
        query = ''' 
            SELECT products.name, meals.quantity, products.calories FROM meals
            JOIN users ON meals.user_id = users.id
            JOIN products ON meals.product_id = products.id
            WHERE users.name = %s AND meal_date = CURRENT_DATE;
            '''
        
        with self.db.connect_to_db() as connection, connection.cursor() as cursor:       #with  автоматически закрывает соединение даже если возникают ошибкт
                cursor.execute(query, (self.name))
                total_calories = cursor.fetchone()[0] or 0 # вернет 0 если не указан лимит 
        
        if total_calories > self.daily_limit:
            print(f"Warning! You have exceeded your daily calorie limit of {self.daily_limit} calories.")
        else:
            print(f"You have consumed {int(total_calories)} calories today. Limit is {self.daily_limit} calories.")



