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
        try:   
            product_name = product_name.strip().lower() #форматируем
            product_data = None
            connection = self.db.connect_to_db() #устанавлиаем связь
            if not connection:
                raise ConnectionError("Failed to connect to the database.")

            product_id_query = '''SELECT id FROM products WHERE LOWER(name) = LOWER(%s);'''
            with connection.cursor() as cursor:
                cursor.execute(product_id_query, (product_name,))
                product_id = cursor.fetchone()

            if not product_id:
                    print(f"Fetching product data for '{product_name}'...")
                    product_data = fetch_product_data(product_name)
                    print(f"Fetched data: {product_data}")
            if not product_data:
                    print(f"Information for product '{product_name}' not found in API.")
                    return

            
            #добавляем автоматически юзера если его еще нет и ставим лимит кал по умолчанию
            user_query_insert= '''
            INSERT INTO users (name, daily_calories_limit)
            VALUES (%s, 2000)  -- Лимит по умолчанию
            ON CONFLICT (name) DO NOTHING;
            '''
            self.db.execute_query(user_query_insert, (self.name,))

            # user_query_select = '''
            # SELECT id FROM users WHERE name = %s;
            # '''
            # with connection:
            #     with connection.cursor() as cursor:
            #         cursor.execute(user_query_select, (self.name,))
            #         user_id = cursor.fetchone()[0]
            
            if product_data:
                product_query ='''
                    INSERT INTO products (name, calories, proteins, fats, carbs)
                    VALUES (LOWER(%s), %s, %s, %s, %s)
                    ON CONFLICT (LOWER(name)) DO NOTHING
                    RETURNING id;
                    '''
                print(f"Inserting product data: {product_data}")
                print(f"Product ID after insert: {product_id}")

                with connection.cursor() as cursor:
                    cursor.execute(product_query, (
                        product_name,
                        product_data["calories"],
                        product_data["proteins"],
                        product_data["fats"],
                        product_data["carbs"]
                        ))

                    result = cursor.fetchone()  # Сохраняем результат в переменную
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
            
            self.db.execute_query(meal_query, (self.name, product_name, meal_type, quantity))
            print(f"Added {quantity}g of {product_name} for {meal_type}.")

        except Exception as ex:
            print(f"An error occurred: {ex}")
            print(f"An error occurred: {ex}", exc_info=True)



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