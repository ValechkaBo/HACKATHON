

-- TABLE FOR USERS
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY, 
--     name TEXT UNIQUE NOT NULL, 
--     daily_calories_limit INTEGER DEFAULT 2000 -- Лимит калорий по умолчанию
-- );

--TABLE FOR PRODUCTS
-- CREATE TABLE products (
--     id SERIAL PRIMARY KEY, -- Уникальный идентификатор продукта
--     name TEXT UNIQUE NOT NULL, -- Уникальное название продукта
--     calories FLOAT NOT NULL, 
--     proteins FLOAT NOT NULL, 
--     fats FLOAT NOT NULL, 
--     carbs FLOAT NOT NULL 
-- );

-- CREATE UNIQUE INDEX unique_product_name ON products (LOWER(name));

-- TABLE FOR MEALS
-- CREATE TABLE meals (
--     id SERIAL PRIMARY KEY, -- Уникальный идентификатор приема пищи
--     user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- Внешний ключ к пользователям
--     product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE, -- Внешний ключ к продуктам
--     meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')), -- Тип приема пищи
--     quantity FLOAT NOT NULL, 
--     meal_date DATE NOT NULL DEFAULT CURRENT_DATE, 
--     UNIQUE (user_id, product_id, meal_type, meal_date) -- Уникальность для предотвращения дубликатов
-- );
