from flask import Blueprint, request, jsonify
from app.utils.geocode import reverse_geocode
from app.services.tourist_service import generate_tourist_info

bp = Blueprint("main_routes", __name__)

# Get the Requests and return the response
@bp.route('/generate', methods=['POST'])
def tourist_info():
    data = request.get_json() or {}
    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat is None or lon is None:
        return jsonify({"error": "missing latitude or longitude"}), 400

    addr = reverse_geocode(lat, lon)
    if not addr or addr.get("error"):
        return jsonify({"error": "reverse geocoding failed", "detail": addr}), 502

    city = addr.get("city")
    street = addr.get("street")
    location = addr.get("location")
    preference = data.get("preference")
    return_base64 = data.get("base64", True)

    result = generate_tourist_info(city, street, location, preference, return_base64)
    return jsonify(result)
