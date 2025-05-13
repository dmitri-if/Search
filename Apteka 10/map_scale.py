def calculate_spn(toponym):
    envelope = toponym['boundedBy']['Envelope']
    lower_corner = list(map(float, envelope['lowerCorner'].split()))
    upper_corner = list(map(float, envelope['upperCorner'].split()))
    
    delta_lon = abs(upper_corner[0] - lower_corner[0]) * 1.5
    delta_lat = abs(upper_corner[1] - lower_corner[1]) * 1.5
    
    return f"{delta_lon},{delta_lat}"