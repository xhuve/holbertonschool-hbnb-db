import sys
import os

from flask_jwt_extended import get_jwt_identity, jwt_required

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import request, jsonify, Blueprint
from persistence.data_manager import DataManager
from models.city import City


city_bp = Blueprint("city_bp", __name__)

@city_bp.route('/cities', methods=['GET'], endpoint="get_all_cities")
def get_all_cities():
    allCities = DataManager.all(City)
    if allCities:
        return jsonify([value.to_dict() for value in allCities])
    return jsonify("No cities")

@city_bp.route('/cities', methods=['POST'], endpoint="create_city")
@jwt_required
def create_city():
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

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
    DataManager.save(city)
    return jsonify(city.to_dict()), 201

@city_bp.route('/cities/<int:city_id>', methods=['GET'], endpoint="get_city")
def get_city(city_id):
    curr_city = DataManager.get(city_id, City)
    return { "name": curr_city["name"], "country_code": curr_city["country_code"] }

@city_bp.route('/cities/<int:city_id>', methods=['PUT'], endpoint="update_city")
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


@city_bp.route('/cities/<int:city_id>', methods=['DELETE'], endpoint="delete_city")
@jwt_required
def delete_city(city_id):
    curr_user = get_jwt_identity()
    if not curr_user.is_admin:
        return jsonify("User does not have admin privileges"), 403

    DataManager.delete(city_id, City)
    return jsonify("Deleted"), 204

