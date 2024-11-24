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
            product_name = product_name.strip().lower()  # Форматируем
            product_data = None
            connection = self.db.connect_to_db()  # Устанавливаем связь

            with connection:  # Управление транзакцией
                with connection.cursor() as cursor:
                    # Проверяем продукт в базе
                    product_id_query = '''SELECT id FROM products WHERE LOWER(name) = LOWER(%s);'''
                    cursor.execute(product_id_query, (product_name,))
                    product_id = cursor.fetchone()
                    product_id = product_id[0] if product_id else None

                    if not product_id:  # Если продукта нет, получаем данные из API
                        print(f"Fetching product data for '{product_name}'...")
                        product_data = fetch_product_data(product_name)
                        print(f"Fetched data: {product_data}")

                        if not product_data:
                            print(f"Information for product '{product_name}' not found in API.")
                            return

                        # Проверка данных перед вставкой
                        if not all(isinstance(product_data[key], (int, float)) for key in ['calories', 'proteins', 'fats', 'carbs']):
                            print(f"Invalid product data: {product_data}")
                            return

                        # Вставляем продукт в базу
                        product_query = '''
                            INSERT INTO products (name, calories, proteins, fats, carbs)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (LOWER(name)) DO NOTHING
                            RETURNING id;
                        '''
                        cursor.execute(product_query, (
                            product_name,
                            product_data["calories"],
                            product_data["proteins"],
                            product_data["fats"],
                            product_data["carbs"]
                        ))
                        result = cursor.fetchone()
                        product_id = result[0] if result else None

                        if not product_id:  # Если вставка не произошла, получаем id продукта
                            cursor.execute('SELECT id FROM products WHERE LOWER(name) = LOWER(%s);', (product_name,))
                            product_id = cursor.fetchone()
                            product_id = product_id[0] if product_id else None

                    if not product_id:
                        print(f"Failed to insert or retrieve product ID for '{product_name}'.")
                        return

                    # Добавляем пользователя
                    user_query_insert = '''
                        INSERT INTO users (name, daily_calories_limit)
                        VALUES (%s, 2000)
                        ON CONFLICT (name) DO NOTHING;
                    '''
                    self.db.execute_query(user_query_insert, (self.name,), connection=connection)

                    # Добавляем прием пищи
                    meal_query = '''
                        INSERT INTO meals (user_id, product_id, meal_type, quantity, meal_date)
                        VALUES (
                            (SELECT id FROM users WHERE name = %s),
                            %s,
                            %s, %s, CURRENT_DATE
                        )
                        ON CONFLICT (user_id, product_id, meal_type, meal_date)
                        DO UPDATE SET quantity = meals.quantity + EXCLUDED.quantity;
                    '''
                    cursor.execute(meal_query, (self.name, product_id, meal_type, quantity))
                    print(f"Added {quantity}g of {product_name} for {meal_type}.")
                cursor.close()              
        except Exception as ex:
            print(f"An error occurred: {ex}")


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
        connection = self.db.connect_to_db()
        query = ''' 
            SELECT SUM((meals.quantity * products.calories) / 100) AS total_calories
            FROM meals
            JOIN users ON meals.user_id = users.id
            JOIN products ON meals.product_id = products.id
            WHERE users.name = %s AND meal_date = CURRENT_DATE;
        '''
        get_limit_query = '''
        SELECT daily_calories_limit FROM users WHERE name = %s;
        '''
    
        with connection:
            with connection.cursor() as cursor:       #with  автоматически закрывает соединение даже если возникают ошибкт
                cursor.execute(get_limit_query, (self.name,))
                result = cursor.fetchone()  # Получаем одну строку из результата
                if result and result[0] is not None:
                    self.daily_limit = float(result[0])  # Устанавливаем лимит из базы
                else:
                    print(f"Daily calorie limit is not set for user '{self.name}'. Please set it first.")
                    return
                
                cursor.execute(query, (self.name,))      #запятая нужна потому что надо передавать кортеж
                result = cursor.fetchone()
                total_calories = result[0] or 0  # Если ничего не съедено, возвращаем 0
                remaining_calories = self.daily_limit - total_calories
            if total_calories > self.daily_limit:
                print(f"Warning! You have exceeded your daily calorie limit of {self.daily_limit} calories.")
            else:
                print(f"You have consumed {total_calories} calories today. Limit is {self.daily_limit} calories.")
                print(f"You have {remaining_calories} calories remaining for today.")