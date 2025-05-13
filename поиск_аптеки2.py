import argparse
import requests
import math
from map_scale import calculate_spn


def geocode(address):
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/?'
    
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


def search_pharmacy(ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    
    search_params = {
        "apikey": 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
        "text": "аптека",
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz",
        "results": 10
    }
    
    response = requests.get(search_api_server, params=search_params)
    if not response:
        raise RuntimeError(f"Ошибка выполнения запроса: {response.status_code}")
    
    json_response = response.json()
    return json_response


def calculate_distance(point1, point2):
    lon1, lat1 = map(float, point1.split(','))
    lon2, lat2 = map(float, point2.split(','))
    
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi/2)**2 + 
         math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2)
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def show_map(ll, spn, pts):
    map_api_server = 'https://static-maps.yandex.ru/v1?'
    
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        "size": "650,450",
        "pt": "~".join(pts)
    }
    
    response = requests.get(map_api_server, params=map_params)
    
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    
    return map_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Поиск ближайшей аптеки')
    parser.add_argument('address', help='Адрес для поиска')
    args = parser.parse_args()
    
    try:
        geocode_result = geocode(args.address)
        toponym = geocode_result["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coords = toponym["Point"]["pos"]
        ll = toponym_coords.replace(" ", ",")
        address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        
        pharmacy_result = search_pharmacy(ll)
        if not pharmacy_result['features']:
            raise RuntimeError("Аптеки не найдены")
        
        pharmacy = pharmacy_result['features'][0]
        pharmacy_coords = ",".join(map(str, pharmacy['geometry']['coordinates']))
        pharmacy_name = pharmacy['properties']['name']
        pharmacy_hours = pharmacy['properties'].get('CompanyMetaData', {}).get('Hours', {}).get('text', 'нет данных')
        
        distance = calculate_distance(ll, pharmacy_coords)
        
        pts = [
            f"{ll},pm2rdm",
            f"{pharmacy_coords},pm2gnm"
        ]
        
        center_lon = (float(ll.split(',')[0]) + float(pharmacy_coords.split(',')[0])) / 2
        center_lat = (float(ll.split(',')[1]) + float(pharmacy_coords.split(',')[1])) / 2
        center_ll = f"{center_lon},{center_lat}"
        
        delta_lon = abs(float(ll.split(',')[0]) - float(pharmacy_coords.split(',')[0])) * 1.5
        delta_lat = abs(float(ll.split(',')[1]) - float(pharmacy_coords.split(',')[1])) * 1.5
        spn = f"{delta_lon},{delta_lat}"
        
        map_file = show_map(center_ll, spn, pts)
        
        snippet = f"""
        Исходный адрес: {address}
        Ближайшая аптека: {pharmacy_name}
        Адрес аптеки: {pharmacy['properties']['description']}
        Часы работы: {pharmacy_hours}
        Расстояние: {distance:.0f} метров
        """
        
        print(snippet)
        print(f"Карта сохранена в файл: {map_file}")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")