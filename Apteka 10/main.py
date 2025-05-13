import argparse
from pharmacy_search import geocode, search_pharmacies, prepare_points, show_map
from map_scale import calculate_spn


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Поиск ближайших аптек')
    parser.add_argument('address', help='Адрес для поиска')
    args = parser.parse_args()
    
    try:
        geocode_result = geocode(args.address)
        toponym = geocode_result["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        original_ll = toponym["Point"]["pos"].replace(" ", ",")
        
        pharmacies = search_pharmacies(original_ll)
        
        if not pharmacies:
            print("Аптеки не найдены")
        
        points = prepare_points(pharmacies, original_ll)
        
        center_ll = original_ll
        spn = calculate_spn(toponym)
        
        map_file = show_map(center_ll, spn, points)
        
        print(f"Найдено {len(pharmacies)} аптек")
        print(f"Карта сохранена в файл: {map_file}")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")