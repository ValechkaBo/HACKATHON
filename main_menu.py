# главный файл для запуска программы
from db_connect import Database
from user_func import User


def main_menu():
    database = Database()
    user_name = input("Enter your name: ")
    user = User(user_name, database)

    while True:
        print("----- CALORIE COUNTER -----")
        print("1. Set daily calorie limit")
        print("2. Add a product")
        print("3. View daily consumption")
        print("4. Check if limit is exceeded")
        print("5. Exit")
        print("---------------------------")
       
        user_choice = input("Choose an action:  ")

        if user_choice == "1":
            daily_limit = int(input("Enter your daily calories limit:  "))
            user.set_daily_limit(daily_limit)
        elif user_choice == "2":
            product_name = input("Enter product name: ")
            quantity = float(input("Enter quantity in grams: "))
            meal_type = input("Enter meal type (breakfast, lunch, dinner, snack): ")
            user.add_meal(product_name, quantity, meal_type)
        elif user_choice == "3":
            user.view_daily_meals()
        elif user_choice == "4":
            user.check_limit()
        elif user_choice == "5":
            print("You exit the program! See you!")
            break
        else:
            print("Invalid input. Choose an action from the menu")

if __name__ == "__main__":
    main_menu()


                
