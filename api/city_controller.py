import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.city import City


city_bp = Blueprint("city_bp", __name__)

@city_bp.route('/cities', methods=['GET'])
def get_all_cities():
    return DataManager.all(City)

@city_bp.route('/cities', methods=['POST'])
def create_city():
    jData = request.get_json()
    if not isinstance(jData["name"], str) or not isinstance(jData["population"], int):
        return jsonify("Bad Request"), 400

    from .country_controller import get_city_in_country
    dictionary = get_city_in_country(jData["country_code"])
    for item in dictionary:
        if item["name"] == jData["name"]:
            return jsonify("Bad Request"), 400

    city = City(
        name=jData["name"],
        population=jData["population"],
        country_code=jData["country_code"]
    )
    return DataManager.save(city), 201

@city_bp.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    curr_city = DataManager.get(city_id, City)
    return { "name": curr_city["name"], "country_code": curr_city["country_code"] }

@city_bp.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    jData = request.get_json()
    req_city = DataManager.get(city_id, City)

    city = City(
        name=jData['name'],
        population=jData['population'],
        country_code=jData['country_code']
    )

    city.id = city_id
    city.created_at = req_city["created_at"]

    try:
        DataManager.update(city)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400


@city_bp.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_cities(city_id):
    DataManager.delete(city_id, City)
    return jsonify("Deleted"), 204

