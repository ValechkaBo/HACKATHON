from api_connect import fetch_product_data

if __name__ == "__main__":
    product_name = input("Write a product name: ")
    product_data = fetch_product_data(product_name)
    if product_data:
        print("Product info:")
        print(f"Calories: {product_data['calories']}")
        print(f"Proteins: {product_data['proteins']} g")
        print(f"Fat: {product_data['fats']} g")
        print(f"Carbs: {product_data['carbs']} g")
    else:
        print("Information about product not found.")