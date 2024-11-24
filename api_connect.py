# тут подключимся к api

import requests

app_id = "784d81cb"  
api_key = "e26479912107ab051625b014068cd16f"
url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

def fetch_product_data(product_name):
    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"   # Тело запроса в формате JSON
    }
    data = {"query": product_name}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        food = response.json()["foods"][0]
        return {
            'calories': food['nf_calories'],
            'proteins': food['nf_protein'],
            'fats': food['nf_total_fat'],
            'carbs': food['nf_total_carbohydrate']
        }
    except Exception as ex:
        print(f'Error {ex}')
    