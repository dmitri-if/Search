import requests
from map_scale import calculate_spn


def geocode(address):
    geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
    
    geocoder_params = {
        "apikey": 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
        "geocode": address,
        "format": "json"
    }
    
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        raise RuntimeError(f"Ошибка выполнения запроса: {response.status_code}")
    
    json_response = response.json()
    return json_response

def show_map(ll, spn, pt=None):
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        "size": "650,450"
    }
    
    if pt:
        map_params["pt"] = pt
    
    response = requests.get(map_api_server, params=map_params)
    
    # Сохранение карты в файл
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    
    return map_file


if __name__ == '__main__':
    try:
        address = input("Введите адрес: ")
        
        response = geocode(address)
        toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coordinates = toponym["Point"]["pos"]
        ll = toponym_coordinates.replace(" ", ",")
        
        spn = calculate_spn(toponym)
        
        pt = f"{ll},pm2rdm"
        
        map_file = show_map(ll, spn, pt)
        print(f"Карта сохранена в файл: {map_file}")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")