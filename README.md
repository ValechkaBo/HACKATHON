# Calorie Counter

## About the Project
**Calorie Counter** is a simple tool to help users track their daily calorie intake. It solves the problem of managing diets and monitoring nutrition by:
- Allowing users to set and update daily calorie limits.
- Adding consumed foods with accurate nutritional values.
- Fetching food data (calories, protein, fat, carbs) via the Nutritionix API.
- Displaying daily consumption and checking if the calorie limit is exceeded.

---

## Features
- Set and update daily calorie limits.
- Add meals with real-time food data from Nutritionix API.
- View daily food consumption.
- Check if the calorie limit is exceeded.

---

## How to Run

### 1. Install Dependencies
1. Make sure you have Python 3.8+ installed.
2. Create a virtual environment:
   ```bash
   python -m venv my_env


### 2. Activate the environment:

my_env\Scripts\activate

### 3. Install required libraries:

pip install -r requirements.txt

### 4. Create a .env file in the project root with the following:

DATABASE=calorie_counter
USER=your_postgres_username
PASSWORD=your_postgres_password
HOST=localhost
PORT=5432
API_APP_ID=your_nutritionix_app_id
API_APP_KEY=your_nutritionix_app_key


### 5. Set Up the Database
CREATE DATABASE calorie_counter;

Сreate all tables from sql file (users, products, meals)

### 6. Files desription
## api_connect.py
Purpose: Handles the connection to the Nutritionix API.
Functionality:
Sends a request to the Nutritionix API to fetch nutritional information about a product.
Parses and returns details like calories, proteins, fats, and carbohydrates.
Prints error messages if the API request fails. (api_connect)
## checker_api.py
Purpose: A simple script to test the API connection and functionality.
Functionality:
Imports fetch_product_data from api_connect.py.
Prompts the user for a product name.
Fetches and displays nutritional information about the product if available, or an error message otherwise. (checker_api)

## db_connect.py
Purpose: Manages the connection to the PostgreSQL database and executes queries.
Functionality:
Establishes a connection to the database using credentials from a .env file.
Provides methods to execute SQL queries (SELECT, INSERT, UPDATE, etc.).
Automatically manages transactions and connection closing.
Key Features:
Handles errors during database operations.
Allows reusability of database connection logic. (db_connect)

## main_menu.py
Purpose: The main entry point for the program.
Functionality:
Displays a menu for the user to interact with the calorie counter.
Provides options to:
Set a daily calorie limit.
Add a product to the daily consumption.
View daily meals.
Check if the calorie limit has been exceeded.
Exit the program.
User Interaction:
Accepts user input and calls methods from the User class accordingly. (main_menu)

## testing.py
Purpose: A script for testing the functionality of the calorie counter.
Functionality:
Tests different methods of the User class:
Setting a daily calorie limit.
Adding a product and its quantity.
Viewing the daily meal summary.
Checking if the daily calorie limit is exceeded. (testing)

## user_func.py
Purpose: Implements the core functionality related to the user, such as setting calorie limits, managing meals, and checking limits.
Functionality:
set_daily_limit: Sets or updates the user's daily calorie limit.
add_meal: Adds a product to the database (if not already present) and logs its consumption.
Fetches nutritional data from the API if needed.
view_daily_meals: Displays all meals consumed by the user on the current day, including calories.
check_limit: Calculates total consumed calories and compares them to the user's daily limit.
Key Features:
Automatically handles product and user insertion into the database.
Provides detailed feedback for user actions. (user_func)


### 6. Run the Program
python main_main.py

### 7. Requirements
Python 3.8+
PostgreSQL
Nutritionix API keys

