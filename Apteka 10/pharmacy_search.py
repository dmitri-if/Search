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
    json_response = response.json()
    return json_response


def search_pharmacies(ll, count=10):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    
    search_params = {
        "apikey": 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
        "text": "аптека",
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz",
        "results": count
    }
    
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    return json_response['features']


def get_point_color(pharmacy):
    hours = pharmacy['properties'].get('CompanyMetaData', {}).get('Hours', {})
    
    if not hours:
        return 'gray'
    
    if hours.get('Availabilities', [{}])[0].get('TwentyFourHours'):
        return 'green'
    else:
        return 'blue'


def prepare_points(pharmacies, original_ll):
    points = [f"{original_ll},pm2rdm"]
    for pharmacy in pharmacies:
        coords = pharmacy['geometry']['coordinates']
        ll = f"{coords[0]},{coords[1]}"
        color = get_point_color(pharmacy)
        points.append(f"{ll},pm2{color}m")
    
    return "~".join(points)


def show_map(ll, spn, points):
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        "size": "650,450",
        "pt": points
    }
    
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    
    return map_file