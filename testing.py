from db_connect import Database
from user_func import User


 
db = Database()
user = User(name="Luca", database = db)
print("=== Testing set_daily_limit ===")
user.set_daily_limit(1800)

print("\n=== Testing add_meal ===")
user.add_meal(product_name="Apple", quantity=150, meal_type="snack")

print("\n=== Testing view_daily_meals ===")
user.view_daily_meals()

print("\n=== Testing check_limit ===")
user.check_limit()