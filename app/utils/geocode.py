import requests

# According to the OpenStreetMap API to get the Adress
def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"format": "json", "lat": lat, "lon": lon, "zoom": 18, "addressdetails": 1}
    headers = {"User-Agent": "MyTouristMapApp/1.0"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=8)
    except requests.RequestException as e:
        return {"error": f"reverse geocode failed: {e}"}

    if resp.status_code != 200:
        return {"error": f"reverse geocode http {resp.status_code}"}

    data = resp.json()
    addr = data.get("address", {})
    location = (addr.get("building") or addr.get("attraction") or addr.get("place") or addr.get("tourism") or addr.get("historic") or addr.get("leisure") or addr.get("neighbourhood") or addr.get("suburb"))
    street = (addr.get("road") or addr.get("pedestrian") or addr.get("footway") or addr.get("street"))
    city = (addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or addr.get("county"))
    full_address = data.get("display_name")

    if not city and not street and not location:
        return {"error": "no usable address fields", "full_address": full_address}

    return {
        "city": city,
        "street": street,
        "location": location,
        "full_address": full_address
    }
