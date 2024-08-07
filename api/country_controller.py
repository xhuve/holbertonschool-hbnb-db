import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from flask import jsonify, Blueprint
from persistence.data_manager import DataManager
from models.country import Country

country_bp = Blueprint("country", __name__)

@country_bp.route('/countries', methods=['GET'])
def get_all_countries():
    allCountries = DataManager.all(Country)
    if allCountries:
        return jsonify([value.to_dict() for value in allCountries])
    return jsonify("No countries")

@country_bp.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    return jsonify(DataManager.get(country_id, Country).to_dict())

@country_bp.route("/countries/<string:country_code>/cities", methods=['GET'])
def get_city_in_country(country_code):
    for city in DataManager.all(Country):
        if not country_code in city['code']:
            return jsonify("Bad Request"), 400
    
    from  models.city import City
    all_cities = [value for value in DataManager.all(City) if value["country_code"] == country_code]
    return all_cities

